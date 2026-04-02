from marshmallow import fields, validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.extensions import ma
from app.models.incident import Incident, Severity, Status

VALID_SEVERITIES = [s.value for s in Severity]
VALID_STATUSES = [s.value for s in Status]


class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident
        load_instance = False
        include_fk = True

    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    resolved_at = fields.DateTime(dump_only=True)

    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    severity = fields.String(required=True, validate=validate.OneOf(VALID_SEVERITIES))
    status = fields.String(validate=validate.OneOf(VALID_STATUSES))
    reported_by = fields.String(required=True, validate=validate.Length(min=1, max=100))
    assigned_to = fields.String(allow_none=True, validate=validate.Length(max=100))


incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)
