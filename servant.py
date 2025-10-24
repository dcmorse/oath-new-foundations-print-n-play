import glob
import subprocess
from retile import load_images_2up, load_subimages, retile, image_middle_not_all_white
from typesetting_helpers import landscape_to_portrait, portrait_to_landscape
import shutil


def do_servant_commands():
    # 4039x5256
    # 6x4
    # denizen-sized
    servant_command_dims = (673, 1051)
    retile(
        servant_command_dims,
        load_subimages(
            servant_command_dims,
            (6, 4),
            ["input/servant/commands.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        "wip/servant/commands-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/servant/commands-portrait-*.png"))
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob("wip/servant/commands-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            "output/servant/commands.pdf",
        ],
        check=True,
    )


def do_servant_display_board():
    # 3220x1336 landscape
    # 1041 pixels is 3.5 inches
    # so overall height of 1336 is 4.5 inches
    # 681 pixels is 2.25 inches
    # overall width is about 10.75 inches
    shutil.copyfile(
        "input/servant/display-board.png", "wip/servant/display-board-landscape.png"
    )
    landscape_to_portrait(["wip/servant/display-board-landscape.png"])
    subprocess.run(
        [
            "img2pdf",
            "wip/servant/display-board-portrait.png",
            "--pagesize",
            "letter",
            "--imgsize",
            "4.5inx10.75in",
            "--fit",
            "shrink",
            "-o",
            "output/servant/display-board.pdf",
        ],
        check=True,
    )


def do_servant_moods():
    # 4039x5256
    mood_portrait_dims = (676, 1051)
    retile(
        mood_portrait_dims,
        load_subimages(
            mood_portrait_dims,
            (6, 5),
            ["input/servant/mood-fronts.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        "wip/servant/moods-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/servant/moods-portrait-*.png"))
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob("wip/servant/moods-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            "output/servant/moods.pdf",
        ],
        check=True,
    )


def do_servant_reference_cards():
    # 4039x5256
    reference_card_dims = (673, 1051)
    retile(
        reference_card_dims,
        load_images_2up(
            reference_card_dims,
            (6, 5),
            ["input/servant/reference-fronts.png"],
            ["input/servant/reference-backs.png"],
            filter=image_middle_not_all_white,
        ),
        (4, 2),
        "wip/servant/reference-cards-portrait-*.png",
    )
    portrait_to_landscape(glob.glob("wip/servant/reference-cards-portrait-*.png"))
    subprocess.run(
        [
            "img2pdf",
            *sorted(glob.glob("wip/servant/reference-cards-landscape*.png")),
            "--pagesize",
            "letter",
            "--imgsize",
            "7inx9in",
            "--fit",
            "shrink",
            "-o",
            "output/servant/reference-cards.pdf",
        ],
        check=True,
    )
