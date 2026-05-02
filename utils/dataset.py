import os
import random
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms


class DeepfakeDataset(Dataset):
    """
    Loads images from:
        root_dir/real/  -> label 0
        root_dir/fake/  -> label 1

    Returns (rgb_tensor, fft_tensor, label) per sample.

    Args:
        balance (bool): Undersample majority class to match minority count.
        train   (bool): Apply data augmentation (training only).
    """

    IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

    def __init__(self, root_dir, balance=False, train=False):
        self.root_dir = root_dir
        self.train    = train
        self.images   = []
        self.labels   = []

        # ── Base transform (both train & val) ──────────────────────────────
        self.base_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225]),
        ])

        # ── Train-only RGB color augmentations (applied after FFT is done) ─
        # Spatial augmentations are handled on the raw numpy image below
        # so both RGB and FFT branches see the same geometry.
        self.color_aug = transforms.Compose([
            transforms.ToPILImage(),
            transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(
                brightness=0.3, contrast=0.3,
                saturation=0.2, hue=0.05
            ),
            transforms.RandomGrayscale(p=0.05),  # rarely, force freq-only cues
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225]),
        ])

        # ── Collect paths per class ────────────────────────────────────────
        per_class = {}
        for label, folder in enumerate(["real", "fake"]):
            folder_path = os.path.join(root_dir, folder)
            if not os.path.isdir(folder_path):
                print(f"[WARNING] Folder not found, skipping: {folder_path}")
                continue
            paths = []
            for img_name in sorted(os.listdir(folder_path)):
                if os.path.splitext(img_name)[1].lower() in self.IMAGE_EXTS:
                    paths.append(os.path.join(folder_path, img_name))
            per_class[label] = paths

        # ── Undersample majority class if requested ────────────────────────
        if balance and len(per_class) == 2:
            min_count = min(len(v) for v in per_class.values())
            for label, paths in per_class.items():
                if len(paths) > min_count:
                    paths = random.sample(paths, min_count)
                self.images.extend(paths)
                self.labels.extend([label] * len(paths))
            print(f"[BALANCE] Undersampled to {min_count} per class "
                  f"({min_count * 2} total)")
        else:
            for label, paths in per_class.items():
                self.images.extend(paths)
                self.labels.extend([label] * len(paths))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        path = self.images[idx]
        img  = cv2.imread(path)

        if img is None:
            rgb = torch.zeros(3, 224, 224)
            fft = torch.zeros(1, 224, 224)
            return rgb, fft, torch.tensor(self.labels[idx], dtype=torch.float32)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # H x W x 3, uint8

        # ── Spatial augmentation on raw image (shared for RGB + FFT) ──────
        if self.train:
            # Random horizontal flip
            if random.random() < 0.5:
                img = cv2.flip(img, 1)

        # ── FFT branch (uses spatially-augmented image, no color changes) ──
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, (224, 224))
        fft  = np.fft.fft2(gray)
        fft  = np.abs(np.fft.fftshift(fft))
        fft  = np.log1p(fft)
        fft  = fft / (fft.max() + 1e-8)
        fft  = torch.tensor(fft, dtype=torch.float32).unsqueeze(0)

        # ── RGB branch ─────────────────────────────────────────────────────
        if self.train:
            rgb = self.color_aug(img)   # crop + flip + color jitter + normalize
        else:
            rgb = self.base_transform(img)

        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return rgb, fft, label