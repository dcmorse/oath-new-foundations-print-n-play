#!/usr/bin/env python

from PIL import Image
import bgs_cards
from typing import Iterable, List, Set
import os
import argparse
import glob
import subprocess
import re
import math
from retile import (
    tile,
    image_middle_not_all_white,
    load_subimages,
    load_images_2up,
    filter_by_idx,
    filter_by_idx_not,
)
from typesetting_helpers import (
    card_images,
    img2pdf_pages,
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


def id(x, *args):
    """Identity function"""
    return x


def _card_order(c: "bgs_cards.Card"):
    """Sort key: suit (if any), then the card number embedded in the id."""
    m = re.search(r"\d+", c.id)
    return (bgs_cards.SUITS.index(c.suit) if c.suit else -1, int(m.group()) if m else 0, c.id)


new_foundation_tasks = set(
    [
        "banners",
        "banner-token",
        "chronicle-tasks",
        # "dormant-legacy-backs", # homebrew idea, not really a pnp thing
        "edifices",
        "first-player-marker",
        "imperial-reliquary",
        "legacies",
        "legacy-backs",
        "new-denizens",
        "new-denizen-backs",
        "oathkeeper-goals",
        "oathkeeper-goal-backs",
        "oathkeeper-title",
        "player-boards",
        "reference-cards",
        "relic-backs",
        "relics",
        "relic-grand-scepter",
        # "rise-of-the-first-chancellor", # made obsolete by setup cards
        "setup-cards",
        "sites",
        "site-backs",
        "usurper-limiter",
        "visions",
        "vision-backs",
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


denizen_portrait_dims = (673, 1051)  # TTS-rip card size; still used for backs


def do_new_denizens():
    tile(
        card_images(sorted(bgs_cards.new_foundations_denizens(), key=_card_order)),
        (4, 2),
        "wip/new-denizens-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/new-denizens-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/new-denizens-landscape*.png")), "output/denizens.pdf"
    )


def do_new_denizen_backs():
    dims = (337, 526)
    tile(
        60 * [Image.open("input/denizen-back.jpg")],
        (4, 2),
        "wip/new-denizen-backs-portrait-*.png",
        size=dims,
    ),
    portrait_to_landscape(glob.glob("wip/new-denizen-backs-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/new-denizen-backs-landscape*.png")),
        "output/denizen-backs.pdf",
    )


def do_unchanged_denizens():
    tile(
        card_images(sorted(bgs_cards.unchanged_denizens(), key=_card_order)),
        (4, 2),
        "wip/base/unchanged-denizens-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/base/unchanged-denizens-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/base/unchanged-denizens-landscape*.png")),
        "output/base/unchanged-denizens.pdf",
    )


def do_edifices():
    # intact and ruined side by side, so they print as front/back pairs
    imgs = []
    for intact, ruined in bgs_cards.edifice_pairs():
        imgs += [intact.load(), ruined.load()]
    tile(imgs, (4, 2), "wip/edifices-portrait-*.png")
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
    tile(
        card_images(
            # Darkest Secret banners on the top row, People's Favor below
            sorted(
                bgs_cards.cards_tagged("Banner"),
                key=lambda c: ("Darkest Secret" not in c.name, c.id),
            )
        ),
        (2, 2),
        "wip/banners-*.png",
    )
    img2pdf_pages("6inx6in", "output/banners.pdf", sorted(glob.glob("wip/banners-*.png")))


