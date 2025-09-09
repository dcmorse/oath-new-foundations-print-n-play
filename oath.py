import argparse
from typing import Set

tasks = set(["denizens", "visions"])


def do_denizens():
    print("do_denizens stubbed")


def do_visions():
    print("do_visions stubbed")


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
