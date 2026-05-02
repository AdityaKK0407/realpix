"""
train.py — RealPix Training Script
------------------------------------
Trains the FusionModel (ViT-B/16 + FFT CNN) on the data/ folder.

Dataset layout expected:
    data/train/real/   (label 0)
    data/train/fake/   (label 1)
    data/valid/real/
    data/valid/fake/
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

from model import DualBranchModel
from utils.dataset import DeepfakeDataset

# ── Config ────────────────────────────────────────────────────────────────
TRAIN_DIR  = "data/train"
VALID_DIR  = "data/valid"
SAVE_PATH  = "deepfake_model.pt"

BATCH_SIZE = 16
EPOCHS     = 10
LR         = 1e-4
PATIENCE   = 5      # early-stop after N epochs with no val_loss improvement
LABEL_SMOOTHING = 0.1  # soften targets: 0→0.05, 1→0.95

# Classes are balanced via undersampling in DeepfakeDataset(balance=True)
# No pos_weight needed
# ──────────────────────────────────────────────────────────────────────────

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():
    print(f"Using device: {DEVICE}")

    # ── Datasets & Loaders ────────────────────────────────────────────────
    train_dataset = DeepfakeDataset(TRAIN_DIR, balance=True, train=True)
    valid_dataset = DeepfakeDataset(VALID_DIR)

    print(f"Train samples : {len(train_dataset)}")
    print(f"Valid samples : {len(valid_dataset)}")

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=4, pin_memory=(DEVICE.type == "cuda")
    )
    valid_loader = DataLoader(
        valid_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=4, pin_memory=(DEVICE.type == "cuda")
    )

    # ── Model ─────────────────────────────────────────────────────────────
    model = DualBranchModel().to(DEVICE)

    # ── Freeze early ViT blocks (prevents overfitting on small dataset) ───
    # ViT-B/16 has 12 blocks. Blocks 0-5 learn generic low-level features
    # (edges, textures) from ImageNet — no need to retrain those.
    # Blocks 6-11 learn task-specific features — keep those trainable.
    vit = model.rgb.model
    for param in vit.patch_embed.parameters():
        param.requires_grad = False
    for i, block in enumerate(vit.blocks):
        if i < 6:
            for param in block.parameters():
                param.requires_grad = False
    frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    total  = sum(p.numel() for p in model.parameters())
    print(f"[FREEZE] {frozen:,} / {total:,} params frozen "
          f"({frozen / total * 100:.1f}%)")

    # ── Loss ──────────────────────────────────────────────────────────────
    criterion = nn.BCEWithLogitsLoss()

    # ── Optimizer & Scheduler ─────────────────────────────────────────────
    # Pretrained ViT gets a lower LR to avoid catastrophic forgetting;
    # from-scratch FFT branch & classifier get the full LR.
    optimizer = AdamW([
        {"params": model.rgb.parameters(),        "lr": LR * 0.1},  # 1e-5
        {"params": model.fft.parameters(),        "lr": LR},        # 1e-4
        {"params": model.classifier.parameters(), "lr": LR},        # 1e-4
    ], weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS)

    # ── Training Loop ─────────────────────────────────────────────────────
    best_val_loss = float("inf")
    patience_counter = 0
    use_amp = DEVICE.type == "cuda"
    scaler = torch.amp.GradScaler(enabled=use_amp)

    for epoch in range(1, EPOCHS + 1):
        # -- Train --
        model.train()
        train_loss = 0.0
        train_correct = 0

        train_pbar = tqdm(train_loader, desc=f"Epoch [{epoch}/{EPOCHS}] Train", leave=False)
        for rgb, fft, labels in train_pbar:
            rgb    = rgb.to(DEVICE)
            fft    = fft.to(DEVICE)
            labels = labels.to(DEVICE).unsqueeze(1)   # (B,) -> (B,1)

            optimizer.zero_grad()
            with torch.amp.autocast(device_type=DEVICE.type, enabled=use_amp):
                logits = model(rgb, fft)                  # (B, 1)
                # Smooth labels: 0→0.05, 1→0.95 — prevents overconfidence
                smooth = labels * (1 - LABEL_SMOOTHING) + 0.5 * LABEL_SMOOTHING
                loss   = criterion(logits, smooth)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()

            train_loss    += loss.item()
            preds          = (torch.sigmoid(logits) >= 0.5).float()
            train_correct += (preds == labels).sum().item()

            train_pbar.set_postfix(loss=loss.item())

        scheduler.step()

        # -- Validate --
        model.eval()
        val_loss = 0.0
        val_correct = 0

        with torch.no_grad():
            valid_pbar = tqdm(valid_loader, desc=f"Epoch [{epoch}/{EPOCHS}] Valid", leave=False)
            for rgb, fft, labels in valid_pbar:
                rgb    = rgb.to(DEVICE)
                fft    = fft.to(DEVICE)
                labels = labels.to(DEVICE).unsqueeze(1)

                with torch.amp.autocast(device_type=DEVICE.type, enabled=use_amp):
                    logits = model(rgb, fft)
                    loss   = criterion(logits, labels)

                val_loss    += loss.item()
                preds        = (torch.sigmoid(logits) >= 0.5).float()
                val_correct += (preds == labels).sum().item()
                
                valid_pbar.set_postfix(loss=loss.item())

        train_acc = train_correct / len(train_dataset) * 100
        val_acc   = val_correct   / len(valid_dataset) * 100
        avg_train = train_loss    / len(train_loader)
        avg_val   = val_loss      / len(valid_loader)

        print(
            f"Epoch [{epoch:>2}/{EPOCHS}]  "
            f"Train Loss: {avg_train:.4f}  Acc: {train_acc:.1f}%  |  "
            f"Val Loss: {avg_val:.4f}  Acc: {val_acc:.1f}%"
        )

        # Save best model / early stopping
        if avg_val < best_val_loss:
            best_val_loss = avg_val
            patience_counter = 0
            torch.save(model.state_dict(), SAVE_PATH)
            print(f"  -> Saved best model (val_loss={best_val_loss:.4f})")
        else:
            patience_counter += 1
            print(f"  -> No improvement ({patience_counter}/{PATIENCE})")
            if patience_counter >= PATIENCE:
                print("Early stopping triggered.")
                break

    print(f"\nTraining complete. Best model saved to '{SAVE_PATH}'")


if __name__ == "__main__":
    main()