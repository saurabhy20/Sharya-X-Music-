FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install without TgCrypto (slower but works)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    pyrogram==2.0.106 \
    pytgcalls==3.0.0.dev24 \
    yt-dlp==2023.3.4 \
    python-dotenv==0.19.0 \
    ffmpeg-python==0.2.0

CMD ["python", "bot.py"]
