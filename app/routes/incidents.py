from flask import Blueprint, jsonify, request, abort
from marshmallow import ValidationError
from sqlalchemy import asc

from app.extensions import db
from app.models.incident import Incident, Status, Severity
from app.schemas.incident import incident_schema, incidents_schema

incidents_bp = Blueprint("incidents", __name__, url_prefix="/api/v1/incidents")


@incidents_bp.get("")
def list_incidents():
    query = db.select(Incident)

    status = request.args.get("status")
    severity = request.args.get("severity")
    if status:
        try:
            query = query.where(Incident.status == Status(status))
        except ValueError:
            abort(400, description=f"Invalid status '{status}'")
    if severity:
        try:
            query = query.where(Incident.severity == Severity(severity))
        except ValueError:
            abort(400, description=f"Invalid severity '{severity}'")

    query = query.order_by(asc(Incident.created_at))

    try:
        page = int(request.args.get("page", 1))
        per_page = min(int(request.args.get("per_page", 20)), 100)
    except ValueError:
        abort(400, description="page and per_page must be integers")

    total = db.session.execute(
        db.select(db.func.count()).select_from(query.subquery())
    ).scalar()
    items = db.session.execute(
        query.offset((page - 1) * per_page).limit(per_page)
    ).scalars().all()

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "items": incidents_schema.dump(items),
    }), 200


@incidents_bp.post("")
def create_incident():
    data = request.get_json(silent=True) or {}
    try:
        validated = incident_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 422

    incident = Incident(**validated)
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident_schema.dump(incident)), 201


@incidents_bp.get("/<uuid:incident_id>")
def get_incident(incident_id):
    incident = db.get_or_404(Incident, incident_id)
    return jsonify(incident_schema.dump(incident)), 200


@incidents_bp.patch("/<uuid:incident_id>")
def patch_incident(incident_id):
    incident = db.get_or_404(Incident, incident_id)
    data = request.get_json(silent=True) or {}

    try:
        validated = incident_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 422

    transitioning_to_resolved = (
        "status" in validated and validated["status"] == Status.resolved.value
        and incident.status != Status.resolved
    )

    for key, value in validated.items():
        setattr(incident, key, value)

    if transitioning_to_resolved:
        incident.resolve()

    db.session.commit()
    return jsonify(incident_schema.dump(incident)), 200


@incidents_bp.put("/<uuid:incident_id>")
def put_incident(incident_id):
    incident = db.get_or_404(Incident, incident_id)
    data = request.get_json(silent=True) or {}

    try:
        validated = incident_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 422

    for key, value in validated.items():
        setattr(incident, key, value)

    db.session.commit()
    return jsonify(incident_schema.dump(incident)), 200


@incidents_bp.delete("/<uuid:incident_id>")
def delete_incident(incident_id):
    incident = db.get_or_404(Incident, incident_id)
    db.session.delete(incident)
    db.session.commit()
    return "", 204
