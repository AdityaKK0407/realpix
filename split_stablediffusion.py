"""
split_stablediffusion.py
-------------------------
Collects all images from StableDiffusion/{512,768,1024}/{man,woman}
and redistributes them into train / valid / test folders.

Split ratio: 80% train | 10% valid | 10% test  (randomised, reproducible)
"""

import os
import random
import shutil

# -- Config -------------------------------------------------------------------
SEED        = 42
TRAIN_RATIO = 0.80
VALID_RATIO = 0.10

SD_ROOT   = r"d:\realpix\StableDiffusion"
TRAIN_DIR = os.path.join(SD_ROOT, "train")
VALID_DIR = os.path.join(SD_ROOT, "valid")
TEST_DIR  = os.path.join(SD_ROOT, "test")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
SOURCE_DIRS = ["512/man", "512/woman", "768/man", "768/woman", "1024/man", "1024/woman"]
# -----------------------------------------------------------------------------


def gather_images():
    """Return list of (full_path, unique_name) for all images."""
    results = []
    for subdir in SOURCE_DIRS:
        folder = os.path.join(SD_ROOT, subdir)
        if not os.path.isdir(folder):
            continue
        prefix = subdir.replace("/", "_").replace("\\", "_")  # e.g. "512_man"
        for fname in sorted(os.listdir(folder)):
            if os.path.splitext(fname)[1].lower() in IMAGE_EXTS:
                full = os.path.join(folder, fname)
                # prefix to avoid name collisions across subfolders
                unique = f"{prefix}_{fname}"
                results.append((full, unique))
    return results


def move_files(items, dst):
    os.makedirs(dst, exist_ok=True)
    for src_path, new_name in items:
        shutil.move(src_path, os.path.join(dst, new_name))


def main():
    all_images = gather_images()
    total = len(all_images)
    print(f"Found {total} images across StableDiffusion subfolders")

    if total == 0:
        print("No images found.")
        return

    random.seed(SEED)
    random.shuffle(all_images)

    n_valid = int(total * VALID_RATIO)
    n_test  = int(total * (1 - TRAIN_RATIO - VALID_RATIO))
    n_train = total - n_valid - n_test

    valid_files = all_images[:n_valid]
    test_files  = all_images[n_valid : n_valid + n_test]
    train_files = all_images[n_valid + n_test:]

    print(f"\nSplit summary:")
    print(f"  Train : {n_train:5d}  ({n_train/total*100:.1f}%)")
    print(f"  Valid : {n_valid:5d}  ({n_valid/total*100:.1f}%)")
    print(f"  Test  : {n_test:5d}  ({n_test/total*100:.1f}%)")

    print(f"\nMoving {n_train} files to train/ ...")
    move_files(train_files, TRAIN_DIR)

    print(f"Moving {n_valid} files to valid/ ...")
    move_files(valid_files, VALID_DIR)

    print(f"Moving {n_test} files to test/ ...")
    move_files(test_files, TEST_DIR)

    # Verify
    ct = len(os.listdir(TRAIN_DIR))
    cv = len(os.listdir(VALID_DIR))
    ce = len(os.listdir(TEST_DIR))
    print(f"\nFinal counts:")
    print(f"  train/ : {ct}")
    print(f"  valid/ : {cv}")
    print(f"  test/  : {ce}")
    print(f"  TOTAL  : {ct+cv+ce}")
    print("\nDone!")


if __name__ == "__main__":
    main()
