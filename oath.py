from typing import Iterable, Set, Tuple
import argparse
import glob
import subprocess
import re
import filecmp
from denizens import is_denizen_to_print
from retile import retile, image_middle_not_all_white, truly


new_foundation_tasks = set(
    [
        "banners",
        "banner-token",
        "chronicle-tasks",
        "edifices",
        "denizens",
        "foundation-board",
        "foundations",
        "legacies",
        "player-boards",
        "reference-cards",
        "relics",
        "rise-of-the-first-chancellor",
        "sites",
        "visions",
    ]
)

clockwork_adversary_tasks: Set[str] = set(["clockwork1"])


def do_clockwork1():
    print("Clockwork1 not yet implemented")


def landscape_to_portrait(src_filenames: Iterable[str]):
    print("landscape_to_portrait")
    for landscape_file in src_filenames:
        portrait_file = landscape_file.replace("-landscape", "-portrait")
        subprocess.run(
            ["convert", landscape_file, "-rotate", "90", portrait_file], check=True
        )


def do_denizens():
    # 6731 x 5256
    retile(
        (673, 1051),
        (10, 5),
        sorted(glob.glob("input/Denizens*.jpg")),
        (4, 2),
        "wip/denizens-landscape-*.png",
        filter=is_denizen_to_print,
    )
    landscape_to_portrait(glob.glob("wip/denizens-landscape-*.png"))
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


def do_edifices():
    retile(
        (671, 1050),
        (5, 1),
        sorted(glob.glob("input/Edifice*.jpg")),
        (4, 2),
        "wip/edifices-landscape-*.png",
    )
    landscape_to_portrait(glob.glob("wip/edifices-landscape-*.png"))
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


def do_banner_token():
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "4.25inx1.5in",
            "--fit",
            "shrink",
            "-o",
            "output/banner-token.pdf",
            "input/Banner token.jpg",
        ],
        check=True,
    )


def do_banners():
    bs = [
        b
        for b in glob.glob("input/Banner*.jpg")
        if not re.search(r"banner.token", b, re.IGNORECASE)
    ]
    retile(
        (1180, 1180),
        (1, 1),
        sorted(bs),
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


def do_tarot_cards(
    src_filenames: Iterable[str],
    basename: str,
    src_dims: Tuple[int, int] = (1, 1),
    filter=truly,
):
    wip_glob_name = f"wip/{basename}-*.png"
    retile(
        (827, 1417),
        src_dims,
        src_filenames,
        (2, 2),
        wip_glob_name,
        filter=filter,
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


def do_chronicle_tasks():
    do_tarot_cards(
        src_filenames=sorted(glob.glob("input/Chronicle Tasks*.jpg")),
        src_dims=(3, 2),
        basename="chronicle-tasks",
        filter=image_middle_not_all_white,
    )


def do_foundations():
    # 1181 x 780, 2in x 0.88in?
    retile(
        (590, 260),  # (1180/2, 780/3),
        (2, 3),
        sorted(glob.glob("input/Foundations *.jpg")),
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


def do_legacies():
    # 6307 x 4039 6x6 (6x5 used)
    # 3637 x 3956 mini-euro 44mm x 68mm (1.73in x 2.68in)
    retile(
        (1051, 673),
        (6, 5),
        sorted(glob.glob("input/Legacies*.jpg")),
        (2, 4),
        "wip/legacies-*.png",
        filter=image_middle_not_all_white,
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "174mmx204mm",
            "--fit",
            "shrink",
            "-o",
            "output/legacies.pdf",
            *sorted(glob.glob("wip/legacies-*.png")),
        ],
        check=True,
    )


def do_player_boards():
    # 4701 x 4488
    # A vision is about is 646 x 1029 at this scale and also 2.25" x 3.5"
    retile(
        (2350, 1122),
        (2, 4),
        sorted(glob.glob("input/Player Boards *.jpg")),
        (1, 2),
        "wip/player-boards-landscape-*.png",
    )
    landscape_to_portrait(glob.glob("wip/player-boards-landscape-*.png"))
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "7.63inx8.18in",
            "--fit",
            "shrink",
            "-o",
            "output/player-boards.pdf",
            *sorted(glob.glob("wip/player-boards-portrait-*.png")),
        ],
        check=True,
    )


