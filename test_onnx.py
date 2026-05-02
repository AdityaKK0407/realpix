"""
test_onnx.py — ONNX Runtime Inference
----------------------------------------
Run deepfake detection via the exported ONNX model on a single image.

Usage:
    python test_onnx.py <path_to_image>

Export the ONNX model first using export_onnx.py.
"""

import sys
import cv2
import numpy as np
import onnxruntime as ort
from torchvision import transforms
from PIL import Image

ONNX_PATH = "deepfake_model.onnx"

# ── Transforms (must match utils/dataset.py) ──────────────────────────────
rgb_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])


def preprocess(image_path: str):
    """Returns (rgb_np, fft_np) as float32 numpy arrays for ONNX input."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # RGB branch: (1, 3, 224, 224)
    pil_img = Image.fromarray(img)
    rgb = rgb_transform(pil_img).unsqueeze(0).numpy()   # float32

    # FFT branch: (1, 1, 224, 224)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    fft  = np.fft.fft2(gray)
    fft  = np.abs(np.fft.fftshift(fft))
    fft  = np.log1p(fft)
    fft  = fft / (fft.max() + 1e-8)
    fft  = cv2.resize(fft, (224, 224))
    fft  = fft[np.newaxis, np.newaxis, :, :].astype(np.float32)  # (1,1,224,224)

    return rgb, fft


def predict(image_path: str) -> dict:
    """Run ONNX inference and return label + confidence."""
    session  = ort.InferenceSession(ONNX_PATH)
    in_names = [inp.name for inp in session.get_inputs()]

    rgb, fft = preprocess(image_path)
    inputs   = {in_names[0]: rgb, in_names[1]: fft}

    output = session.run(None, inputs)   # list of arrays
    logit  = float(output[0][0][0])      # scalar logit

    # Sigmoid
    prob = 1 / (1 + np.exp(-logit))

    label      = "AI GENERATED" if prob >= 0.5 else "REAL IMAGE"
    confidence = prob if prob >= 0.5 else 1 - prob

    return {"label": label, "confidence": round(confidence * 100, 2), "fake_prob": round(prob, 4)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_onnx.py <image_path>")
        sys.exit(1)

    result = predict(sys.argv[1])
    print(f"Prediction : {result['label']}")
    print(f"Confidence : {result['confidence']}%")
    print(f"Fake prob  : {result['fake_prob']}")
