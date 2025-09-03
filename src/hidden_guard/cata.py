from __future__ import annotations
from typing import Dict

class ContextAwareThreatAssessor:
    """
    Fuse CMCA and WSD scores into tri-level risk with tunable thresholds.
    """
    def __init__(self, suspicious_score: float = 0.5, critical_score: float = 0.75):
        self.suspicious_score = float(suspicious_score)
        self.critical_score = float(critical_score)

    def assess(self, cmca_sim: float, wsd_score: float) -> Dict:
        # Lower similarity => more suspicious; invert it
        cmca_susp = 1.0 - cmca_sim
        # Blend (simple average; can be weighted via config)
        final = 0.5 * cmca_susp + 0.5 * wsd_score

        if final >= self.critical_score:
            level = "CRITICAL"
            action = "BLOCK"
        elif final >= self.suspicious_score:
            level = "SUSPICIOUS"
            action = "MONITOR"
        else:
            level = "SAFE"
            action = "ALLOW"

        return {
            "risk_score": round(float(final), 4),
            "risk_level": level,
            "action": action,
            "components": {
                "cmca_similarity": round(float(cmca_sim), 4),
                "wsd_score": round(float(wsd_score), 4)
            }
        }
