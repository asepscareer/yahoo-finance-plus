FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd --create-home --shell /bin/bash appuser

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

ENV GOOGLE_CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

EXPOSE 8000

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]