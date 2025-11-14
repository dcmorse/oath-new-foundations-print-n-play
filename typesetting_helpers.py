import glob
from typing import Iterable, Tuple
import subprocess
from retile import load_subimages, retile, truly


def landscape_to_portrait(src_filenames: Iterable[str], *, ccw: bool = False):
    print("landscape_to_portrait")
    rotation = "-90" if ccw else "90"
    for landscape_file in src_filenames:
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", rotation, portrait_file], check=True
        )


def portrait_to_landscape(src_filenames: Iterable[str], *, ccw: bool = False):
    print("portrait_to_landscape")
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
