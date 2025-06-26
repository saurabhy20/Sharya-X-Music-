FROM python:3.9-slim

WORKDIR /app

# Install build tools for tgcrypto and ffmpeg for audio
RUN apt-get update && \
    apt-get install -y gcc ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY repo /app

RUN if [ -f "/app/requirements.txt" ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

CMD ["python", "main.py"]
