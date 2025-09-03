from __future__ import annotations
import torch
import open_clip
from PIL import Image
import numpy as np
from typing import Tuple

class CrossModalConsistencyAnalyzer:
    """
    CLIP-based image-text cosine similarity. Returns a score in [0, 1].
    """
    def __init__(self, model_name: str = "ViT-B-32", pretrained: str = "openai", device: str = "auto"):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained, device=self.device)
        self.tokenizer = open_clip.get_tokenizer(model_name)

    @torch.no_grad()
    def similarity(self, image_path: str, text: str) -> float:
        image = self.preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(self.device)
        text_tokens = self.tokenizer([text]).to(self.device)

        image_features = self.model.encode_image(image)
        text_features = self.model.encode_text(text_tokens)

        # Normalize
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features  /= text_features.norm(dim=-1, keepdim=True)

        cos_sim = (image_features @ text_features.T).squeeze().item()
        # clip outputs are roughly in [-1, 1]; map to [0,1]
        score = (cos_sim + 1.0) / 2.0
        return float(max(0.0, min(1.0, score)))
