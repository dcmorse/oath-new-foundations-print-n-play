#!/usr/bin/env python
from denizens import is_unchanged_denizen
from typing import Iterable, Set, Tuple
import argparse
import glob
import subprocess
import re
import math
from denizens import is_new_denizen, is_unchanged_denizen
from retile import (
    retile,
    image_middle_not_all_white,
    load_subimages,
    load_images_2up,
    filter_by_idx,
)
from typesetting_helpers import (
    do_tarot_cards,
    tarot_landscape_dims,
    landscape_to_portrait,
    portrait_to_landscape,
    typeset_landscape_bridge_cards,
)
from servant import (
    do_servant_nf_commands,
    do_servant_nf_display_board,
    do_servant_nf_moods,
    do_servant_nf_reference_cards,
    do_servant_base_commands,
    do_servant_base_display_board,
    do_servant_base_moods,
    do_servant_base_reference_cards,
)
from queen_of_shadows import (
    do_qos_altars,
    do_qos_chronicle_tasks,
    do_qos_darkness_cards,
    do_qos_darkness_track,
    do_qos_player_board,
    do_qos_priority_tokens,
    do_qos_prisoner_tiles_helper,
    do_qos_ruse_token,
    do_qos_shadow_cards,
    do_qos_title_cards,
)


new_foundation_tasks = set(
    [
        "banners",
        "banner-token",
        "chronicle-tasks",
        "edifices",
        "first-player-marker",
        "imperial-reliquary",
        "legacies",
        "legacy-backs",
        "new-denizens",
        "oathkeeper-goals",
        "oathkeeper-title",
        "player-boards",
        "reference-cards",
        "relics",
        # "rise-of-the-first-chancellor", # replaced by setup cards:
        "setup-cards",
        "sites",
        "usurper-limiter",
        "visions",
    ]
)


base_tasks = set(["unchanged-denizens"])

servant_tasks: Set[str] = set(
    [
        "servant-commands",
        "servant-display-board",
        "servant-moods",
        "servant-reference-cards",
    ]
)

servant_nf_tasks: Set[str] = {
    task.replace("servant-", "servant-nf-") for task in servant_tasks
}

servant_base_tasks: Set[str] = {
    task.replace("servant-", "servant-base-") for task in servant_tasks
}

queen_of_shadows_tasks: Set[str] = set(
    [
        "qos-altars",
        "qos-chronicle-tasks",
        "qos-darkness-cards",
        "qos-darkness-track",
        "qos-shadow-cards",
        "qos-title-cards",
        "qos-player-board",
        "qos-priority-tokens",
        "qos-prisoner-tiles",
        "qos-prisoner-tiles-light-mode",
        "qos-ruse-token",
    ]
)


def do_qos_prisoner_tiles():
    do_qos_prisoner_tiles_helper(light_mode=False)


def do_qos_prisoner_tiles_light_mode():
    do_qos_prisoner_tiles_helper(light_mode=True)


denizen_portrait_dims = (673, 1051)


def do_new_denizens():
    # 6731 x 5256
    retile(
        denizen_portrait_dims,
        load_subimages(
            denizen_portrait_dims,
            (10, 5),
            sorted(glob.glob("input/Denizens*.jpg")),
            filter=is_new_denizen,
        ),
        (4, 2),
        "wip/new-denizens-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/new-denizens-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/new-denizens-landscape*.png")), "output/denizens.pdf"
    )


def do_unchanged_denizens():
    # 6731 x 5256
    retile(
        denizen_portrait_dims,
        load_subimages(
            denizen_portrait_dims,
            (10, 5),
            sorted(glob.glob("input/Denizens*.jpg")),
            filter=is_unchanged_denizen,
        ),
        (4, 2),
        "wip/base/unchanged-denizens-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/base/unchanged-denizens-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/base/unchanged-denizens-landscape*.png")),
        "output/base/unchanged-denizens.pdf",
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
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/edifices-landscape*.png")), "output/edifices.pdf"
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
        # {0, 1, 2, 3, 8},
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


def do_first_player_marker():
    # src_dims = (602, 829)
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "3inx2in",
            "--fit",
            "shrink",
            "-o",
            "output/first-player-marker.pdf",
            "input/first-player-marker.jpg",
        ]
    )


def do_imperial_reliquary():
    imperial_reliquary_dims = (661, 661)
    retile(
        imperial_reliquary_dims,
        load_images_2up(
            imperial_reliquary_dims,
            (1, 1),
            ["input/imperial-reliquary-front.jpg"],
            ["input/imperial-reliquary-back.jpg"],
        ),
        (2, 1),
        "wip/imperial-reliquary-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "5inx2.5in",
            "--fit",
            "shrink",
            "-o",
            "output/imperial-reliquary.pdf",
            *sorted(glob.glob("wip/imperial-reliquary-*.png")),
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
        # {4, 5},
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


legacy_src_size = (6, 6)

def do_legacies():
    # 6307 x 4039 6x6
    m, n = denizen_portrait_dims
    src_dims = (n, m)
    retile(
        src_dims,
        load_subimages(
            src_dims,
            legacy_src_size,
            sorted(glob.glob("input/Legacies*.jpg")),
            filter=image_middle_not_all_white,
        ),
        # {0, 10, 16},
        # {1, 5, 15, 16, 20, 23},
        (2, 4),
        "wip/legacies-portrait-*.png",
    )
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/legacies-portrait*.png")), "output/legacies.pdf"
    )


