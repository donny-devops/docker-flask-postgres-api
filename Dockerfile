# =============================================================================
# Multi-stage Dockerfile: builder -> runtime
# Python 3.12-slim, non-root user, gunicorn via entrypoint.sh
# =============================================================================

# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Build-time system deps (gcc for psycopg2 native compile)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="donny-devops" \
      org.opencontainers.image.title="docker-flask-postgres-api" \
      org.opencontainers.image.description="Production Flask + PostgreSQL REST API" \
      org.opencontainers.image.source="https://github.com/donny-devops/docker-flask-postgres-api"

# Runtime-only system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy app source
COPY --chown=appuser:appgroup . .

RUN chmod +x entrypoint.sh

# Drop privileges
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Entrypoint runs migrations then starts gunicorn
ENTRYPOINT ["./entrypoint.sh"]