def do_reference_cards():
    do_tarot_cards(
        [
            f"input/{fn}"
            for fn in [
                "Reference Actions.jpg",
                "Reference Card Restrictions and Powers.jpg",
                "Reference Misc Actions.jpg",
                "Site 1 Reference.jpg",
            ]
        ],
        "reference-cards",
    )


def do_relics():
    # 6731 x 3365 (plus other rows beneath)
    """including the grand scepter"""
    retile(
        (673, 673),
        (10, 5),
        sorted(glob.glob("input/Relics*.jpg")),
        (3, 4),
        "wip/relics-*.png",
        # TODO: filter out removed cards
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "6.75inx9in",
            "--fit",
            "shrink",
            "-o",
            "output/relics.pdf",
            *sorted(glob.glob("wip/relics-*.png")),
        ],
        check=True,
    )
    if not filecmp.cmp(
        "input/Relic The Grand Scepter 1.jpg",
        "input/Relic The Grand Scepter 2.jpg",
        shallow=False,
    ):
        raise ValueError("The Grand Scepter images differ; please check them.")
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "2.25inx2.25in",
            "--fit",
            "shrink",
            "-o",
            "output/relic-grand-scepter.pdf",
            "input/Relic The Grand Scepter 1.jpg",
        ],
        check=True,
    )


def do_rise_of_the_first_chancellor():
    do_tarot_cards(
        src_filenames=sorted(glob.glob("input/RotFC *.jpg")),
        basename="rise-of-the-first-chancellor",
    )


def do_sites():
    # 1358 x 1051
    # 6731 x 3365 (plus other rows beneath)
    retile(
        (1358, 1051),
        (1, 1),
        sorted(
            [
                s
                for s in glob.glob("input/Site *.jpg")
                if not re.search(r"site.*reference", s, re.IGNORECASE)
            ]
        ),
        (2, 2),
        "wip/sites-landscape-*.png",
    )
    landscape_to_portrait(glob.glob("wip/sites-landscape-*.png"))
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
            "output/sites.pdf",
            *sorted(glob.glob("wip/sites-portrait*.png")),
        ],
        check=True,
    )


def do_visions():
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "7.25inx7in",
            "--fit",
            "shrink",
            "-o",
            "output/visions.pdf",
            glob.glob("input/Vis*ons.jpg")[0],  # spelled 'Visons' at time of writing
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(
        prog="oath",
        description="convert oath assets into printable pdfs.",
        epilog="See the README.md for more info.",
    )
    parser.add_argument(
        "--new-foundations",
        action="store_true",
        help="Enable all New Foundations tasks",
    )
    parser.add_argument(
        "--clockwork-adversaries",
        action="store_true",
        help="Enable all Clockwork Adversaries tasks",
    )
    for game_tasks in [new_foundation_tasks, clockwork_adversary_tasks]:
        for task in game_tasks:
            parser.add_argument(
                f"--{task}",
                action="store_const",
                const=True,
                help=f"Enable {task} task",
            )
            parser.add_argument(
                f"--no-{task}",
                action="store_const",
                const=False,
                help=f"Disable {task} task",
                dest=task,
            )
    args0 = vars(parser.parse_args())
    args1 = {}
    # default for the big game command line switches --new-foundations, --clockwork-adversaries
    for tasks, game_on in [
        (new_foundation_tasks, args0["new_foundations"]),
        (clockwork_adversary_tasks, args0["clockwork_adversaries"]),
    ]:
        for task in tasks:
            args1[task.replace("-", "_")] = bool(game_on)
    # set fine-grained per-component switches
    for task in new_foundation_tasks.union(clockwork_adversary_tasks):
        if (b := args0.get(task.replace("-", "_"))) is not None:
            args1[task.replace("-", "_")] = b
    # run enabled tasks
    for task, enabled in args1.items():
        if enabled:
            snake_task = task.replace("-", "_")
            globals()[f"do_{snake_task}"]()


if __name__ == "__main__":
    main()
