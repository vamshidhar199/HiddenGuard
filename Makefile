setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api:
\tuvicorn src.hidden_guard.api.app:app --reload --host 0.0.0.0 --port 8000

scan:
\tpython scripts/scan_image.py --image data/samples/stego_message.png --text "abstract pattern"
