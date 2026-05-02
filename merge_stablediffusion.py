"""
merge_stablediffusion.py
-------------------------
Copies StableDiffusion train/test images into data/train/fake and data/test/fake.
Uses COPY (not move) so SD originals are preserved.
Prefixes filenames with 'sd_' to avoid collisions.
"""

import os
import shutil

SD_ROOT   = r"d:\realpix\StableDiffusion"
DATA_ROOT = r"d:\realpix\data"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def copy_images(src_dir, dst_dir, prefix="sd_"):
    os.makedirs(dst_dir, exist_ok=True)
    count = 0
    for fname in os.listdir(src_dir):
        if os.path.splitext(fname)[1].lower() in IMAGE_EXTS:
            src = os.path.join(src_dir, fname)
            dst = os.path.join(dst_dir, f"{prefix}{fname}")
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                count += 1
    return count


def main():
    print("Copying StableDiffusion train -> data/train/fake ...")
    n1 = copy_images(
        os.path.join(SD_ROOT, "train"),
        os.path.join(DATA_ROOT, "train", "fake"),
    )
    print(f"  Copied {n1} images")

    print("Copying StableDiffusion test -> data/test/fake ...")
    n2 = copy_images(
        os.path.join(SD_ROOT, "test"),
        os.path.join(DATA_ROOT, "test", "fake"),
    )
    print(f"  Copied {n2} images")

    # Final counts
    tr_real = len(os.listdir(os.path.join(DATA_ROOT, "train", "real")))
    tr_fake = len(os.listdir(os.path.join(DATA_ROOT, "train", "fake")))
    te_real = len(os.listdir(os.path.join(DATA_ROOT, "test", "real")))
    te_fake = len(os.listdir(os.path.join(DATA_ROOT, "test", "fake")))

    print(f"\nFinal data/ counts:")
    print(f"  train/real : {tr_real}")
    print(f"  train/fake : {tr_fake}")
    print(f"  test/real  : {te_real}")
    print(f"  test/fake  : {te_fake}")
    print(f"  TOTAL      : {tr_real + tr_fake + te_real + te_fake}")
    print("\nDone!")


if __name__ == "__main__":
    main()
