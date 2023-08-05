import csv
import io
import logging
import math
from pathlib import Path

import cv2
import imageio
import numpy as np
import pydicom
import requests
from pydicom import uid
from pydicom.encaps import encapsulate, generate_pixel_data_frame
from pydicom.pixel_data_handlers import apply_color_lut

from echoloader.lib import unpack

logger = logging.getLogger('echolog')


def is_video(img=None, shape=None):
    shape = shape or (isinstance(img, np.ndarray) and img.shape)
    return shape and (len(shape) == 4 or (len(shape) == 3 and shape[-1] > 4))


def ybr_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR)


def blank_top_bar(media, regions):
    video = is_video(media)
    image = np.mean(media, axis=0) if video else media
    new_image = np.mean(image[..., :3], axis=-1) if 3 <= image.shape[-1] <= 4 else image
    binary_image = (new_image > 2).astype('uint8')
    h = int(binary_image.shape[0] * 0.2)
    sum_pixel = np.sum(binary_image[:h, :], axis=1)
    top_bar = np.where(sum_pixel > (binary_image.shape[0] * 0.88))
    top_bar_bottom = 0
    if len(top_bar[0]) != 0:
        new_image[top_bar, :] = 0
        image[top_bar, :] = 0
        top_bar_bottom = top_bar[0][-1] + 1
    top_bar_bottom = max(top_bar_bottom, 40)
    mask = np.ones_like(media[0] if video else media)
    mask[:top_bar_bottom] = 0
    for region in regions:
        xo, xn = region.RegionLocationMinX0, region.RegionLocationMaxX1
        yo, yn = region.RegionLocationMinY0, region.RegionLocationMaxY1
        mask[yo:yn, xo:xn] = 1
    media *= mask


def mpeg4hp41(ds):
    frames = imageio.mimread(next(generate_pixel_data_frame(ds.PixelData)), memtest=False, format='mp4')
    return np.asarray(frames)


