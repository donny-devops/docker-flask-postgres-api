from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Item

api_bp = Blueprint("api", __name__)


@api_bp.get("/items")
def list_items() -> Response:
    """Return all active items."""
    items = Item.query.filter_by(is_active=True).order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])


@api_bp.get("/items/<int:item_id>")
def get_item(item_id: int) -> Response:
    """Return a single item by ID."""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    return jsonify(item.to_dict())


@api_bp.post("/items")
def create_item() -> tuple[Response, int]:
    """Create a new item."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name: str | None = data.get("name")
    if not name or not name.strip():
        return jsonify({"error": "Field 'name' is required and cannot be blank"}), 400

    item = Item(
        name=name.strip(),
        description=data.get("description"),
    )
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Item with name '{name}' already exists"}), 409

    return jsonify(item.to_dict()), 201


@api_bp.put("/items/<int:item_id>")
def update_item(item_id: int) -> Response:
    """Update an existing item."""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "name" in data:
        name = data["name"]
        if not name or not name.strip():
            return jsonify({"error": "Field 'name' cannot be blank"}), 400
        item.name = name.strip()

    if "description" in data:
        item.description = data["description"]

    if "is_active" in data:
        item.is_active = bool(data["is_active"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Item with name '{item.name}' already exists"}), 409

    return jsonify(item.to_dict())


@api_bp.delete("/items/<int:item_id>")
def delete_item(item_id: int) -> Response:
    """Soft-delete an item by setting is_active=False."""
    item = db.get_or_404(Item, item_id, description=f"Item {item_id} not found")
    item.is_active = False
    db.session.commit()
    return jsonify({"message": f"Item {item_id} deleted", "id": item_id})
