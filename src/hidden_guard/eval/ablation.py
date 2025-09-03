from __future__ import annotations
import argparse, json
from ..pipeline import HiddenGuardPipeline
from ..wsd import WaveletStegoDetector
from ..cmca import CrossModalConsistencyAnalyzer
from ..cata import ContextAwareThreatAssessor

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--text", required=True)
    args = ap.parse_args()

    pipe = HiddenGuardPipeline()
    res_full = pipe.scan(args.image, args.text)

    cmca = CrossModalConsistencyAnalyzer()
    wsd = WaveletStegoDetector()
    cata = ContextAwareThreatAssessor()

    sim = cmca.similarity(args.image, args.text)
    wsd_score, feats = wsd.score(args.image)
    res_cata = cata.assess(sim, wsd_score)

    print(json.dumps({
        "ablation": {
            "full_pipeline": res_full,
            "cmca_similarity_only": sim,
            "wsd_only": wsd_score,
            "cata_fused": res_cata
        }
    }, indent=2))

if __name__ == "__main__":
    main()
