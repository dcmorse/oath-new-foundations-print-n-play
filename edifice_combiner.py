import math
import glob
from typing import List, Tuple
from PIL import Image
from PIL import ImageColor

src_px = (3366, 2102)
src_dims = (5, 2)
card_px = tuple(px // dim for (px, dim) in zip(src_px, src_dims))
dst_dims = (4, 2)

dx, dy = dst_dims
cx, cy = card_px
dst_px = (dx * cx, dy * cy)
dst_img = Image.new("RGB", dst_px, color="white")


def moddiv(a, b):
    x, y = divmod(a, b)
    return (y, x)


def is_non_blank_card(src_img, card_idxs) -> float:
    red = ImageColor.getrgb("#FFFFFF")
    expected_white_pixel_coordinates = [(100, 100), (500, 100), (100, 500), (500, 500)]
    w, h = card_px
    i, j = card_idxs

    def count_white_pixels(offset_pxs: List[Tuple[int]]):
        count = 0
        for rx, ry in offset_pxs:
            probe_px = (rx + i * w, ry + j * h)
            pixel_value = src_img.getpixel(probe_px)
            distance_from_white_squared = sum(
                (c1 - c0) ** 2 for (c1, c0) in zip(pixel_value, red)
            )
            if distance_from_white_squared <= 300:
                count += 1
        return count

    confidence = count_white_pixels(expected_white_pixel_coordinates)
    return confidence < len(expected_white_pixel_coordinates)


def requilt():
    dst_idx = 0
    dst_file_idx = 0

    def write_page():
        fname = f"wip/edifices-{dst_file_idx:02}.png"
        print("write_page()")
        dst_img.save(fname)
        dst_img.paste("white", (0, 0, dst_img.width, dst_img.height))

    for path in glob.glob("input/Edifice*.jpg"):
        print(f"{path=}")
        with Image.open(path) as src_img:
            for src_idxs in (
                (i, j) for j in range(src_dims[1]) for i in range(src_dims[0])
            ):
                if is_non_blank_card(src_img, src_idxs):
                    copy_subimage(src_img, src_idxs, moddiv(dst_idx, dst_dims[0]))
                    dst_idx += 1
                    if dst_idx == math.prod(dst_dims):
                        write_page()
                        dst_file_idx += 1
                        dst_idx = 0
    if dst_idx > 0:
        write_page()


def copy_subimage(src_img, src_dim, dst_dim):
    print(f"copy_subimage({src_dim=},{dst_dim=})")
    dx, dy = dst_dim
    sx, sy = src_dim
    w, h = card_px
    dst_lurd = (dx * w, dy * h, (dx + 1) * w, (dy + 1) * h)
    src_lurd = (sx * w, sy * h, (sx + 1) * w, (sy + 1) * h)
    clipboard = src_img.crop(src_lurd)
    dst_img.paste(clipboard, dst_lurd)


requilt()
