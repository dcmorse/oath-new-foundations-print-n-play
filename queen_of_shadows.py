import glob
from retile import load_subimages, retile, image_middle_not_all_white
from typesetting_helpers import (
    portrait_to_landscape,
    typeset_landscape_bridge_cards,
)
import shutil


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
