import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Severity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Status(str, enum.Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"
    closed = "closed"


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    severity = db.Column(db.Enum(Severity), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.open)
    reported_by = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    resolved_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def resolve(self):
        self.status = Status.resolved
        self.resolved_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Incident {self.id} [{self.severity}] {self.title!r}>"
