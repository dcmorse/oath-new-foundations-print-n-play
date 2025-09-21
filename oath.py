import argparse
from typing import Set
from retile import retile, image_middle_not_all_white
import glob
import subprocess
from denizens import is_denizen_to_print

tasks = set(
    [
        "banners",
        "chronicle-tasks",
        "edifices",
        "denizens",
        "visions",
        "foundation-board",
        "foundations",
    ]
)


def do_denizens():
    # 6731 x 5256
    retile(
        (673, 1051),
        (10, 5),
        "input/Denizens*.jpg",
        (4, 2),
        "wip/denizens-landscape-*.png",
        filter=is_denizen_to_print,
    )
    for landscape_file in glob.glob("wip/denizens-landscape*.png"):
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", "90", portrait_file], check=True
        )
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
            "output/denizens.pdf",
            *sorted(glob.glob("wip/denizens-portrait*.png")),
        ],
        check=True,
    )


def do_visions():
    print("do_visions stubbed")


def do_edifices():
    retile(
        (671, 1050),
        (5, 1),
        "input/Edifice*.jpg",
        (4, 2),
        "wip/edifices-landscape-*.png",
    )
    for landscape_file in glob.glob("wip/edifices-landscape*.png"):
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", "90", portrait_file], check=True
        )
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
            "output/edifices.pdf",
            *sorted(glob.glob("wip/edifices-portrait*.png")),
        ],
        check=True,
    )


def do_banners():
    retile(
        (1180, 1180),
        (1, 1),
        "input/Banner*.jpg",
        (2, 2),
        "wip/banners-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "6inx6in",
            "--fit",
            "shrink",
            "-o",
            "output/banners.pdf",
            *sorted(glob.glob("wip/banners-*.png")),
        ],
        check=True,
    )


def do_chronicle_tasks():
    ## input is 2480 x 2835
    # Assuming output is Arcs Tarot size: 4.75 x 2.75 inches
    subprocess.run("rm -f wip/chronicle-tasks-*.png", shell=True)
    retile(
        (826, 1417),
        (3, 2),
        "input/Chronicle Tasks*.jpg",
        (2, 2),
        "wip/chronicle-tasks-*.png",
        filter=image_middle_not_all_white,
    )
    if not glob.glob("wip/chronicle-tasks-*.png"):
        raise RuntimeError("no chronicle tasks generated")
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
            "output/chronicle-tasks.pdf",
            *sorted(glob.glob("wip/chronicle-tasks-*.png")),
        ],
        check=True,
    )


def do_foundations():
    # 1181 x 780, 2in x 0.88in?
    retile(
        (590, 260),  # (1180/2, 780/3),
        (2, 3),
        "input/Foundations *.jpg",
        (2, 10),
        "wip/foundations-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "4inx9in",
            "--fit",
            "shrink",
            "-o",
            "output/foundations.pdf",
            *sorted(glob.glob("wip/foundations-*.png")),
        ],
        check=True,
    )


def do_foundation_board():
    subprocess.run(
        [
            "convert",
            "input/Foundation Board.jpg",
            "-rotate",
            "90",
            "wip/foundation-board.png",
        ],
        check=True,
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx10in",
            "--fit",
            "shrink",
            "-o",
            "output/foundation-board.pdf",
            "wip/foundation-board.png",
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(
        prog="oath",
        description="convert oath assets into printable pdfs.",
        epilog="See the README.md for more info.",
    )
    parser.add_argument("--all", action="store_true", help="Enable all tasks")
    for task in tasks:
        parser.add_argument(
            f"--{task}", action="store_const", const=True, help=f"Enable {task} task"
        )
        parser.add_argument(
            f"--no-{task}",
            action="store_const",
            const=False,
            help=f"Disable {task} task",
            dest=task,
        )
    args0 = parser.parse_args()
    args1 = {
        task: (
            args0.all
            if (task_value := getattr(args0, task.replace("-", "_"))) is None
            else task_value
        )
        for task in tasks
    }
    for task, enabled in args1.items():
        if enabled:
            snake_task = task.replace("-", "_")
            globals()[f"do_{snake_task}"]()


if __name__ == "__main__":
    main()
