import math
import glob
from typing import List, Tuple
from PIL import Image
from PIL import ImageColor
import numpy as np


def is_denizen_to_print(src_array, src_img, subimage_size, card_idxs) -> bool:
    return (
        is_new_foundations_denizen(card_idxs)
        or is_card_with_red_triangle(src_array, src_img, subimage_size, card_idxs)
        or is_royal_ambitions(src_img, card_idxs)
    )


def is_royal_ambitions(src_img, card_idxs) -> bool:
    return card_idxs == (8, 1) and "Denizens Discord" in getattr(
        src_img, "filename", ""
    )


def is_new_foundations_denizen(card_idxs) -> bool:
    i, j = card_idxs
    return (i >= 3 and j == 3) or (i < 3 and j == 4)


def is_card_with_red_triangle(src_array, src_img, subimage_size, card_idxs) -> bool:
    red = ImageColor.getrgb("#d22147")
    expect_red_pxs = [(638, 995), (628, 1001), (646, 1001), (638, 983)]
    expect_not_red_pxs = [(624, 986), (652, 986), (638, 1010)]
    w, h = subimage_size
    i, j = card_idxs

    # only sample bottom right corner of the card
    scan_w, scan_h = 110, 130
    x0, y0, x1, y1 = (
        w * (i + 1) - scan_w,
        h * (j + 1) - scan_h,
        w * (i + 1),
        h * (j + 1),
    )
    sub_array = src_array[y0:y1, x0:x1]

    target_color = np.array(red)
    delta = 30

    # Calculate color distance for pixels in subregion only
    distances_squared = np.sum((sub_array - target_color) ** 2, axis=2)

    # Count pixels within delta
    red_pixel_count = np.sum(distances_squared <= delta**2)
    if red_pixel_count < 10:
        return False
    elif 48 <= red_pixel_count <= 69:
        return True
    else:
        log_red_triangle_uncertainty(i, j, w, h, src_img, red_pixel_count)
        return False


def log_red_triangle_uncertainty(i, j, w, h, src_img, count):
    err_img = src_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
    src_filename = getattr(src_img, "filename", "unknown")
    if src_filename:
        src_basename = src_filename.split("/")[-1].split(".")[0]
    else:
        src_basename = "unknown"
    print(
        f"WARNING: Uncertain red triangle detection {count} for card '{src_filename}' ({i}, {j}), logging image"
    )
    err_img.save(f"wip/den-err-{i}-{j}-{src_basename}.png")
