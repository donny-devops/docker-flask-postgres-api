#!/bin/bash
# =============================================================================
# Docker container entrypoint
# Runs Flask-Migrate DB upgrade, then starts gunicorn.
# =============================================================================
set -euo pipefail

echo "[entrypoint] Running Flask-Migrate upgrade..."
flask db upgrade

echo "[entrypoint] Starting gunicorn on 0.0.0.0:5000..."
exec python -m gunicorn \
    --bind 0.0.0.0:5000 \
    --workers "${GUNICORN_WORKERS:-2}" \
    --threads "${GUNICORN_THREADS:-4}" \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    "app:create_app()"
