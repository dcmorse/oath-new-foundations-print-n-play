from typing import Iterable, Set, Tuple
import argparse
import glob
import subprocess
import re
import filecmp
from denizens import is_denizen_to_print
from retile import (
    retile,
    image_middle_not_all_white,
    load_subimages,
    load_images_2up,
    truly,
)
from typesetting_helpers import landscape_to_portrait, portrait_to_landscape
from servant import (
    do_servant_commands,
    do_servant_display_board,
    do_servant_moods,
    do_servant_reference_cards,
)


new_foundation_tasks = set(
    [
        "banners",
        "banner-token",
        "chronicle-tasks",
        "edifices",
        "denizens",
        "legacies",
        "player-boards",
        "reference-cards",
        "relics",
        "rise-of-the-first-chancellor",
        "setup-cards",
        "sites",
        "visions",
    ]
)

servant_tasks: Set[str] = set(
    [
        "servant-commands",
        "servant-display-board",
        "servant-moods",
        "servant-reference-cards",
    ]
)

queen_of_shadows_tasks: Set[str] = set([])  # not yet implemented


denizen_portrait_dims = (673, 1051)


def do_denizens():
    # 6731 x 5256
    retile(
        denizen_portrait_dims,
        load_subimages(
            denizen_portrait_dims,
            (10, 5),
            sorted(glob.glob("input/Denizens*.jpg")),
            numpy_filter=is_denizen_to_print,
        ),
        (4, 2),
        "wip/denizens-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/denizens-portrait-*.png"))
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
            *sorted(glob.glob("wip/denizens-landscape*.png")),
        ],
        check=True,
    )


ediface_portrait_dims = (671, 1050)  # recall that denizen_portrait_dims = (673, 1051)


def do_edifices():
    retile(
        ediface_portrait_dims,
        load_images_2up(
            ediface_portrait_dims,
            (5, 1),
            (
                e
                for e in sorted(glob.glob("input/Edifice*.jpg"))
                if not re.search(r"ruined", e, re.IGNORECASE)
            ),
            sorted(glob.glob("input/Edifice*Ruined.jpg")),
        ),
        (4, 2),
        "wip/edifices-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/edifices-portrait-*.png"))
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
            *sorted(glob.glob("wip/edifices-landscape*.png")),
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
    banner_dims = (1180, 1180)
    bs = []
    retile(
        banner_dims,
        load_subimages(
            banner_dims,
            (1, 1),
            (
                b
                for b in glob.glob("input/Banner*.jpg")
                if not re.search(r"banner.token", b, re.IGNORECASE)
            ),
        ),
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


tarot_landscape_dims = (827, 1417)


def do_tarot_cards(
    src_filenames: Iterable[str],
    basename: str,
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


def do_chronicle_tasks():
    retile(
        tarot_landscape_dims,
        load_images_2up(
            tarot_landscape_dims,
            (3, 2),
            ["input/Chronicle Tasks 1.jpg"],
            ["input/Chronicle Tasks 2.jpg"],
            filter=image_middle_not_all_white,
        ),
        (2, 2),
        "wip/chronicle-tasks-*.png",
    )
    subprocess.run(  # shared DNA with do_tarot_cards...
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "5.5inx9.5in",
            "--fit",
            "shrink",
            "-o",
            f"output/chronicle-tasks.pdf",
            *sorted(glob.glob("wip/chronicle-tasks-*.png")),
        ],
        check=True,
    )


def do_setup_cards():
    retile(
        denizen_portrait_dims,
        load_images_2up(
            denizen_portrait_dims,
            (5, 3),
            ["input/Setup Cards F.jpg"],
            ["input/Setup Cards B.jpg"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        "wip/setup-cards-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/setup-cards-portrait-*.png"))
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
            "output/setup-cards.pdf",
            *sorted(glob.glob("wip/setup-cards-landscape*.png")),
        ],
        check=True,
    )


def do_legacies():
    # 6307 x 4039 6x6 (6x5 used)
    m, n = denizen_portrait_dims
    src_dims = (n, m)
    retile(
        src_dims,
        load_subimages(
            src_dims,
            (6, 6),
            sorted(glob.glob("input/Legacies*.jpg")),
            filter=image_middle_not_all_white,
        ),
        (2, 4),
        "wip/legacies-*.png",
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
    src_dims = (2350, 1122)
    retile(
        src_dims,
        load_images_2up(
            src_dims,
            (2, 4),
            ["input/Player Boards 1.jpg"],
            ["input/Player Boards 2.jpg"],
        ),
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


relic_dims = (673, 673)  # Grand Scepter has different dimensions


def do_relics():
    # 6731 x 3365 (plus other rows beneath)
    """including the grand scepter"""
    retile(
        relic_dims,
        load_subimages(relic_dims, (10, 5), sorted(glob.glob("input/Relics*.jpg"))),
        (3, 4),
        "wip/relics-*.png",
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
    retile(
        (650, 650),
        load_subimages(
            relic_dims, (1, 1), glob.glob("input/Relic The Grand Scepter *.jpg")
        ),
        (2, 1),
        "wip/relic-grand-scepter-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "2.25inx4.5in",
            "--fit",
            "shrink",
            "-o",
            "output/relic-grand-scepter.pdf",
            *glob.glob("wip/relic-grand-scepter-*.png"),
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
    site_dims = (1358, 1051)
    retile(
        site_dims,
        load_subimages(
            site_dims,
            (1, 1),
            sorted(
                (
                    s
                    for s in glob.glob("input/Site *.jpg")
                    if not re.search(r"site.*reference", s, re.IGNORECASE)
                )
            ),
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
        "--servant",
        action="store_true",
        help="Enable all Servant tasks",
    )
    parser.add_argument(
        "--queen-of-shadows",
        action="store_true",
        help="Enable all Queen of Shadows tasks",
    )
    for game_tasks in [new_foundation_tasks, servant_tasks, queen_of_shadows_tasks]:
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
        (servant_tasks, args0["servant"]),
        (queen_of_shadows_tasks, args0["queen_of_shadows"]),
    ]:
        for task in tasks:
            args1[task.replace("-", "_")] = bool(game_on)
    # set fine-grained per-component switches
    for task in new_foundation_tasks.union(servant_tasks, queen_of_shadows_tasks):
        if (b := args0.get(task.replace("-", "_"))) is not None:
            args1[task.replace("-", "_")] = b
    # run enabled tasks
    for task, enabled in args1.items():
        if enabled:
            snake_task = task.replace("-", "_")
            print(f"# {task}")
            globals()[f"do_{snake_task}"]()


if __name__ == "__main__":
    main()
