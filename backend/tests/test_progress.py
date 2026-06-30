def _auth_headers(client, email="[email protected]"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "password123"})
    res = client.post("/api/v1/auth/login", data={"username": email, "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_toggle_topic_complete_and_incomplete(client):
    headers = _auth_headers(client)
    payload = {"field_id": "python-developer", "topic_id": "py-syntax"}

    res = client.post("/api/v1/progress/toggle", json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["completed"] is True

    res = client.post("/api/v1/progress/toggle", json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["completed"] is False


def test_progress_unknown_field_404(client):
    headers = _auth_headers(client)
    res = client.post(
        "/api/v1/progress/toggle",
        json={"field_id": "nope", "topic_id": "x"},
        headers=headers,
    )
    assert res.status_code == 404


def test_get_field_progress(client):
    headers = _auth_headers(client)
    client.post(
        "/api/v1/progress/toggle",
        json={"field_id": "python-developer", "topic_id": "py-syntax"},
        headers=headers,
    )
    res = client.get("/api/v1/progress/python-developer", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["completed_count"] == 1


def test_progress_requires_auth(client):
    res = client.get("/api/v1/progress/python-developer")
    assert res.status_code == 401
