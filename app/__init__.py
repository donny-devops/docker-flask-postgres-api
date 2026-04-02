import os
from flask import Flask
from dotenv import load_dotenv

from app.config import config
from app.extensions import db, migrate, ma
from app.errors import register_error_handlers

load_dotenv()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.routes import incidents_bp, health_bp
    app.register_blueprint(incidents_bp)
    app.register_blueprint(health_bp)

    register_error_handlers(app)

    return app
