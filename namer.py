import os
import csv
import shutil
import filecmp

tts_src_dir = os.path.join(
    os.path.expanduser("~"),
    ".var/app/com.valvesoftware.Steam/.local/share/Tabletop Simulator/Mods/Images",
)
staging_dst_dir = "input"  # yes, the destination is called "input" - we're writing files for later use by oath.py, so the name's relative to that project's pov.


def name_map():
    with open("names.csv", "r", encoding="utf-8") as f:
        return {row["tts_name"]: row["human_name"] for row in csv.DictReader(f)}


def copy_src_to_dst():
    for tts_name, human_name in name_map().items():
        src_path = os.path.join(tts_src_dir, tts_name)
        dst_path = os.path.join(staging_dst_dir, human_name)
        if not os.path.exists(src_path):
            print(f"missing {dst_path} - {src_path}")
            continue
        if os.path.exists(dst_path):
            if filecmp.cmp(src_path, dst_path, shallow=False):
                print(f"same    {dst_path}")
                continue
            print(f"update  {dst_path}")
        else:
            print(f"create  {dst_path}")
        shutil.copy2(src_path, dst_path)


copy_src_to_dst()
