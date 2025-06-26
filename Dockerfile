FROM python:3.9  # Full image includes gcc and build tools

WORKDIR /app

COPY repo /app

RUN if [ -f "/app/requirements.txt" ]; then \
    pip install --no-cache-dir -r /app/requirements.txt; \
    fi
