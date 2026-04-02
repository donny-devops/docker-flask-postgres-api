"""API route handlers for the /api/v1 blueprint."""
from flask import Blueprint, Response, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Item
from app.schemas import item_create_schema, item_update_schema

api_bp = Blueprint("api", __name__)


@api_bp.get("/items")
def list_items() -> Response:
    """Return all active items, newest first."""
    items = Item.query.filter_by(is_active=True).order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])


@api_bp.get("/items/<int:item_id>")
def get_item(item_id: int) -> Response:
    """Return a single item by ID (active or inactive)."""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    return jsonify(item.to_dict())


@api_bp.post("/items")
def create_item() -> tuple[Response, int]:
    """Create a new item. Body: {name, description?}"""
    raw = request.get_json(silent=True)
    if raw is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        data = item_create_schema.load(raw)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "details": exc.messages}), 422

    item = Item(name=data["name"].strip(), description=data.get("description"))
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Item with name '{data['name']}' already exists"}), 409

    return jsonify(item.to_dict()), 201


@api_bp.put("/items/<int:item_id>")
def update_item(item_id: int) -> Response:
    """Update an existing item. Body: {name?, description?, is_active?}"""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    raw = request.get_json(silent=True)
    if raw is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        data = item_update_schema.load(raw)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "details": exc.messages}), 422

    if "name" in data:
        item.name = data["name"].strip()
    if "description" in data:
        item.description = data["description"]
    if "is_active" in data:
        item.is_active = data["is_active"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Item with name '{item.name}' already exists"}), 409

    return jsonify(item.to_dict())


@api_bp.delete("/items/<int:item_id>")
def delete_item(item_id: int) -> Response:
    """Soft-delete an item (sets is_active=False)."""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    item.is_active = False
    db.session.commit()
    return jsonify({"message": f"Item {item_id} deleted", "id": item_id})
