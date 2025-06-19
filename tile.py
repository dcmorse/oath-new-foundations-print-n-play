from typing import Generator, List, Tuple
from PIL import Image
from sys import argv
import math
import glob


def page_filenames(
    tiling: Tuple[int, int], src_glob: str
) -> Generator[List[str], None, None]:
    filenames = sorted(glob.glob(src_glob))
    chunk_size = math.prod(tiling)
    for i in range(int(math.ceil(len(filenames) / chunk_size))):
        yield filenames[i * chunk_size : (i + 1) * chunk_size]


def quilt(tiling: Tuple[int, int], src_glob: str, dst_glob: str):
    witnessed_img_dims = None
    for batch_idx, batch in enumerate(page_filenames(tiling, src_glob)):
        imgs = [Image.open(fn) for fn in batch]
        if witnessed_img_dims is None:
            witnessed_img_dims = imgs[0].size
        for img in imgs:
            assert img.size == witnessed_img_dims
        w, h = witnessed_img_dims
        n, m = tiling
        output_img = Image.new("RGB", (n * w, m * h), "white")
        for i, img in enumerate(imgs):
            x = (i % n) * w
            y = (i // n) * h
            output_img.paste(img, (x, y))
        output_img.save(dst_glob.replace("*", f"{batch_idx:02d}"))


# python tile.py 2 2 site-\*.jpg sites-\*.jpg
if __name__ == "__main__":
    if len(argv) != 5:
        print(
            "Usage: python tile.py <width> <height> <input_glob> <output_glob>\n"
            "Example: python tile.py 2 2 site-\\*.jpg sites-\\*.jpg"
            "Note: escape asterisk with backslash in shell (e.g., site-\\*.jpg)\n"
        )
        exit(1)
    s_w, s_h, src_glob, dst_glob = argv[1:5]
    quilt((int(s_w), int(s_h)), src_glob, dst_glob)
