import math
import glob
from typing import List, Tuple
from PIL import Image
from PIL import ImageColor


def is_denizen_to_print(src_img, subimage_size, card_idxs) -> bool:
    return is_new_foundations_denizen(card_idxs) or is_card_with_red_triangle(
        src_img, subimage_size, card_idxs
    )


def is_new_foundations_denizen(card_idxs) -> bool:
    i, j = card_idxs
    return (i >= 3 and j == 3) or (i < 3 and j == 4)


def is_card_with_red_triangle(src_img, subimage_size, card_idxs) -> bool:
    red = ImageColor.getrgb("#d22147")
    nudge = 4
    expect_red_pxs = [(638, 991), (628, 997), (646, 997), (638, 979)]
    expect_not_red_pxs = [(624, 982), (652, 982), (638, 1006)]
    expect_not_red_pxs = [(x, y + nudge) for (x, y) in expect_not_red_pxs]
    expect_red_pxs = [(x, y + nudge) for (x, y) in expect_red_pxs]
    w, h = subimage_size
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
        print(f"unsure about {card_idxs=}")
        print(
            "confidence +{count_red_pixels(expect_red_pxs)}-{count_red_pixels(expect_not_red_pxs)} this card is red"
        )
        err_img = src_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
        for rx, ry in expect_red_pxs:
            err_img.putpixel((rx, ry), (0, 0, 0))
        for rx, ry in expect_not_red_pxs:
            err_img.putpixel((rx, ry), (0, 255, 0))
        # Get the original filename if available
        src_filename = getattr(src_img, "filename", "unknown")
        if src_filename:
            src_filename = src_filename.split("/")[-1].split(".")[0]
        else:
            src_filename = "unknown"
        err_img.save(f"wip/den-err-{i}-{j}-{src_filename}.png")
    # print(f"{card_idxs=} is red triangle? {confidence >= 5} ({confidence=})")
    return confidence >= 5


# def requilt():
#     dst_idx = 0
#     dst_file_idx = 0

#     def write_page():
#         fname = f"wip/denizens-{dst_file_idx:02}.png"
#         print("write_page()")
#         dst_img.save(fname)
#         dst_img.paste("white", (0, 0, dst_img.width, dst_img.height))

#     for path in glob.glob("input/Denizens*.jpg"):
#         print(f"{path=}")
#         with Image.open(path) as src_img:
#             for src_idxs in (
#                 (i, j) for j in range(src_dims[1]) for i in range(src_dims[0])
#             ):
#                 if is_denizen_to_print(src_img, src_idxs):
#                     copy_subimage(src_img, src_idxs, moddiv(dst_idx, dst_dims[0]))
#                     dst_idx += 1
#                     if dst_idx == math.prod(dst_dims):
#                         write_page()
#                         dst_file_idx += 1
#                         dst_idx = 0
#     if dst_idx > 0:
#         write_page()
