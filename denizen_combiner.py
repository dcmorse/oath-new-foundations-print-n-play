import math
import glob
from typing import List, Tuple
from PIL import Image
from PIL import ImageColor
from edifice_combiner import is_non_blank_card

src_px = (6732, 5256)
src_dims = (10, 5)
card_px = tuple(px // dim for (px, dim) in zip(src_px, src_dims))
dst_dims = (4, 2)

# subimg = src.crop(tuple(round(x) for x in (3 * card_fpx[0], 1 * card_fpx[1], 4 * card_fpx[0], 2 * card_fpx[1])))  # box coords: (x1, y1, x2, y2)
# subimg.save("subimage.jpg")
dx, dy = dst_dims
cx, cy = card_px
dst_px = (dx * cx, dy * cy)
dst_img = Image.new("RGB", dst_px, color="white")


print(f"{card_px=}")


def moddiv(a, b):
    x, y = divmod(a, b)
    return (y, x)


def is_card_to_print(src_img, card_idxs) -> bool:
    return is_new_foundations_card(
        src_img, card_idxs
    ) or is_revised_base_card_with_red_triangle(src_img, card_idxs)


def is_new_foundations_card(src_img, card_idxs) -> bool:
    i, j = card_idxs
    if (i >= 3 and j == 3) or (i < 3 and j == 4):
        return is_non_blank_card(src_img, card_idxs)
    return False


def is_revised_base_card_with_red_triangle(src_img, card_idxs) -> bool:
    red = ImageColor.getrgb("#d22147")
    expect_red_pxs = [(638, 991), (628, 997), (646, 997), (638, 979)]
    expect_not_red_pxs = [(624, 928), (652, 982), (638, 1006)]
    w, h = card_px
    i, j = card_idxs

    def count_red_pixels(offset_pxs: List[Tuple[int]]):
        count = 0
        for rx, ry in offset_pxs:
            probe_px = (rx + i * w, ry + j * h)
            pixel_value = src_img.getpixel(probe_px)
            distance_from_red_squared = sum(
                (c1 - c0) ** 2 for (c1, c0) in zip(pixel_value, red)
            )
            if distance_from_red_squared <= 300:
                count += 1
        return count

    confidence = (
        count_red_pixels(expect_red_pxs) + 3 - count_red_pixels(expect_not_red_pxs)
    )
    if confidence == 6 or confidence == 5:
        print(f"unsure about {card_idxs=} - confidence {confidence}/7 this card is red")
    return confidence >= 5


def requilt():
    dst_idx = 0
    dst_file_idx = 0

    def write_page():
        fname = f"denizens-{dst_file_idx:02}.png"
        print("write_page()")
        dst_img.save(fname)
        dst_img.paste("white", (0, 0, dst_img.width, dst_img.height))

    for path in glob.glob("../oath-res/Denizens*.jpg"):
        print(f"{path=}")
        with Image.open(path) as src_img:
            for src_idxs in (
                (i, j) for j in range(src_dims[1]) for i in range(src_dims[0])
            ):
                if is_card_to_print(src_img, src_idxs):
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
