import os


class Config:
    """Base configuration loaded from environment variables."""

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-not-for-production")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        "postgresql://appuser:apppassword@localhost:5432/appdb",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


class TestingConfig(Config):
    """Testing configuration with SQLite in-memory database."""

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    SECRET_KEY: str = "test-secret-key"
