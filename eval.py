"""
eval.py — RealPix Evaluation Script
-------------------------------------
Evaluates the trained FusionModel on the test set and prints
classification report + ROC-AUC score.
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, roc_auc_score, roc_curve

from model import DualBranchModel
from utils.dataset import DeepfakeDataset

# ── Config ────────────────────────────────────────────────────────────────
TEST_DIR   = "data/test"
MODEL_PATH = "deepfake_model.pt"
BATCH_SIZE = 16
# ──────────────────────────────────────────────────────────────────────────

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():
    print(f"Using device: {DEVICE}")

    # ── Dataset & Loader ──────────────────────────────────────────────────
    test_dataset = DeepfakeDataset(TEST_DIR)
    test_loader  = DataLoader(
        test_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=4, pin_memory=(DEVICE.type == "cuda")
    )
    print(f"Test samples: {len(test_dataset)}")

    # ── Model ─────────────────────────────────────────────────────────────
    model = DualBranchModel().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
    print("Model loaded.")

    # ── Inference ─────────────────────────────────────────────────────────
    all_labels = []
    all_preds  = []
    all_probs  = []

    with torch.no_grad():
        for rgb, fft, labels in test_loader:
            rgb  = rgb.to(DEVICE)
            fft  = fft.to(DEVICE)

            logits = model(rgb, fft)           # (B, 1)
            probs  = torch.sigmoid(logits)     # probability of fake
            preds  = (probs >= 0.5).long().squeeze(1)

            all_labels.extend(labels.long().cpu().numpy())
            all_preds.extend(preds.cpu().numpy())
            all_probs.extend(probs.squeeze(1).cpu().numpy())

    all_labels = np.array(all_labels)
    all_preds  = np.array(all_preds)
    all_probs  = np.array(all_probs)

    # ── Metrics ───────────────────────────────────────────────────────────
    print("\n=== Classification Report ===")
    print(classification_report(all_labels, all_preds, target_names=["Real", "Fake"]))

    auc = roc_auc_score(all_labels, all_probs)
    print(f"ROC-AUC Score: {auc:.4f}")

    # ── ROC Curve ─────────────────────────────────────────────────────────
    fpr, tpr, _ = roc_curve(all_labels, all_probs)
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve — RealPix Deepfake Detector")
    plt.legend()
    plt.tight_layout()
    plt.savefig("roc_curve.png")
    plt.show()
    print("ROC curve saved to roc_curve.png")


if __name__ == "__main__":
    main()