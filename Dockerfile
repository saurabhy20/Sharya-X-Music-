FROM python:3.9-slim

# 1. Install minimal build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy requirements first for layer caching
COPY requirements.txt .

# 3. Install with explicit wheel support
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir --only-binary :all: TgCrypto && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy application files
COPY . .

CMD ["python", "bot.py"]
