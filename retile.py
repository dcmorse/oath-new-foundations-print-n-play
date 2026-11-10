import glob
import os
from itertools import chain, count
from typing import Generator, List, Optional, Tuple, Iterable, Set, TypeVar
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

X = TypeVar("X")


def filter_by_idx(
    stream: Generator[X, None, None], idxs: Set[int]
) -> Generator[X, None, None]:
    for i, item in enumerate(stream):
        if i in idxs:
            yield item


def filter_by_idx_not(
    stream: Generator[X, None, None], idxs: Set[int]
) -> Generator[X, None, None]:
    for i, item in enumerate(stream):
        if i not in idxs:
            yield item


def load_subimages(
    subimg_size: Tuple[int, int],
    src_grid_dims: Tuple[int, int],
    src_files: Iterable[str],
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
    src_front_files: Iterable[str],
    src_back_files: Iterable[str],
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


def tile(
    images: Iterable[Image.Image],
    dst_dims: Tuple[int, int],
    dst_glob: str,
    *,
    size: Optional[Tuple[int, int]] = None,
    rotate_cw: bool = False,
) -> None:
    """Build grids: paste a stream of equally-sized images into pages of dst_dims
    (columns, rows), writing the pages to dst_glob (the * becomes a page number).

    size is the tile size; by default it is the size of the first image (after rotation).
    Images of any other size are resized to match, with a warning.
    rotate_cw rotates each image 90 degrees clockwise first.
    Pages left over from earlier runs matching dst_glob (and its -portrait/-landscape
    twin) are deleted first, so they can't leak into later steps."""
    def prepared() -> Generator[Image.Image, None, None]:
        for img in images:
            yield img.rotate(-90, expand=True) if rotate_cw else img

    stream = prepared()
    first = next(stream, None)
    if first is None:
        raise ValueError(f"no images to tile into {dst_glob}")
    w, h = size or first.size

    def uniform() -> Generator[Image.Image, None, None]:
        for k, img in enumerate(chain([first], stream)):
            if img.size != (w, h):
                print(f"warning: resizing image {k} from {img.size} to {(w, h)}")
                img = img.resize((w, h), resample=Image.LANCZOS)
            yield img

    for stale in set(glob.glob(dst_glob)) | set(
        glob.glob(dst_glob.replace("-portrait", "-landscape"))
    ):
        os.remove(stale)
    n, m = dst_dims
    for dst_page_number, subimgs in enumerate(batched(uniform(), n * m)):
        print(f"writing {dst_page_number=}")
        output_img = Image.new("RGB", (n * w, m * h), "white")
        for i, subimg in enumerate(subimgs):
            output_img.paste(subimg, ((i % n) * w, (i // n) * h))
        output_img.save(dst_glob.replace("*", f"{dst_page_number:02d}"))
