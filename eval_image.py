"""
eval_image.py — Single Image Inference
----------------------------------------
Run deepfake detection on a single image file.

Usage:
    python eval_image.py <path_to_image>
"""

import sys
import cv2
import torch
import numpy as np
from torchvision import transforms

from model import DualBranchModel

MODEL_PATH = "deepfake_model.pt"
DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Transforms (must match utils/dataset.py) ──────────────────────────────
rgb_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])


def preprocess(image_path: str):
    """Load image and return (rgb_tensor, fft_tensor) ready for the model."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # RGB branch
    rgb = rgb_transform(img).unsqueeze(0)   # (1, 3, 224, 224)

    # FFT branch
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    fft  = np.fft.fft2(gray)
    fft  = np.abs(np.fft.fftshift(fft))
    fft  = np.log1p(fft)
    fft  = fft / (fft.max() + 1e-8)
    fft  = cv2.resize(fft, (224, 224))
    fft  = torch.tensor(fft, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # (1,1,224,224)

    return rgb, fft


def predict(image_path: str) -> dict:
    """Return prediction label and confidence for a single image."""
    model = DualBranchModel().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    rgb, fft = preprocess(image_path)
    rgb = rgb.to(DEVICE)
    fft = fft.to(DEVICE)

    with torch.no_grad():
        logit = model(rgb, fft)           # (1, 1)
        prob  = torch.sigmoid(logit).item()

    label      = "AI GENERATED" if prob >= 0.5 else "REAL IMAGE"
    confidence = prob if prob >= 0.5 else 1 - prob

    return {"label": label, "confidence": round(confidence * 100, 2), "fake_prob": round(prob, 4)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eval_image.py <image_path>")
        sys.exit(1)

    result = predict(sys.argv[1])
    print(f"Prediction : {result['label']}")
    print(f"Confidence : {result['confidence']}%")
    print(f"Fake prob  : {result['fake_prob']}")
