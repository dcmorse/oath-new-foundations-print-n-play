import os
import re
import glob
import shutil

# output card dims 4.5" x 3.5"
# res = (1358, 1051)


def rename_all():
    for site_munged_name in glob.glob("input/httpsdldropboxusercontentcom*Site*.jpg"):
        match = re.search(r"Site(?P<id>\d*)jpg", site_munged_name)
        if not match:
            raise ValueError(
                f"expected site filename to contain the string 'Site' then some digits: {site_munged_name!r}"
            )
        site_id = int(match["id"] or "1")
        site_clean_name = f"wip/site-{site_id:02d}.jpg"
        copy_when_newer(site_munged_name, site_clean_name)


def copy_when_newer(src, dst):
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        print(f"copy({src=}, {dst=})")
        shutil.copy2(src, dst)


if __name__ == "__main__":
    rename_all()