def do_chronicle_tasks():
    # Five double-sided cards. BGS has all five fronts and the text backs of the Sun and
    # the Throne; the art-only backs of the World, Beacon and Stars come from the TTS rip
    # (tiles 2-4 of the 3x2 back sheet).
    fronts = [c for c in sorted(bgs_cards.cards_tagged("Chronicle"), key=lambda c: c.id)
              if c.flip_side is None or c.id.endswith("a-NF")]
    size = fronts[0].load().size
    sheet = Image.open("input/Chronicle Tasks 2.jpg")
    tw, th = sheet.width // 3, sheet.height // 2
    tts_backs = [
        sheet.crop((i * tw, j * th, (i + 1) * tw, (j + 1) * th)).resize(size, Image.LANCZOS)
        for j in range(2) for i in range(3)
    ]
    art_backs = iter(tts_backs[2:5])
    imgs = []
    for c in fronts:
        imgs += [c.load(), bgs_cards.by_id()[c.flip_side].load() if c.flip_side else next(art_backs)]
    tile(imgs, (2, 2), "wip/chronicle-tasks-*.png")
    img2pdf_pages("5.5inx9.5in", "output/chronicle-tasks.pdf",
                  sorted(glob.glob("wip/chronicle-tasks-*.png")))


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
    tile(
        load_images_2up(
            imperial_reliquary_dims,
            (1, 1),
            ["input/imperial-reliquary-front.jpg"],
            ["input/imperial-reliquary-back.jpg"],
        ),
        (2, 1),
        "wip/imperial-reliquary-*.png",
        size=imperial_reliquary_dims,
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
    # Two-sided cards print as front/back pairs. The few one-sided cards share a
    # generic art back that BGS doesn't publish, so it comes from the TTS rip.
    fronts = [c for c in sorted(bgs_cards.cards_tagged("Setup"), key=lambda c: c.id)
              if c.flip_side is None or c.id.endswith("a-NF")]
    size = fronts[0].load().size
    sheet = Image.open("input/Setup Cards B.jpg")
    tw, th = sheet.width // 5, sheet.height // 3
    art_back = sheet.crop((0, 0, tw, th)).resize(size, resample=Image.LANCZOS)
    imgs = []
    for c in fronts:
        imgs += [c.load(), bgs_cards.by_id()[c.flip_side].load() if c.flip_side else art_back]
    tile(imgs, (4, 2), "wip/setup-cards-portrait-*.png")
    portrait_to_landscape(glob.glob("wip/setup-cards-portrait-*.png"))
    img2pdf_pages("7inx9in", "output/setup-cards.pdf",
                  sorted(glob.glob("wip/setup-cards-landscape*.png")))


legacy_src_size = (6, 6)


def do_legacies():
    tile(
        card_images(sorted(bgs_cards.cards_tagged("Legacy"), key=lambda c: c.id)),
        (2, 4),
        "wip/legacies-portrait-*.png",
    )
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/legacies-portrait*.png")), "output/legacies.pdf"
    )


def do_legacy_backs():
    m, n = denizen_portrait_dims
    src_dims = (n, m)
    tile(
        load_subimages(
            src_dims,
            (1, 1),
            math.prod(legacy_src_size) * ["input/legacy-back.jpg"],
        ),
        (2, 4),
        "wip/legacy-backs-portrait-*.png",
        size=src_dims,
    )
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/legacy-backs-portrait*.png")), "output/legacy-backs.pdf"
    )


# Not part of any product - just a homebrew idea.
# def do_dormant_legacy_backs():
#     m, n = denizen_portrait_dims
#     src_dims = (n, m)
#     tile(
#         src_dims,
#         load_subimages(
#             src_dims,
#             (1, 1),
#             8 * ["input/dormant-legacy-back.png"],
#         ),
#         (2, 4),
#         "wip/dormant-legacy-backs-portrait-*.png",
#     )
#     typeset_landscape_bridge_cards(
#         sorted(glob.glob("wip/dormant-legacy-backs-portrait*.png")),
#         "output/dormant-legacy-backs.pdf",
#     )


def do_oathkeeper_goals():
    tile(
        card_images(sorted(bgs_cards.cards_tagged("Oathkeeper Goal"), key=lambda c: c.id)),
        (2, 2),
        "wip/oathkeeper-goals-*.png",
    )
    img2pdf_pages("5inx6in", "output/oathkeeper-goals.pdf",
                  sorted(glob.glob("wip/oathkeeper-goals-*.png")))


def do_oathkeeper_goal_backs():
    src_dims = (673, 898)
    tile(
        load_subimages(
            src_dims,
            (1, 1),
            ["input/oathkeeper-goal-back.jpg"] * 4,
        ),
        (2, 2),
        "wip/oathkeeper-goal-backs-*.png",
        size=src_dims,
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
            "output/oathkeeper-goal-backs.pdf",
            *sorted(glob.glob("wip/oathkeeper-goal-backs-*.png")),
        ]
    )


