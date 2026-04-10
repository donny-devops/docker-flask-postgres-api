from flask import Flask

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class: type = Config) -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import api_bp  # noqa: PLC0415

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Health check endpoint (outside blueprint for simplicity)
    @app.get("/health")
    def health() -> dict:  # type: ignore[return]
        return {"status": "healthy", "service": "docker-flask-postgres-api"}

    return app
