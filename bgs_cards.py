"""Card images and metadata from Buried Giant Studios' public card repo.

    https://github.com/buriedgiantstudios/cards/

We keep a sparse, shallow checkout (only the Oath data and images, ~150MB) in
`bgs-cards/` (override with $OATH_BGS_DIR).  Fetch or refresh it with
`./bgs_git_card_downloader.py`.

This module is a thin query layer over the YAML card data.
"""

import os
import sys
from dataclasses import dataclass, field
from functools import cache
from typing import Dict, List, Optional

import yaml
from PIL import Image

BGS_DIR = os.environ.get("OATH_BGS_DIR", os.path.join(os.path.dirname(__file__), "bgs-cards"))
LOCALE = "en-US"
DATA_DIR = os.path.join(BGS_DIR, "content", "card-data", "oath", LOCALE)
IMAGE_DIR = os.path.join(BGS_DIR, "content", "card-images", "oath", LOCALE)

# The three data files, in a stable order.
DATA_FILES = [
    "oathbasegame.yml",
    "denizen-deck.yml",
    "oath-newfoundations.yml",
    "oath-clockwork.yml",  # Servant and Queen of Shadows
]
CLOCKWORK_FILE = "oath-clockwork.yml"

SUITS = ["Arcane", "Beast", "Discord", "Hearth", "Nomad", "Order"]


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    image: str  # image basename, without extension; the stable key
    text: str
    tags: frozenset
    source: str  # data file the card came from
    image_class: Optional[str] = None  # "square" | "rotated" | None (portrait)
    flip_side: Optional[str] = None  # id of the card on the other side
    meta: Dict = field(default_factory=dict, hash=False, compare=False)

    @property
    def path(self) -> str:
        return os.path.join(IMAGE_DIR, self.image + ".png")

    @property
    def suit(self) -> Optional[str]:
        return next((s for s in SUITS if s in self.tags), None)

    @property
    def is_nf_file(self) -> bool:
        return self.source == "oath-newfoundations.yml"

    def load(self) -> Image.Image:
        """The card image as RGB, with any transparency flattened onto white."""
        img = Image.open(self.path)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, "white")
            bg.paste(img, mask=img.getchannel("A"))
            return bg
        return img.convert("RGB")


@cache
def all_cards() -> List[Card]:
    if not os.path.isdir(DATA_DIR):
        sys.exit(
            f"BGS card data not found at {BGS_DIR}. Run ./bgs_git_card_downloader.py first."
        )
    cards = []
    for fn in DATA_FILES:
        with open(os.path.join(DATA_DIR, fn), encoding="utf-8") as f:
            for row in yaml.safe_load(f):
                cards.append(
                    Card(
                        id=row["id"],
                        name=row["name"],
                        image=row["image"],
                        text=row.get("text", ""),
                        tags=frozenset(row.get("tags", [])),
                        source=fn,
                        image_class=row.get("imageClass"),
                        flip_side=row.get("flipSide"),
                        meta=row.get("meta") or {},
                    )
                )
    return cards


@cache
def by_id() -> Dict[str, Card]:
    return {c.id: c for c in all_cards()}


def cards_tagged(tag: str, *, nf: bool = True) -> List[Card]:
    """Cards with `tag`. nf=True: from the New Foundations files; nf=False: base game file.
    Clockwork (Servant / Queen of Shadows) cards are not included; see clockwork_cards."""
    return [
        c
        for c in all_cards()
        if tag in c.tags
        and c.source != CLOCKWORK_FILE
        and (c.source == "oathbasegame.yml") != nf
    ]


def clockwork_cards(tag: str, *, nf: bool = False) -> List[Card]:
    """Clockwork cards with `tag`, in id order. nf=True selects the New Foundations
    variants of Servant cards (tagged "New Foundations"); nf=False the base-game ones.
    Queen of Shadows cards have no NF variants and are untagged: pass nf=False."""
    return sorted(
        (
            c
            for c in all_cards()
            if c.source == CLOCKWORK_FILE
            and tag in c.tags
            and ("New Foundations" in c.tags) == nf
        ),
        key=lambda c: c.id,
    )


# --- Denizens -----------------------------------------------------------------
#
# A denizen is a suited card that isn't an edifice. Three flavours matter for printing:
#   new       - printed for New Foundations: the 60 brand-new denizens (denizen-deck.yml)
#               plus the revised ones (suffixed "-NF" in the New Foundations file).
#   unchanged - in the base game and still in NF unchanged, so owners of base Oath don't
#               need to print them (but can, to run several universes from one box).


def _is_denizen(c: Card) -> bool:
    return c.suit is not None and not (c.tags & {"Edifice", "Site", "Relic"})


def new_foundations_denizens() -> List[Card]:
    return [c for c in all_cards() if _is_denizen(c) and c.source != "oathbasegame.yml"]


def unchanged_denizens() -> List[Card]:
    return [
        c
        for c in all_cards()
        if _is_denizen(c)
        and c.source == "oathbasegame.yml"
        and "New Foundations" in c.tags
    ]


def edifice_pairs() -> List[tuple]:
    """(intact, ruined) pairs, in id order."""
    pairs = []
    for c in all_cards():
        if "Edifice" in c.tags and "Intact" in c.tags:
            pairs.append((c, by_id()[c.flip_side]))
    return pairs
