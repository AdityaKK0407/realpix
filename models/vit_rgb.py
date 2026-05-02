import timm
import torch.nn as nn


class ViTRGB(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
            num_classes=0,
            drop_path_rate=0.1,  # stochastic depth: randomly drop blocks during training
        )

    def forward(self, x):
        return self.model(x)
