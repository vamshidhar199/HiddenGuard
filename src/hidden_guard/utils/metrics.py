from __future__ import annotations
def normalize01(x: float, lo: float, hi: float) -> float:
    if hi == lo:
        return 0.0
    v = (x - lo) / (hi - lo)
    return max(0.0, min(1.0, float(v)))
