import glob
import subprocess
from retile import load_images_2up, load_subimages, retile, image_middle_not_all_white
from typesetting_helpers import (
    do_tarot_cards,
    landscape_to_portrait,
    tarot_landscape_dims,
    portrait_to_landscape,
    typeset_landscape_bridge_cards,
)
from PIL import Image, ImageOps


def do_qos_priority_tokens():
    token_dims = (355, 355)
    retile(
        token_dims,
        load_subimages(
            token_dims,
            (1, 1),
            sorted(glob.glob("input/queen-of-shadows/priority-token-*.png")),
        ),
        (4, 2),
        "wip/queen-of-shadows/priority-tokens-light-*.png",
    )
    for light_path in glob.glob("wip/queen-of-shadows/priority-tokens-light-*.png"):
        img = Image.open(light_path).convert("RGB")
        inverted = ImageOps.invert(img)
        dark_path = light_path.replace("light", "dark")
        inverted.save(dark_path)
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
            "output/queen-of-shadows/priority-tokens.pdf",
            *sorted(glob.glob("wip/queen-of-shadows/priority-tokens-dark-*.png")),
        ],
        check=True,
    )


def do_qos_darkness_track():
    # Ideally 4.75" x 11", but scaled it down to fit on letter paper with some margins
    darkness_track_dims = (3142, 1264)
    retile(
        darkness_track_dims,
        load_subimages(
            darkness_track_dims,
            (1, 1),
            ["input/queen-of-shadows/darkness-track.png"],
        ),
        (1, 1),
        "wip/queen-of-shadows/darkness-track-landscape-*.png",
    )
    landscape_to_portrait(
        glob.glob("wip/queen-of-shadows/darkness-track-landscape-*.png")
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "4.42inx10.5in",
            "--fit",
            "shrink",
            "-o",
            "output/queen-of-shadows/darkness-track.pdf",
            *sorted(glob.glob("wip/queen-of-shadows/darkness-track-portrait-*.png")),
        ],
        check=True,
    )


def do_qos_chronicle_tasks():
    retile(
        tarot_landscape_dims,
        load_images_2up(
            tarot_landscape_dims,
            (5, 1),
            ["input/queen-of-shadows/chronicle-tasks-front.png"],
            ["input/queen-of-shadows/chronicle-tasks-back.png"],
            filter=image_middle_not_all_white,
        ),
        (2, 2),
        "wip/queen-of-shadows/chronicle-tasks-*.png",
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
            f"output/queen-of-shadows/chronicle-tasks.pdf",
            *sorted(glob.glob("wip/queen-of-shadows/chronicle-tasks-*.png")),
        ],
        check=True,
    )


def do_qos_player_board():
    # Ideally 4.75" x 11", but scaled it down to fit on letter paper with some margins
    player_board_dims = (3142, 1264)
    retile(
        player_board_dims,
        load_subimages(
            player_board_dims,
            (1, 1),
            sorted(glob.glob("input/queen-of-shadows/player-board-*.png")),
        ),
        (1, 1),
        "wip/queen-of-shadows/player-board-landscape-*.png",
    )
    landscape_to_portrait(
        glob.glob("wip/queen-of-shadows/player-board-landscape-*.png")
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "4.42inx10.5in",
            "--fit",
            "shrink",
            "-o",
            "output/queen-of-shadows/player-board.pdf",
            *sorted(glob.glob("wip/queen-of-shadows/player-board-portrait-*.png")),
        ],
        check=True,
    )


def do_qos_prisoner_tiles_helper(*, light_mode=False):
    """unlike most things in this kit, this is designed to be printed double-sided"""
    # 745x438
    prisoner_tile_dims = (745, 438)
    mode = "light" if light_mode else "dark"
    for state in ["freed", "imprisoned"]:
        img = Image.open(f"input/queen-of-shadows/prisoner-{state}.png")
        inverted = ImageOps.invert(img.convert("RGB")) if light_mode else img
        inverted.save(f"wip/queen-of-shadows/prisoner-{state}-{mode}.png")
    retile(
        prisoner_tile_dims,
        load_subimages(
            prisoner_tile_dims,
            (1, 1),
            # The following fancy ordering makes the edges between tiles legible
            [
                f"wip/queen-of-shadows/prisoner-imprisoned-{mode}.png",
                f"wip/queen-of-shadows/prisoner-freed-{mode}.png",
            ]
            * 12
            + [
                f"wip/queen-of-shadows/prisoner-freed-{mode}.png",
                f"wip/queen-of-shadows/prisoner-imprisoned-{mode}.png",
            ]
            * 12,
        ),
        (4, 6),
        f"wip/queen-of-shadows/prisoner-tiles-{mode}-portrait-*.png",
    )
    portrait_to_landscape(
        glob.glob(f"wip/queen-of-shadows/prisoner-tiles-{mode}-portrait-*.png")
    )
    subprocess.run(
        [
            "img2pdf",
            "--pagesize",
            "letter",
            "--imgsize",
            "6inx8in",
            "--fit",
            "shrink",
            "-o",
            f"output/queen-of-shadows/prisoner-tiles-{mode}.pdf",
            *sorted(
                glob.glob(f"wip/queen-of-shadows/prisoner-tiles-{mode}-landscape-*.png")
            ),
        ],
        check=True,
    )


def do_qos_shadow_cards():
    # 4713x5256
    # 7x5
    command_card_dims = (673, 1051)
    retile(
        command_card_dims,
        load_subimages(
            command_card_dims,
            (7, 5),
            [
                "input/queen-of-shadows/shadow-card-fronts.png"
            ],  # ignore the card backs: not worth the fuss
        ),
        (4, 2),
        "wip/queen-of-shadows/shadow-cards-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/queen-of-shadows/shadow-cards-portrait-*.png"))
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/queen-of-shadows/shadow-cards-landscape-*.png")),
        "output/queen-of-shadows/shadow-cards.pdf",
    )


def do_qos_title_cards():
    # 3969x1795
    # 6x2
    # 661x898
    title_card_dims = (661, 898)
    retile(
        title_card_dims,
        load_subimages(
            title_card_dims,
            (6, 2),
            ["input/queen-of-shadows/title-cards.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        "wip/queen-of-shadows/title-cards-portrait-*.png",
    )
    portrait_to_landscape(
        glob.glob("wip/queen-of-shadows/title-cards-portrait-*.png"), ccw=True
    )
    typeset_landscape_bridge_cards(
        sorted(glob.glob("wip/queen-of-shadows/title-cards-landscape-*.png")),
        "output/queen-of-shadows/title-cards.pdf",
    )
