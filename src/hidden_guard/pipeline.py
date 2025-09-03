from __future__ import annotations
import yaml
from pathlib import Path
from typing import Optional, Dict

from .cmca import CrossModalConsistencyAnalyzer
from .wsd import WaveletStegoDetector
from .cata import ContextAwareThreatAssessor

class HiddenGuardPipeline:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).resolve().parents[2] / "configs" / "default.yaml")
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.cmca = CrossModalConsistencyAnalyzer(
            model_name=cfg["model"]["clip_name"],
            pretrained=cfg["model"]["clip_pretrained"],
            device=cfg["runtime"]["device"]
        )
        self.wsd = WaveletStegoDetector(
            wavelet=cfg["wsd"]["wavelet"],
            levels=cfg["wsd"]["levels"]
        )
        self.cata = ContextAwareThreatAssessor(
            suspicious_score=cfg["cata"]["suspicious_score"],
            critical_score=cfg["cata"]["critical_score"]
        )
        self.sim_low = float(cfg["cmca"]["similarity_low_thresh"])
        self.sim_bypass = float(cfg["cmca"]["similarity_high_bypass"])

    def scan(self, image_path: str, text: str) -> Dict:
        sim = self.cmca.similarity(image_path, text)

        if sim >= self.sim_bypass:
            # Very likely aligned; short-circuit as SAFE
            return {
                "risk_score": 0.0,
                "risk_level": "SAFE",
                "action": "ALLOW",
                "components": {"cmca_similarity": float(sim), "wsd_score": 0.0},
                "note": "High alignment bypass"
            }

        wsd_score, feats = self.wsd.score(image_path)
        result = self.cata.assess(sim, wsd_score)
        result["wsd_features"] = feats
        return result