def do_oathkeeper_title():
    src_dims = (602, 829)
    tile(
        load_subimages(
            src_dims,
            (1, 1),
            glob.glob("input/*per-title.jpg"),  # {oathkee,usur}per-title
        ),
        (2, 1),
        "wip/oathkeeper-title-*.png",
        size=src_dims,
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
    tile(
        id(
            load_images_2up(
                src_dims,
                (2, 4),
                ["input/Player Boards 1.jpg"],
                ["input/Player Boards 2.jpg"],
            ),
            # {0, 3, 5, 7, 9, 11, 13, 15}, # indexes of player boards changed on Feb 17 2026
        ),
        (1, 2),
        "wip/player-boards-landscape-*.png",
        size=src_dims,
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


def do_relic_backs():
    huge_img = Image.open("input/relic-back.jpg")
    if huge_img.width < 1000 or huge_img.height < 1000:
        raise ValueError(
            "Oh, someone downsampled the relic back to be a sane resolution. We should adjust this code."
        )
    img = huge_img.resize(
        (huge_img.width // 2, huge_img.height // 2), resample=Image.BOX
    )
    tile(
        47 * [img],
        (3, 4),
        "wip/relic-backs-*.png",
        size=(img.width, img.height),
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
            "output/relic-backs.pdf",
            *sorted(glob.glob("wip/relic-backs-*.png")),
        ],
        check=True,
    )


GRAND_SCEPTER_ID = "OATH-GrandScepter-NF"


def do_relics():
    relics = [c for c in sorted(bgs_cards.cards_tagged("Relic"), key=lambda c: c.id)
              if c.id != GRAND_SCEPTER_ID]
    tile(card_images(relics), (3, 4), "wip/relics-*.png")
    img2pdf_pages("6.75inx9in", "output/relics.pdf", sorted(glob.glob("wip/relics-*.png")))


def do_relic_grand_scepter():
    # BGS only publishes the face. The art-only back ("cannot be removed from play")
    # is from the TTS rip.
    front = bgs_cards.by_id()[GRAND_SCEPTER_ID].load()
    back = Image.open("input/Relic The Grand Scepter 1.jpg").convert("RGB")
    tile([front, back], (2, 1), "wip/relic-grand-scepter-*.png")
    img2pdf_pages("4.5inx3.5in", "output/relic-grand-scepter.pdf",
                  sorted(glob.glob("wip/relic-grand-scepter-*.png")))


# replaced by setup cards:
# def do_rise_of_the_first_chancellor():
#     do_tarot_cards(
#         src_filenames=sorted(glob.glob("input/RotFC *.jpg")),
#         basename="rise-of-the-first-chancellor",
#     )


def do_sites():
    tile(
        card_images(sorted(bgs_cards.cards_tagged("Site"), key=lambda c: c.id)),
        (2, 2),
        "wip/sites-landscape-*.png",
    )
    landscape_to_portrait(glob.glob("wip/sites-landscape-*.png"))
    img2pdf_pages("7inx9in", "output/sites.pdf", sorted(glob.glob("wip/sites-portrait*.png")))


def do_site_backs():
    site_back_dims = (1313, 1016)
    back = Image.open("input/site-back.jpg")
    for nup in [1, 4]:
        tile(
            nup * [back],
            (2, 2),
            f"wip/site-backs-{nup}up-landscape-*.png",
            size=site_back_dims,
        )
    landscape_to_portrait(glob.glob("wip/site-backs-1up-landscape-*.png"))
    landscape_to_portrait(glob.glob("wip/site-backs-4up-landscape-*.png"))

    def img_to_pdf(nup):
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
                f"output/site-backs-{nup}up.pdf",
                *sorted(glob.glob(f"wip/site-backs-{nup}up-portrait*.png")),
            ],
            check=True,
        )

    img_to_pdf(1)
    img_to_pdf(4)


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
    # BGS stores visions landscape ("rotated"); the physical card is portrait with
    # the text running top-to-bottom, so rotate clockwise.
    tile(
        card_images(sorted(bgs_cards.cards_tagged("Vision"), key=lambda c: c.id)),
        (3, 2),
        "wip/visions-*.png",
        rotate_cw=True,
    )
    img2pdf_pages("7inx9in", "output/visions.pdf", sorted(glob.glob("wip/visions-*.png")))


def do_vision_backs():
    dims = (651, 1016)
    tile(
        5 * [Image.open("input/vision-back.jpg")],
        (4, 2),
        "wip/vision-backs-portrait-*.png",
        size=dims,
    ),
    portrait_to_landscape(glob.glob("wip/vision-backs-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/vision-backs-landscape*.png")),
        "output/vision-backs.pdf",
    )
    # typeset_landscape_bridge_cards(
    #     ["input/vision-backs.jpg"] * 5, "output/vision-backs.pdf"
    # )


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
    if not any(args1.values()):
        parser.print_help()
        parser.exit(1, "\nNo tasks enabled - pick a game switch (e.g. --new-foundations) or a task.\n")
    # run enabled tasks
    for task, enabled in args1.items():
        if enabled:
            snake_task = task.replace("-", "_")
            print(f"# {task}")
            globals()[f"do_{snake_task}"]()


if __name__ == "__main__":
    main()
