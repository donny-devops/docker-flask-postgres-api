import json


INCIDENT_PAYLOAD = {
    "title": "Database connection timeout",
    "description": "Primary DB is refusing connections intermittently.",
    "severity": "high",
    "reported_by": "ops-team",
}


def test_health(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_create_incident(client):
    res = client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == INCIDENT_PAYLOAD["title"]
    assert data["status"] == "open"
    assert data["id"] is not None


def test_list_incidents(client):
    client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    res = client.get("/api/v1/incidents")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_incident(client):
    create_res = client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    incident_id = create_res.get_json()["id"]
    res = client.get(f"/api/v1/incidents/{incident_id}")
    assert res.status_code == 200
    assert res.get_json()["id"] == incident_id


def test_patch_incident(client):
    create_res = client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    incident_id = create_res.get_json()["id"]
    res = client.patch(
        f"/api/v1/incidents/{incident_id}",
        data=json.dumps({"status": "investigating", "assigned_to": "jane-doe"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "investigating"
    assert data["assigned_to"] == "jane-doe"


def test_resolve_incident_sets_resolved_at(client):
    create_res = client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    incident_id = create_res.get_json()["id"]
    res = client.patch(
        f"/api/v1/incidents/{incident_id}",
        data=json.dumps({"status": "resolved"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.get_json()["resolved_at"] is not None


def test_delete_incident(client):
    create_res = client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    incident_id = create_res.get_json()["id"]
    res = client.delete(f"/api/v1/incidents/{incident_id}")
    assert res.status_code == 204
    get_res = client.get(f"/api/v1/incidents/{incident_id}")
    assert get_res.status_code == 404


def test_filter_by_severity(client):
    client.post(
        "/api/v1/incidents",
        data=json.dumps(INCIDENT_PAYLOAD),
        content_type="application/json",
    )
    client.post(
        "/api/v1/incidents",
        data=json.dumps({**INCIDENT_PAYLOAD, "severity": "low"}),
        content_type="application/json",
    )
    res = client.get("/api/v1/incidents?severity=high")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 1
    assert data["items"][0]["severity"] == "high"


def test_create_incident_missing_required_fields(client):
    res = client.post(
        "/api/v1/incidents",
        data=json.dumps({"title": "Missing severity and reporter"}),
        content_type="application/json",
    )
    assert res.status_code == 422


def test_get_nonexistent_incident(client):
    res = client.get("/api/v1/incidents/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 404
