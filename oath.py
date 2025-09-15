import argparse
from typing import Set
from retile import retile
import glob
import subprocess

tasks = set(["denizens", "visions", "edifices"])


def do_denizens():
    print("do_denizens stubbed")


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
    # Rotate all edifices images 90 degrees
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
    # args1 = {task: args0.all if getattr(args0, task) is None else getattr(args0, task) for task in tasks}
    args1 = {
        task: (
            args0.all if (task_value := getattr(args0, task)) is None else task_value
        )
        for task in tasks
    }
    for task, enabled in args1.items():
        if enabled:
            print(f"do_{task}()")
            globals()[f"do_{task}"]()


if __name__ == "__main__":
    main()
