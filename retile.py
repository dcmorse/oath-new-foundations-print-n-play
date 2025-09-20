from typing import Generator, List, Tuple
from PIL import Image
from sys import argv
from more_itertools import batched
import math
import glob


# Load subimages, break them into batches, write them to pages
# This file is currently used for sites and relics, but could probably be adapted
# to denizens and edifices.

# Relics are 2.25 x 2.25 inches and 672 x 672 pixels
# So that's 3 x 4 grid on 8.5 x 11 inch paper.


def constant_function(x):
    return lambda *args, **kwargs: x


truly = constant_function(True)


def load_subimages(
    subimg_size: Tuple[int, int],
    src_grid_dims: Tuple[int, int],
    src_glob: str,
    *,
    filter,
) -> Generator[List[Image.Image], None, None]:
    w, h = subimg_size
    for filename in sorted(glob.glob(src_glob)):
        src_page_img = Image.open(filename)
        for flat_index in range(math.prod(src_grid_dims)):
            j, i = divmod(flat_index, src_grid_dims[0])
            if filter(src_page_img, subimg_size, (i, j)):
                yield src_page_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))


def image_middle_not_all_white(
    src_page_img: Image.Image, subimg_size: Tuple[int, int], card_idxs: Tuple[int, int]
) -> bool:
    """For use with the retile filter argument"""
    w, h = subimg_size
    i, j = card_idxs
    sample_area = src_page_img.crop(
        ((i + 0.125) * w, (j + 0.125) * h, (i + 0.875) * w, (j + 0.875) * h)
    )
    extrema = sample_area.getextrema()
    if isinstance(extrema[0], tuple):
        # rgb/rgba - ignore alpha
        return not all(band[0] == band[1] == 255 for band in extrema[:3])
    else:
        # grayscale
        return not (extrema[0] == extrema[1] == 255)


def retile(
    subimg_size: Tuple[int, int],
    src_dims: Tuple[int, int],
    src_glob: str,
    dst_dims: Tuple[int, int],
    dst_glob: str,
    *,
    filter=truly,
):
    """Convert a bunch of grids of subimages into a different bunch of grids of subimages,
    with a different number of rows and columns from the source."""
    w, h = subimg_size
    for dst_page_number, subimgs in enumerate(
        batched(
            load_subimages(subimg_size, src_dims, src_glob, filter=filter),
            math.prod(dst_dims),
        )
    ):
        print(f"writing {dst_page_number=}")
        n, m = dst_dims
        output_img = Image.new("RGB", (n * w, m * h), "white")
        for i, subimg in enumerate(subimgs):
            x = (i % n) * w
            y = (i // n) * h
            output_img.paste(subimg, (x, y))
        output_img.save(dst_glob.replace("*", f"{dst_page_number:02d}"))
