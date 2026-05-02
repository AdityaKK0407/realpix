"""
export_onnx.py — Export DualBranchModel to ONNX
------------------------------------------------
Converts deepfake_model.pt to deepfake_model.onnx

Run:
    python export_onnx.py
"""

import torch
from model import DualBranchModel

MODEL_PATH = "deepfake_model.pt"
ONNX_PATH = "deepfake_model.onnx"
DEVICE = torch.device("cpu")


def load_checkpoint(model, path):
    checkpoint = torch.load(path, map_location=DEVICE)

    # Case 1: saved directly using torch.save(model.state_dict(), path)
    if isinstance(checkpoint, dict) and all(
        isinstance(k, str) for k in checkpoint.keys()
    ):
        # Case 2: checkpoint dictionary containing state_dict
        if "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        elif "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
        else:
            state_dict = checkpoint
    else:
        raise ValueError("Unsupported checkpoint format. Expected state_dict or checkpoint dict.")

    # Remove 'module.' if trained with DataParallel
    cleaned_state_dict = {}
    for k, v in state_dict.items():
        new_key = k.replace("module.", "")
        cleaned_state_dict[new_key] = v

    model.load_state_dict(cleaned_state_dict, strict=True)
    return model


def main():
    model = DualBranchModel().to(DEVICE)
    model = load_checkpoint(model, MODEL_PATH)
    model.eval()

    print(f"Loaded model from: {MODEL_PATH}")

    dummy_rgb = torch.randn(1, 3, 224, 224, device=DEVICE)
    dummy_fft = torch.randn(1, 1, 224, 224, device=DEVICE)

    # Test forward pass before export
    with torch.no_grad():
        output = model(dummy_rgb, dummy_fft)

    print("Forward pass successful.")
    print("Model output type:", type(output))

    if isinstance(output, (tuple, list)):
        print("Warning: model returns tuple/list. ONNX will export all outputs unless you handle it.")
        print("Output shapes:", [o.shape for o in output])
    else:
        print("Output shape:", output.shape)

    torch.onnx.export(
        model,
        (dummy_rgb, dummy_fft),
        ONNX_PATH,
        input_names=["rgb", "fft"],
        output_names=["logit"],
        dynamic_axes={
            "rgb": {0: "batch_size"},
            "fft": {0: "batch_size"},
            "logit": {0: "batch_size"},
        },
        opset_version=17,
        do_constant_folding=True,
    )

    print(f"ONNX model exported successfully to: {ONNX_PATH}")
    print("Inputs:")
    print("  rgb: (batch_size, 3, 224, 224)")
    print("  fft: (batch_size, 1, 224, 224)")
    print("Output:")
    print("  logit: apply sigmoid(logit) to get probability")


if __name__ == "__main__":
    main()