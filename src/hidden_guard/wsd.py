from __future__ import annotations
import numpy as np
import pywt
import cv2
from skimage.feature import graycomatrix, graycoprops
from typing import Dict, Tuple

def _kurtosis(x: np.ndarray) -> float:
    # Fisher's definition (excess kurtosis); add small eps for stability
    x = x.astype(np.float64).ravel()
    n = x.size
    if n < 4:
        return 0.0
    mean = x.mean()
    m2 = np.mean((x - mean) ** 2) + 1e-12
    m4 = np.mean((x - mean) ** 4) + 1e-12
    g2 = m4 / (m2**2) - 3.0
    return float(g2)

class WaveletStegoDetector:
    """
    Wavelet-based steganalysis on HH/HL/LH sub-bands + GLCM contrasts.
    Produces a score in [0,1] where higher implies more suspicious.
    """
    def __init__(self, wavelet: str = "db8", levels: int = 2):
        self.wavelet = wavelet
        self.levels = int(levels)

    def _wavelet_features(self, gray: np.ndarray) -> Dict[str, float]:
        coeffs = pywt.wavedec2(gray, self.wavelet, level=self.levels)
        # coeffs: (LL, (LH, HL, HH), ...)
        features = {}
        for lvl in range(1, len(coeffs)):
            (cLH, cHL, cHH) = coeffs[lvl]
            features[f"kurtosis_HH_l{lvl}"] = _kurtosis(cHH)
            features[f"kurtosis_HL_l{lvl}"] = _kurtosis(cHL)
            features[f"kurtosis_LH_l{lvl}"] = _kurtosis(cLH)
        return features

    def _glcm_contrast(self, gray: np.ndarray) -> float:
        # Reduce to 8-bit and 32 levels to keep GLCM tractable
        if gray.dtype != np.uint8:
            gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        gray_q = (gray // 8).astype(np.uint8)  # 32 gray levels
        glcm = graycomatrix(gray_q, distances=[1,2,4], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=32, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast').mean()
        return float(contrast)

    def score(self, image_path: str) -> Tuple[float, dict]:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(image_path)

        feats = self._wavelet_features(img)
        feats["glcm_contrast"] = self._glcm_contrast(img)

        # Robust z-score normalization against plausible natural-image priors
        # For a demo, we use heuristic ranges; in production fit on clean data.
        kurt_vals = np.array([feats[k] for k in feats if k.startswith("kurtosis_")], dtype=np.float64)
        # Natural image sub-bands often have negative excess kurtosis around [-1, 1]
        kurt_norm = np.clip((np.abs(kurt_vals) / 2.0), 0.0, 3.0)  # heuristic
        contrast_norm = min(3.0, feats["glcm_contrast"] / 50.0)

        # Combine
        suspicious = float(np.tanh(0.6 * (kurt_norm.mean() + contrast_norm)))
        return suspicious, feats
