# Minimal runtime image (requires GPU drivers for CUDA if desired)
FROM python:3.10-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000
CMD ["uvicorn", "src.hidden_guard.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
