"""Marshmallow schemas for request validation and response serialization."""

from marshmallow import Schema, ValidationError, fields, validate, validates


class ItemCreateSchema(Schema):
    """Schema for validating POST /items request body."""

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        metadata={"description": "Unique item name (1-255 chars)"},
    )
    description = fields.Str(
        load_default=None,
        metadata={"description": "Optional free-text description"},
    )

    @validates("name")
    def validate_name_not_blank(self, value: str) -> None:
        if not value.strip():
            raise ValidationError("Name cannot be blank or whitespace.")


class ItemUpdateSchema(Schema):
    """Schema for validating PUT /items/<id> request body."""

    name = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=255),
    )
    description = fields.Str(required=False, allow_none=True)
    is_active = fields.Bool(required=False)

    @validates("name")
    def validate_name_not_blank(self, value: str) -> None:
        if not value.strip():
            raise ValidationError("Name cannot be blank or whitespace.")


item_create_schema = ItemCreateSchema()
item_update_schema = ItemUpdateSchema()
