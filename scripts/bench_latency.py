#!/usr/bin/env python3
import argparse, time, statistics as stats
from src.hidden_guard.pipeline import HiddenGuardPipeline
from rich import print

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--iters", type=int, default=25)
    ap.add_argument("--warmup", type=int, default=5)
    args = ap.parse_args()

    pipe = HiddenGuardPipeline()
    times = []
    # warmup
    for _ in range(args.warmup):
        pipe.scan(args.image, args.text)

    for _ in range(args.iters):
        t0 = time.perf_counter()
        pipe.scan(args.image, args.text)
        times.append((time.perf_counter() - t0) * 1000.0)

    print({
        "iters": args.iters,
        "mean_ms": round(stats.mean(times), 3),
        "p50_ms": round(stats.median(times), 3),
        "p90_ms": round(stats.quantiles(times, n=10)[8], 3),
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3)
    })

if __name__ == "__main__":
    main()