def unusual_frame_mean(px: np.ndarray, threshold=58):
    """
    If mean pixel value of frame is larger than threshold, background is likely non-black
    (usually happens when dicom tag is RGB but the frames are actually in YBR).
    """
    frame = px[px.shape[0] // 2] if is_video(px) else px  # take middle frame for video
    return frame.mean() > threshold


def parse_dicom_pixel(dicom):
    """Parse color space and coerce to RGB, and anonymize by blanking out top bar."""
    try:
        px = dicom.pixel_array
    except NotImplementedError as exc:
        handler = parse_dicom_pixel.custom_handlers.get(dicom.file_meta.TransferSyntaxUID)
        if not handler:
            raise exc
        px = handler(dicom)
    pi = dicom.PhotometricInterpretation
    dicom.PhotometricInterpretation = 'RGB'
    if pi in ['YBR_FULL', 'YBR_FULL_422', 'RGB'] and unusual_frame_mean(px):
        px = np.asarray([ybr_to_rgb(img) for img in px]) if is_video(px) else ybr_to_rgb(px)
    elif pi in ['PALETTE COLOR']:
        px = (apply_color_lut(px, dicom) // 255).astype('uint8')
    else:
        dicom.PhotometricInterpretation = pi
    return px


parse_dicom_pixel.custom_handlers = {
    uid.MPEG4HP41: mpeg4hp41,
}


def ensure_even(stream):
    # Very important for some viewers
    if len(stream) % 2:
        return stream + b"\x00"
    return stream


def person_data_callback(ds, e):
    if e.VR == "PN" or e.tag == (0x0010, 0x0030):
        del ds[e.tag]


def pad_to_multiple(arr, size, dims=(1, 2)):
    pad_dims = [(0, size - (s % size)) if i in dims else (0, 0) for i, s in enumerate(arr.shape)]
    return np.pad(arr, pad_dims, 'constant')


def package_dicom(ds, anonymize, compress):
    # Populate required values for file meta information
    ds.remove_private_tags()
    if not anonymize and not compress:
        return
    media = parse_dicom_pixel(ds)
    if anonymize:
        ds.walk(person_data_callback)
        blank_top_bar(media, getattr(ds, "SequenceOfUltrasoundRegions", []))
    video = is_video(media)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    if len(media.shape) < 3 + video:
        media = np.repeat(np.expand_dims(media, -1), 3, -1)
    ds.Rows, ds.Columns, ds.SamplesPerPixel = media.shape[video:]
    ds.PhotometricInterpretation = "YBR_FULL_422"
    if video:
        ds.StartTrim = 1
        ds.StopTrim = ds.NumberOfFrames = media.shape[0] if video else 1
        fps = getattr(ds, 'CineRate', 1000 / getattr(ds, 'FrameTime', 40))
        ds.CineRate = ds.RecommendedDisplayFrameRate = round(fps, 2)
        ds.FrameTime = 1000 / ds.CineRate
        ds.ActualFrameDuration = math.ceil(1000 / ds.CineRate)
        ds.PreferredPlaybackSequencing = 0
        ds.FrameDelay = 0
        if compress:
            ds.file_meta.TransferSyntaxUID = uid.MPEG4HP41
            ds.PixelData = encapsulate([
                imageio.mimwrite(imageio.RETURN_BYTES, pad_to_multiple(media, 16), fps=fps, format='mp4')])
        else:
            ds.file_meta.TransferSyntaxUID = uid.JPEGBaseline8Bit
            ds.PixelData = encapsulate([imageio.imwrite(imageio.RETURN_BYTES, img, format='jpg') for img in media])
    else:
        ds.file_meta.TransferSyntaxUID = uid.JPEGBaseline8Bit
        ds.PixelData = encapsulate([imageio.imwrite(imageio.RETURN_BYTES, media, format='jpg')])
    ds['PixelData'].is_undefined_length = True


def file_params(args, ds, ae_title, filename=None):
    customer = getattr(args, 'customer', '') or ae_title
    stem = '_'.join(map(str, filter(bool, [ds.SOPInstanceUID, filename])))
    return {
        'customer': customer or '',
        'trial': getattr(args, 'trial', None) or customer or '',
        'patient_id': ds.PatientID,
        'visit_id': ds.StudyID or ds.StudyInstanceUID or ds.StudyDate or 'No Study ID',
        'filename': f"{stem}.dcm",
    }


def upload(args, ds, param):
    logger.info(f'uploading {param}')
    content_type = 'application/dicom'
    headers = args.auth.get_headers()
    param['content_type'] = content_type
    upload_param = {}
    url = f"{args.auth.api_url}/dicom/upload"
    if args.env.cloud:
        r = requests.get(url, params=param, headers=headers)
        d = unpack(r)
        url = d['url']
        headers = d['headers']
    else:
        upload_param = param
    buf = io.BytesIO()
    ds.save_as(buf)
    buf.seek(0)
    return unpack(requests.put(url, data=buf.read(), headers=headers, params=upload_param))


def process(path=None, ds=None, ae_title=None, f=None, args=None):
    try:
        if args.closed:
            return
        path = path and Path(path)
        ds = ds or pydicom.dcmread(f or path)
        params = file_params(args, ds, ae_title=ae_title, filename=getattr(path, 'stem', None))
        logger.info(f'processing {params}')
        extracted = args.extracted
        k = tuple(params.values())
        if k not in extracted:
            if args.filter and not any(
                    getattr(ds, k, None) == v for f in args.filter for k, v in [f.split('=', 1)]):
                logger.info(f'Skipping {ds.SOPInstanceUID} due to no matching filter')
                return
            package_dicom(ds, anonymize=args.anonymize, compress=args.compress)
            dst = args.dst
            if dst:
                src = args.src
                rel = path.relative_to(src) if src else f"{ds.SOPInstanceUID}.dcm"
                out = (Path(dst) / rel).with_suffix(".dcm")
                if args.overwrite or not out.is_file():
                    out.parent.mkdir(exist_ok=True, parents=True)
                    ds.save_as(out)
            if hasattr(args, "auth"):
                upload(args, ds, params)
            extracted.add(k)
            if args.csv_out:
                csv.writer(open(args.csv_out, 'a', newline='')).writerow(k)
    finally:
        if f:
            f.close()