def do_legacy_backs():
    m, n = denizen_portrait_dims
    src_dims = (n, m)
    retile(
        src_dims,
        load_subimages(
            src_dims,
            (1, 1),
            math.prod(legacy_src_size) * ["input/legacy-back.jpg"],
        ),
        (2, 4),
        "wip/legacy-backs-portrait-*.png",
    )
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/legacy-backs-portrait*.png")), "output/legacy-backs.pdf"
    )


def do_oathkeeper_goals():
    src_dims = (673, 898)
    retile(
        src_dims,
        load_subimages(
            src_dims,
            (1, 1),
            glob.glob("input/oathkeeper-of-*.jpg"),
        ),
        dst_dims=(2, 2),
        dst_glob="wip/oathkeeper-goals-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "5inx6in",
            "--fit",
            "shrink",
            "-o",
            "output/oathkeeper-goals.pdf",
            *sorted(glob.glob("wip/oathkeeper-goals-*.png")),
        ]
    )


def do_oathkeeper_title():
    src_dims = (602, 829)
    retile(
        src_dims,
        load_subimages(
            src_dims,
            (1, 1),
            glob.glob("input/*per-title.jpg"),  # {oathkee,usur}per-title
        ),
        dst_dims=(2, 1),
        dst_glob="wip/oathkeeper-title-*.png",
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "4inx3in",
            "--fit",
            "shrink",
            "-o",
            "output/oathkeeper-title.pdf",
            *sorted(glob.glob("wip/oathkeeper-title-*.png")),
        ]
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
                "reference-actions.jpg",
                "reference-campaign-recover-challenge.jpg",
                "reference-minor-and-card-powers.jpg",
                "reference-site.jpg",
            ]
        ],
        "reference-cards",
    )


relic_dims = (673, 673)


def id(x, *args):
    return x


def do_relics():
    # 6731 x 3365 (plus other rows beneath)
    """including the grand scepter"""
    retile(
        relic_dims,
        id(
            load_subimages(relic_dims, (10, 5), sorted(glob.glob("input/Relics*.jpg"))),
            # {2, 5, 7, 10, 20, 24, 27, 28, 29, 31, 34, 45, 46, 49},
        ),
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
        relic_dims,
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
            "4.5inx3.5in",
            "--fit",
            "shrink",
            "-o",
            "output/relic-grand-scepter.pdf",
            *glob.glob("wip/relic-grand-scepter-*.png"),
        ],
        check=True,
    )

# replaced by setup cards:
# def do_rise_of_the_first_chancellor():
#     do_tarot_cards(
#         src_filenames=sorted(glob.glob("input/RotFC *.jpg")),
#         basename="rise-of-the-first-chancellor",
#     )


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


def do_usurper_limiter():
    # This log message is expected and I guess doing work for us:
    # "Image contains an alpha channel. Computing a separate soft mask (/SMask) image to store transparency in PDF."
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "1inx1in",
            "--fit",
            "shrink",
            "-o",
            "output/usurper-limiter.pdf",
            "input/usurper-limiter.png",
        ],
        check=True,
    )


def do_visions():
    typeset_landscape_bridge_cards(["input/Visions.jpg"], "output/visions.pdf")


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
        "--servant-nf",
        action="store_true",
        help="Enable all Servant tasks - new foundations variant",
    )
    parser.add_argument(
        "--servant-base",
        action="store_true",
        help="Enable all Servant tasks - base oath variant",
    )
    parser.add_argument(
        "--queen-of-shadows",
        action="store_true",
        help="Enable all Queen of Shadows tasks",
    )
    parser.add_argument(
        "--base",
        action="store_true",
        help="Enable all Base Game tasks - note that the base game is not completely printable",
    )
    for game_tasks in [
        new_foundation_tasks,
        servant_nf_tasks,
        servant_base_tasks,
        queen_of_shadows_tasks,
        base_tasks,
    ]:
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
        (servant_nf_tasks, args0["servant_nf"]),
        (servant_base_tasks, args0["servant_base"]),
        (queen_of_shadows_tasks, args0["queen_of_shadows"]),
        (base_tasks, args0["base"]),
    ]:
        for task in tasks:
            args1[task.replace("-", "_")] = bool(game_on)
    # set fine-grained per-component switches
    for task in new_foundation_tasks.union(
        servant_base_tasks, servant_nf_tasks, queen_of_shadows_tasks, base_tasks
    ):
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
