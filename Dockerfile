# ---------- Base ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ---------- System deps ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Python deps ----------
COPY django-api/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# ---------- Project files ----------
COPY django-api /app/
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# ---------- Directories & permissions ----------
# Create the directories that will be used by volumes
RUN mkdir -p /app/staticfiles /app/media && \
    # Give ownership to the non-root user (UID 1000)
    chown -R 1000:1000 /app

# ---------- Non-root user ----------
RUN useradd -m -u 1000 django && \
    chown -R django:django /app
USER django

# ---------- Healthcheck ----------
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

EXPOSE 8000

# Gunicorn is started from the entrypoint script
