from ctypes import Array
from itertools import count
from typing import Generator, List, Tuple
from PIL import Image
from sys import argv
from more_itertools import batched
import math

import numpy as np


# Load subimages, break them into batches, write them to pages
# This file is currently used for sites and relics, but could probably be adapted
# to denizens and edifices.

# Relics are 2.25 x 2.25 inches and 672 x 672 pixels
# So that's 3 x 4 grid on 8.5 x 11 inch paper.


def constant_function(x):
    return lambda *args, **kwargs: x


truly = constant_function(True)


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


def load_subimages(
    subimg_size: Tuple[int, int],
    src_grid_dims: Tuple[int, int],
    src_files: Array[str],
    *,
    filter=truly,
    # If numpy_filter is specified, ignore regular filter.
    # numpy_filter requires allocating a big slow array, but makes red triangle detection faster
    numpy_filter=None,
) -> Generator[List[Image.Image], None, None]:
    w, h = subimg_size
    for filename in src_files:
        src_page_img = Image.open(filename)
        src_page_array = np.array(src_page_img) if numpy_filter else None
        for flat_index in range(math.prod(src_grid_dims)):
            j, i = divmod(flat_index, src_grid_dims[0])
            if (
                numpy_filter(src_page_array, src_page_img, subimg_size, (i, j))
                if numpy_filter
                else filter(src_page_img, subimg_size, (i, j))
            ):
                yield src_page_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))


def load_images_2up(
    subimg_size: Tuple[int, int],
    src_grid_dims: Tuple[int, int],
    src_front_files: Array[str],
    src_back_files: Array[str],
    *,
    filter=truly,
) -> Generator[List[Image.Image], None, None]:
    w, h = subimg_size
    for src_f_filename, src_b_filename in zip(src_front_files, src_back_files):
        src_front_img = Image.open(src_f_filename)
        src_back_img = Image.open(src_b_filename)
        for flat_index in range(math.prod(src_grid_dims)):
            j, i = divmod(flat_index, src_grid_dims[0])
            front_filter = filter(src_front_img, subimg_size, (i, j))
            back_filter = filter(src_back_img, subimg_size, (i, j))
            if front_filter or back_filter:
                yield src_front_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
                yield src_back_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))


def retile(
    subimg_size: Tuple[int, int],
    subimg_gen: Generator[List[Image.Image], None, None],
    # src_dims: Tuple[int, int],
    # src_files: Array[str],
    dst_dims: Tuple[int, int],
    dst_glob: str,
):
    """Convert a bunch of grids of subimages into a different bunch of grids of subimages,
    with a different number of rows and columns from the source."""
    w, h = subimg_size
    for dst_page_number, subimgs in enumerate(batched(subimg_gen, math.prod(dst_dims))):
        print(f"writing {dst_page_number=}")
        n, m = dst_dims
        output_img = Image.new("RGB", (n * w, m * h), "white")
        for i, subimg in enumerate(subimgs):
            x = (i % n) * w
            y = (i // n) * h
            output_img.paste(subimg, (x, y))
        output_img.save(dst_glob.replace("*", f"{dst_page_number:02d}"))
