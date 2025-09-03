# HiddenGuard

Real-time detection and mitigation framework for **steganographic prompt injection (SPI)** against Multimodal LLM (MLLM) pipelines.

This repository provides a lightweight, modular implementation of three core components:
1. **CMCA** — Cross-Modal Consistency Analyzer (CLIP-based image–text similarity)
2. **WSD** — Wavelet-based Steganographic Detector (frequency-domain features)
3. **CATA** — Context-Aware Threat Assessor (risk scoring + tri-level actions)

> Implements the ideas described in the paper “HiddenGuard: Real-Time Detection and Mitigation of Steganographic Prompt Injection Attacks in MLLMs.”

## Quickstart

### 1) Environment
```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Try the CLI scanner
```bash
# Safe vs stego samples are in data/samples
python scripts/scan_image.py --image data/samples/safe_noise.png --text "A noisy abstract pattern"
python scripts/scan_image.py --image data/samples/stego_message.png --text "A noisy abstract pattern"
```

### 3) Run the REST API
```bash
uvicorn src.hidden_guard.api.app:app --reload --host 0.0.0.0 --port 8000
# Then POST an image + text to http://localhost:8000/scan
```

### 4) Latency / ablations
```bash
python scripts/bench_latency.py --image data/samples/stego_message.png --text "abstract pattern" --iters 50
python -m src.hidden_guard.eval.ablation --image data/samples/stego_message.png --text "abstract pattern"
```

### Repo layout
```
src/hidden_guard/
  cmca.py   # CLIP image-text similarity
  wsd.py    # Wavelet-based stego detection
  cata.py   # Risk aggregation and thresholds
  pipeline.py
  api/app.py
  utils/stego_lsb.py  # for synthetic data generation
  utils/image_io.py
  utils/metrics.py
configs/default.yaml
scripts/scan_image.py
scripts/bench_latency.py
data/samples/  # small toy images and a stego example
tests/
```

### Notes
- CLIP weights will download on first run (internet required only once).
- The **sample images** are tiny toy examples for demonstration; use your own data or the scripts in `src/hidden_guard/eval` to generate more.
- For larger experiments, connect public benchmarks (e.g., JailBreakZoo, MM-SafetyBench) using your own credentials and storage.

## License
MIT
