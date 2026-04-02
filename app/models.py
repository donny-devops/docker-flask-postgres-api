from datetime import UTC, datetime

from app.extensions import db


class Item(db.Model):
    """Represents a generic item resource."""

    __tablename__ = "items"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False, unique=True)
    description: str | None = db.Column(db.Text, nullable=True)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: datetime = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    def to_dict(self) -> dict:
        """Serialize the model to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name!r}>"
