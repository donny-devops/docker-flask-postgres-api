"""Application entry point for local development.

Usage:
    python run.py

For production, use gunicorn via docker-compose or the Dockerfile CMD.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
