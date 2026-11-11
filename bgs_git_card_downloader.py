#!/usr/bin/env python
"""Fetch or refresh the local checkout of Buried Giant Studios' card repo
(https://github.com/buriedgiantstudios/cards/) into bgs-cards/, which oath.py reads.

It's a sparse, shallow checkout: only the Oath data and images (~150MB).
"""

import os
import subprocess

from bgs_cards import BGS_DIR

BGS_URL = "https://github.com/buriedgiantstudios/cards.git"


def fetch() -> None:
    """Clone (sparse + shallow) or fast-forward the BGS checkout."""
    if os.path.isdir(os.path.join(BGS_DIR, ".git")):
        subprocess.run(["git", "-C", BGS_DIR, "pull", "--ff-only", "--depth", "1"], check=True)
        return
    subprocess.run(
        ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", BGS_URL, BGS_DIR],
        check=True,
    )
    subprocess.run(
        ["git", "-C", BGS_DIR, "sparse-checkout", "set",
         "content/card-data/oath", "content/card-images/oath"],
        check=True,
    )


if __name__ == "__main__":
    fetch()
