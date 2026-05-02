"""
extract_split_archive.py
-------------------------
Extracts real photos from archive.zip and distributes them into:
  data/train/real  (80%)
  data/valid/real  (10%)
  data/test/real   (10%)

Prefixes filenames with 'arc_' to avoid collisions with existing data.
"""

import os
import random
import zipfile
import shutil

ARCHIVE   = r"d:\realpix\archive.zip"
DATA_ROOT = r"d:\realpix\data"
SEED      = 42

TRAIN_DIR = os.path.join(DATA_ROOT, "train", "real")
VALID_DIR = os.path.join(DATA_ROOT, "valid", "real")
TEST_DIR  = os.path.join(DATA_ROOT, "test",  "real")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def main():
    # -- Gather all image entries from the zip ---------------------------------
    with zipfile.ZipFile(ARCHIVE, "r") as z:
        all_entries = [
            e for e in z.namelist()
            if os.path.splitext(e)[1].lower() in IMAGE_EXTS
            and not e.endswith("/")
        ]

    total = len(all_entries)
    print(f"Found {total} images in archive.zip")

    # -- Shuffle & split -------------------------------------------------------
    random.seed(SEED)
    random.shuffle(all_entries)

    n_valid = int(total * 0.10)
    n_test  = int(total * 0.10)
    n_train = total - n_valid - n_test

    valid_entries = all_entries[:n_valid]
    test_entries  = all_entries[n_valid : n_valid + n_test]
    train_entries = all_entries[n_valid + n_test:]

    print(f"\nSplit summary:")
    print(f"  Train : {n_train:5d}  (80.0%)")
    print(f"  Valid : {n_valid:5d}  (10.0%)")
    print(f"  Test  : {n_test:5d}  (10.0%)")

    # -- Extract directly to destination dirs ---------------------------------
    for dst_dir, entries, label in [
        (TRAIN_DIR, train_entries, "train"),
        (VALID_DIR, valid_entries, "valid"),
        (TEST_DIR,  test_entries,  "test"),
    ]:
        os.makedirs(dst_dir, exist_ok=True)
        print(f"\nExtracting {len(entries)} files to {label}/real ...")
        with zipfile.ZipFile(ARCHIVE, "r") as z:
            for i, entry in enumerate(entries, 1):
                basename = os.path.basename(entry)
                new_name = f"arc_{basename}"
                dst_path = os.path.join(dst_dir, new_name)
                if not os.path.exists(dst_path):
                    data = z.read(entry)
                    with open(dst_path, "wb") as f:
                        f.write(data)
                if i % 500 == 0:
                    print(f"  ... {i}/{len(entries)}")

    # -- Final counts ----------------------------------------------------------
    tr = len(os.listdir(TRAIN_DIR))
    va = len(os.listdir(VALID_DIR))
    te = len(os.listdir(TEST_DIR))

    print(f"\nFinal real image counts:")
    print(f"  train/real : {tr}")
    print(f"  valid/real : {va}")
    print(f"  test/real  : {te}")
    print(f"\nDone!")


if __name__ == "__main__":
    main()
