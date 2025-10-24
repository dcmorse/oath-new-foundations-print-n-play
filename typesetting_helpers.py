from typing import Iterable
import subprocess


def landscape_to_portrait(src_filenames: Iterable[str]):
    print("landscape_to_portrait")
    for landscape_file in src_filenames:
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", "90", portrait_file], check=True
        )


def portrait_to_landscape(src_filenames: Iterable[str]):
    print("portrait_to_landscape")
    for portrait_file in src_filenames:
        landscape_file = portrait_file.replace("-portrait", "-landscape")
        subprocess.run(
            ["convert", portrait_file, "-rotate", "-90", landscape_file], check=True
        )
