import glob
import os
from typing import Iterable, List, Tuple
import subprocess
from PIL import Image
from retile import load_subimages, retile, truly


def landscape_to_portrait(src_filenames: Iterable[str], *, ccw: bool = False):
    print("landscape_to_portrait")
    rotation = "-90" if ccw else "90"
    if not src_filenames:
        raise ValueError("no files to rotate")
    for landscape_file in src_filenames:
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", rotation, portrait_file], check=True
        )


def portrait_to_landscape(src_filenames: Iterable[str], *, ccw: bool = False):
    print("portrait_to_landscape")
    if not src_filenames:
        raise ValueError("no files to rotate")
    rotation = "-90" if ccw else "90"
    for portrait_file in src_filenames:
        landscape_file = portrait_file.replace("-portrait", "-landscape")
        subprocess.run(
            ["convert", portrait_file, "-rotate", rotation, landscape_file], check=True
        )


def typeset_landscape_bridge_cards(src_filenames: Iterable[str], dst_filename: str):
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            dst_filename,
            *src_filenames,
        ],
        check=True,
    )


tarot_landscape_dims = (827, 1417)  # seems rather portrait-y for "landscape"...


def do_tarot_cards(
    src_filenames: Iterable[str],
    basename: str,  # may include slashes, lolsob
    src_dims: Tuple[int, int] = (1, 1),
    *,
    filter=truly,
):
    wip_glob_name = f"wip/{basename}-*.png"
    retile(
        tarot_landscape_dims,
        load_subimages(tarot_landscape_dims, src_dims, src_filenames, filter=filter),
        (2, 2),
        wip_glob_name,
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "5.5inx9.5in",
            "--fit",
            "shrink",
            "-o",
            f"output/{basename}.pdf",
            *sorted(glob.glob(wip_glob_name)),
        ],
        check=True,
    )


def card_images(cards: Iterable) -> List[Image.Image]:
    return [c.load() for c in cards]


def retile_cards(
    images: Iterable[Image.Image], dst_dims, dst_glob: str, *, rotate_cw: bool = False
) -> None:
    """Lay equally-sized card images out in pages of dst_dims (cols, rows), writing
    dst_glob.  Stray images of another size are resized to match the first.
    Stale pages from earlier runs are removed first."""
    imgs = list(images)
    if rotate_cw:
        imgs = [i.rotate(-90, expand=True) for i in imgs]
    size = imgs[0].size
    for k, img in enumerate(imgs):
        if img.size != size:
            print(f"warning: resizing image {k} from {img.size} to {size}")
            imgs[k] = img.resize(size, resample=Image.LANCZOS)
    for stale in set(glob.glob(dst_glob)) | set(
        glob.glob(dst_glob.replace("-portrait", "-landscape"))
    ):
        os.remove(stale)
    retile(size, imgs, dst_dims, dst_glob)


def img2pdf_pages(imgsize: str, dst: str, pages: Iterable[str]) -> None:
    subprocess.run(
        ["img2pdf", "--pagesize", "letter", "--imgsize", imgsize, "--fit", "shrink",
         "-o", dst, *pages],
        check=True,
    )
