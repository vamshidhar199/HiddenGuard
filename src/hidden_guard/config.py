from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class HiddenGuardConfig(BaseModel):
    model_clip_name: str = "ViT-B-32"
    model_clip_pretrained: str = "openai"

    # WSD params
    wavelet: str = "db8"
    levels: int = 2
    kurtosis_z_thresh: float = 2.5
    glcm_contrast_z_thresh: float = 2.0

    # CMCA params
    similarity_low_thresh: float = 0.18
    similarity_high_bypass: float = 0.37

    # CATA params
    suspicious_score: float = 0.5
    critical_score: float = 0.75

    device: str = "auto"
