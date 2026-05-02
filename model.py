"""
model.py — DualBranchModel
--------------------------
Thin wrapper that re-exports FusionModel (ViT-B/16 RGB + FFT CNN)
as the canonical model for the RealPix pipeline.

Output: single logit per sample (use BCEWithLogitsLoss for training,
        sigmoid for inference).
"""

from models.fusion_model import FusionModel

# Canonical name used throughout the pipeline
DualBranchModel = FusionModel