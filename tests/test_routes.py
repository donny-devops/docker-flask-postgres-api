import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app() -> Flask:
    """Create application for testing."""
    flask_app = create_app(TestingConfig)
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture(autouse=True)
def clean_db(app: Flask) -> None:
    """Truncate tables between tests."""
    with app.app_context():
        from app.models import Item
        _db.session.query(Item).delete()
        _db.session.commit()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


# ── Health Check ──────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json["status"] == "healthy"


# ── List Items ─────────────────────────────────────────────────────────────────

class TestListItems:
    def test_empty_list(self, client: FlaskClient) -> None:
        resp = client.get("/api/v1/items")
        assert resp.status_code == 200
        assert resp.json == []

    def test_returns_active_items_only(self, client: FlaskClient) -> None:
        client.post("/api/v1/items", json={"name": "active-item"})
        created = client.post("/api/v1/items", json={"name": "to-delete"}).json
        client.delete(f"/api/v1/items/{created['id']}")

        resp = client.get("/api/v1/items")
        assert resp.status_code == 200
        names = [i["name"] for i in resp.json]
        assert "active-item" in names
        assert "to-delete" not in names


# ── Create Item ────────────────────────────────────────────────────────────────

class TestCreateItem:
    def test_create_success(self, client: FlaskClient) -> None:
        resp = client.post(
            "/api/v1/items",
            json={"name": "widget", "description": "A test widget"},
        )
        assert resp.status_code == 201
        assert resp.json["name"] == "widget"
        assert resp.json["description"] == "A test widget"
        assert resp.json["is_active"] is True
        assert "id" in resp.json

    def test_create_missing_name(self, client: FlaskClient) -> None:
        resp = client.post("/api/v1/items", json={"description": "no name"})
        assert resp.status_code == 400

    def test_create_blank_name(self, client: FlaskClient) -> None:
        resp = client.post("/api/v1/items", json={"name": "   "})
        assert resp.status_code == 400

    def test_create_duplicate_name(self, client: FlaskClient) -> None:
        client.post("/api/v1/items", json={"name": "dup"})
        resp = client.post("/api/v1/items", json={"name": "dup"})
        assert resp.status_code == 409

    def test_create_no_body(self, client: FlaskClient) -> None:
        resp = client.post("/api/v1/items", content_type="application/json", data="bad-json")
        assert resp.status_code == 400


# ── Get Item ───────────────────────────────────────────────────────────────────

class TestGetItem:
    def test_get_existing(self, client: FlaskClient) -> None:
        created = client.post("/api/v1/items", json={"name": "find-me"}).json
        resp = client.get(f"/api/v1/items/{created['id']}")
        assert resp.status_code == 200
        assert resp.json["name"] == "find-me"

    def test_get_not_found(self, client: FlaskClient) -> None:
        resp = client.get("/api/v1/items/99999")
        assert resp.status_code == 404


# ── Update Item ────────────────────────────────────────────────────────────────

class TestUpdateItem:
    def test_update_name(self, client: FlaskClient) -> None:
        created = client.post("/api/v1/items", json={"name": "old-name"}).json
        resp = client.put(f"/api/v1/items/{created['id']}", json={"name": "new-name"})
        assert resp.status_code == 200
        assert resp.json["name"] == "new-name"

    def test_update_not_found(self, client: FlaskClient) -> None:
        resp = client.put("/api/v1/items/99999", json={"name": "x"})
        assert resp.status_code == 404


# ── Delete Item ────────────────────────────────────────────────────────────────

class TestDeleteItem:
    def test_soft_delete(self, client: FlaskClient) -> None:
        created = client.post("/api/v1/items", json={"name": "bye"}).json
        resp = client.delete(f"/api/v1/items/{created['id']}")
        assert resp.status_code == 200

        # Confirm it no longer appears in active list
        items = client.get("/api/v1/items").json
        assert not any(i["id"] == created["id"] for i in items)

    def test_delete_not_found(self, client: FlaskClient) -> None:
        resp = client.delete("/api/v1/items/99999")
        assert resp.status_code == 404
