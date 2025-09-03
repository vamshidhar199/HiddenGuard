#!/usr/bin/env python3
import argparse, json
from src.hidden_guard.pipeline import HiddenGuardPipeline
from rich import print

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="Path to image")
    ap.add_argument("--text", required=True, help="Reference text/caption")
    ap.add_argument("--config", default="configs/default.yaml")
    args = ap.parse_args()

    pipe = HiddenGuardPipeline(args.config)
    result = pipe.scan(args.image, args.text)
    print(result)

if __name__ == "__main__":
    main()
