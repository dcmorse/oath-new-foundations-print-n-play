import glob
import subprocess
from typing import Literal
from PIL import Image
import bgs_cards
from retile import tile
from typesetting_helpers import (
    card_images,
    img2pdf_pages,
    landscape_to_portrait,
    portrait_to_landscape,
)
import shutil

ServantDir = Literal["servant-nf", "servant-base"]
servant_base_dir = "servant-base"
servant_nf_dir = "servant-nf"


def _is_nf(servant_dir: ServantDir) -> bool:
    return servant_dir == servant_nf_dir


def do_servant_commands(servant_dir: ServantDir):
    cards = bgs_cards.clockwork_cards("Command", nf=_is_nf(servant_dir))
    tile(
        card_images(cards), (4, 2), f"wip/{servant_dir}/commands-portrait-*.png"
    )
    portrait_to_landscape(glob.glob(f"wip/{servant_dir}/commands-portrait-*.png"))
    img2pdf_pages(
        "7inx9in",
        f"output/{servant_dir}/commands.pdf",
        sorted(glob.glob(f"wip/{servant_dir}/commands-landscape*.png")),
    )


def do_servant_base_commands():
    do_servant_commands(servant_base_dir)


def do_servant_nf_commands():
    do_servant_commands(servant_nf_dir)


def do_servant_display_board(servant_dir: ServantDir):
    # 3220x1336 landscape
    # 1041 pixels is 3.5 inches
    # so overall height of 1336 is 4.5 inches
    # 681 pixels is 2.25 inches
    # overall width is about 10.75 inches
    shutil.copyfile(
        f"input/{servant_dir}/display-board.png",
        f"wip/{servant_dir}/display-board-landscape.png",
    )
    landscape_to_portrait([f"wip/{servant_dir}/display-board-landscape.png"])
    subprocess.run(
        [
            "img2pdf",
            f"wip/{servant_dir}/display-board-portrait.png",
            "--pagesize",
            "letter",
            "--imgsize",
            "4.5inx10.75in",
            "--fit",
            "shrink",
            "-o",
            f"output/{servant_dir}/display-board.pdf",
        ],
        check=True,
    )


def do_servant_base_display_board():
    do_servant_display_board(servant_base_dir)


def do_servant_nf_display_board():
    do_servant_display_board(servant_nf_dir)


def do_servant_moods(servant_dir: ServantDir):
    cards = bgs_cards.clockwork_cards("Mood", nf=_is_nf(servant_dir))
    tile(card_images(cards), (4, 2), f"wip/{servant_dir}/moods-portrait-*.png")
    portrait_to_landscape(glob.glob(f"wip/{servant_dir}/moods-portrait-*.png"))
    img2pdf_pages(
        "7inx9in",
        f"output/{servant_dir}/moods.pdf",
        sorted(glob.glob(f"wip/{servant_dir}/moods-landscape*.png")),
    )


def do_servant_base_moods():
    do_servant_moods(servant_base_dir)


def do_servant_nf_moods():
    do_servant_moods(servant_nf_dir)


def do_servant_reference_cards(servant_dir: ServantDir):
    # The action cards. Most are double-sided and print as front/back pairs. The "Moon"
    # cards are one-sided and share a generic stone-wall back, which BGS doesn't
    # publish, so it comes from the TTS rip (the third tile of the back sheet).
    cards = bgs_cards.clockwork_cards("Action", nf=_is_nf(servant_dir))
    fronts = [c for c in cards if "(Back)" not in c.name]
    size = fronts[0].load().size
    sheet = Image.open(f"input/{servant_dir}/reference-backs.png")
    tw, th = sheet.width // 6, sheet.height // 5
    stone_back = sheet.crop((2 * tw, 0, 3 * tw, th)).resize(size, Image.LANCZOS)
    imgs = []
    for c in fronts:
        imgs += [
            c.load(),
            bgs_cards.by_id()[c.flip_side].load() if c.flip_side else stone_back,
        ]
    tile(imgs, (4, 2), f"wip/{servant_dir}/reference-cards-portrait-*.png")
    portrait_to_landscape(
        glob.glob(f"wip/{servant_dir}/reference-cards-portrait-*.png")
    )
    img2pdf_pages(
        "7inx9in",
        f"output/{servant_dir}/reference-cards.pdf",
        sorted(glob.glob(f"wip/{servant_dir}/reference-cards-landscape*.png")),
    )


def do_servant_base_reference_cards():
    do_servant_reference_cards(servant_base_dir)


def do_servant_nf_reference_cards():
    do_servant_reference_cards(servant_nf_dir)
