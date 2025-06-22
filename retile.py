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


def load_subimages(
    subimg_size: Tuple[int, int], src_grid_dims: Tuple[int, int], src_glob: str
) -> Generator[List[Image.Image], None, None]:
    w, h = subimg_size
    for filename in sorted(glob.glob(src_glob)):
        src_page_img = Image.open(filename)
        for flat_index in range(math.prod(src_grid_dims)):
            j, i = divmod(flat_index, src_grid_dims[0])
            subimg = src_page_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
            if is_blank_image(subimg):
                # assumes non-blank images start in upper left and go right, then down
                break
            yield subimg


def is_blank_image(img: Image.Image) -> bool:
    return False  # TODO


def retile(
    subimg_size: Tuple[int, int],
    src_dims: Tuple[int, int],
    src_glob: str,
    dst_dims: Tuple[int, int],
    dst_glob: str,
):
    """Convert a bunch of grids of subimages into a different bunch of grids of subimages,
    with a different number of rows and columns from the source."""
    w, h = subimg_size
    for dst_page_number, subimgs in enumerate(
        batched(load_subimages(subimg_size, src_dims, src_glob), math.prod(dst_dims))
    ):
        n, m = dst_dims
        output_img = Image.new("RGB", (n * w, m * h), "white")
        for i, subimg in enumerate(subimgs):
            x = (i % n) * w
            y = (i // n) * h
            output_img.paste(subimg, (x, y))
        output_img.save(dst_glob.replace("*", f"{dst_page_number:02d}"))


# python tile.py 2 2 site-\*.jpg sites-\*.jpg
if __name__ == "__main__":
    if len(argv) != 9:
        print(
            "Usage: retile.py <tile_w> <tile_h> <src_w> <src_h> <src_glob> <dst_w> <dst_h> <dst_glob>\n"
            "Example: python retile.py 1358 1051 1 1 wip/site-\\*.jpg 2 2 wip/sites-\\*.png"
            "Note: escape asterisk with backslash in shell (e.g., site-\\*.jpg)\n"
        )
        exit(1)
    (
        subimage_w,
        subimage_h,
        src_tiling_cols,
        src_tiling_rows,
        src_glob,
        dst_tiling_cols,
        dst_tiling_rows,
        dst_glob,
    ) = argv[1:9]
    retile(
        (int(subimage_w), int(subimage_h)),
        (int(src_tiling_cols), int(src_tiling_rows)),
        src_glob,
        (int(dst_tiling_cols), int(dst_tiling_rows)),
        dst_glob,
    )
