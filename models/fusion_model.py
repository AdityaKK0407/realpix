import torch
import torch.nn as nn
from models.vit_rgb import ViTRGB
from models.fft_branch import FFTBranch


class FusionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rgb = ViTRGB()
        self.fft = FFTBranch()

        self.classifier = nn.Sequential(
            nn.Linear(768 + 64, 256),
            nn.ReLU(),
            nn.Dropout(0.4),   # regularise: drop 40% of neurons during training
            nn.Linear(256, 1)
        )

    def forward(self, rgb, fft):
        rgb_feat = self.rgb(rgb)
        fft_feat = self.fft(fft)

        fused = torch.cat([rgb_feat, fft_feat], dim=1)
        fused = nn.functional.normalize(fused, dim=1)

        return self.classifier(fused)
