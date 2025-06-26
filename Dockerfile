FROM python:3.9

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY repo /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
