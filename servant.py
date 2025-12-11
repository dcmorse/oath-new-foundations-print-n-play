import glob
import subprocess
from typing import Literal
from retile import load_images_2up, load_subimages, retile, image_middle_not_all_white
from typesetting_helpers import landscape_to_portrait, portrait_to_landscape
import shutil

ServantDir = Literal["servant-nf", "servant-base"]
servant_base_dir = "servant-base"
servant_nf_dir = "servant-nf"


def do_servant_commands(servant_dir: ServantDir):
    # 4039x5256
    # 6x4
    # denizen-sized
    servant_command_dims = (673, 1051)
    retile(
        servant_command_dims,
        load_subimages(
            servant_command_dims,
            (6, 4),
            [f"input/{servant_dir}/commands.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        f"wip/{servant_dir}/commands-portrait-*.png",
    )
    portrait_to_landscape(glob.glob(f"wip/{servant_dir}/commands-portrait-*.png"))
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob(f"wip/{servant_dir}/commands-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            f"output/{servant_dir}/commands.pdf",
        ],
        check=True,
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
    # 4039x5256
    mood_portrait_dims = (676, 1051)
    retile(
        mood_portrait_dims,
        load_subimages(
            mood_portrait_dims,
            (6, 5),
            [f"input/{servant_dir}/mood-fronts.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        f"wip/{servant_dir}/moods-portrait-*.png",
    )
    portrait_to_landscape(glob.glob(f"wip/{servant_dir}/moods-portrait-*.png"))
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob(f"wip/{servant_dir}/moods-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            f"output/{servant_dir}/moods.pdf",
        ],
        check=True,
    )


def do_servant_base_moods():
    do_servant_moods(servant_base_dir)


def do_servant_nf_moods():
    do_servant_moods(servant_nf_dir)


def do_servant_reference_cards(servant_dir: ServantDir):
    # 4039x5256
    reference_card_dims = (673, 1051)
    retile(
        reference_card_dims,
        load_images_2up(
            reference_card_dims,
            (6, 5),
            [f"input/{servant_dir}/reference-fronts.png"],
            [f"input/{servant_dir}/reference-backs.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        f"wip/{servant_dir}/reference-cards-portrait-*.png",
    )
    portrait_to_landscape(
        glob.glob(f"wip/{servant_dir}/reference-cards-portrait-*.png")
    )
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob(f"wip/{servant_dir}/reference-cards-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            f"output/{servant_dir}/reference-cards.pdf",
        ],
        check=True,
    )


def do_servant_base_reference_cards():
    do_servant_reference_cards(servant_base_dir)


def do_servant_nf_reference_cards():
    do_servant_reference_cards(servant_nf_dir)
