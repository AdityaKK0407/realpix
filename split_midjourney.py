"""
split_midjourney.py
--------------------
Redistributes MidJourney images from the existing `train/` folder into
proper train / valid / test splits WITHOUT copying files (uses move).

Split ratio: 80% train | 10% valid | 10% test  (randomised, reproducible)
"""

import os
import random
import shutil

# ── Config ──────────────────────────────────────────────────────────────────
SEED          = 42
TRAIN_RATIO   = 0.80
VALID_RATIO   = 0.10
TEST_RATIO    = 0.10   # remainder

SRC_DIR   = r"d:\realpix\MidJourney\train"
VALID_DIR = r"d:\realpix\MidJourney\valid"
TEST_DIR  = r"d:\realpix\MidJourney\test"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
# ────────────────────────────────────────────────────────────────────────────

def gather_images(folder: str) -> list[str]:
    """Return sorted list of image filenames (basenames) in *folder*."""
    return sorted(
        f for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS
    )


def move_files(names: list[str], src: str, dst: str):
    os.makedirs(dst, exist_ok=True)
    for name in names:
        shutil.move(os.path.join(src, name), os.path.join(dst, name))


def main():
    # ── Gather all images currently in train/ ──────────────────────────────
    all_images = gather_images(SRC_DIR)
    total = len(all_images)
    print(f"Found {total} images in {SRC_DIR}")

    if total == 0:
        print("No images found – nothing to do.")
        return

    # ── Shuffle deterministically ───────────────────────────────────────────
    random.seed(SEED)
    random.shuffle(all_images)

    # ── Calculate split sizes ───────────────────────────────────────────────
    n_valid = int(total * VALID_RATIO)
    n_test  = int(total * TEST_RATIO)
    n_train = total - n_valid - n_test   # keeps rounding errors in train

    valid_files = all_images[:n_valid]
    test_files  = all_images[n_valid : n_valid + n_test]
    # train_files stay in SRC_DIR — no move needed

    print(f"\nSplit summary:")
    print(f"  Train  : {n_train:6d}  ({n_train/total*100:.1f}%)  -> stays in train/")
    print(f"  Valid  : {n_valid:6d}  ({n_valid/total*100:.1f}%)  -> moving to valid/")
    print(f"  Test   : {n_test:6d}  ({n_test/total*100:.1f}%)  -> moving to test/")

    # ── Move files ──────────────────────────────────────────────────────────
    print(f"\nMoving {n_valid} files to {VALID_DIR} …")
    move_files(valid_files, SRC_DIR, VALID_DIR)

    print(f"Moving {n_test} files to {TEST_DIR} …")
    move_files(test_files, SRC_DIR, TEST_DIR)

    # ── Verify ──────────────────────────────────────────────────────────────
    remaining_train = len(gather_images(SRC_DIR))
    remaining_valid = len(gather_images(VALID_DIR))
    remaining_test  = len(gather_images(TEST_DIR))

    print(f"\nFinal counts:")
    print(f"  train/ : {remaining_train}")
    print(f"  valid/ : {remaining_valid}")
    print(f"  test/  : {remaining_test}")
    print(f"  TOTAL  : {remaining_train + remaining_valid + remaining_test}  (expected {total})")
    print("\nDone!")


if __name__ == "__main__":
    main()
