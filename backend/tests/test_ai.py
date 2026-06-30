def _auth_headers(client, email="tester@example.com"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "password123"})
    res = client.post("/api/v1/auth/login", data={"username": email, "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_generate_roadmap_requires_auth(client):
    res = client.post("/api/v1/ai/generate-roadmap", json={"field_name": "Rust Developer"})
    assert res.status_code == 401


def test_generate_roadmap_without_api_key_returns_503(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    headers = _auth_headers(client)
    res = client.post(
        "/api/v1/ai/generate-roadmap", json={"field_name": "Rust Developer"}, headers=headers
    )
    assert res.status_code == 503


def test_generate_roadmap_rejects_curated_field_name(client):
    headers = _auth_headers(client)
    res = client.post(
        "/api/v1/ai/generate-roadmap",
        json={"field_name": "python-developer"},
        headers=headers,
    )
    assert res.status_code == 400


def test_chat_requires_auth(client):
    res = client.post("/api/v1/ai/chat", json={"message": "hello"})
    assert res.status_code == 401


def test_summarize_requires_auth(client):
    res = client.post(
        "/api/v1/ai/summarize", json={"field_id": "python-developer", "topic_id": "py-syntax"}
    )
    assert res.status_code == 401


def test_semantic_search_finds_asyncio_topic(client):
    res = client.get("/api/v1/search/semantic?q=asyncio")
    assert res.status_code == 200
    body = res.json()
    assert body["result_count"] >= 1
    assert any(r["topic"]["id"] == "py-concurrency" for r in body["results"])


def test_semantic_search_short_query_rejected(client):
    res = client.get("/api/v1/search/semantic?q=a")
    assert res.status_code == 422  # min_length=2 on the query param


def test_quiz_requires_auth(client):
    res = client.post(
        "/api/v1/ai/quiz", json={"field_id": "python-developer", "topic_id": "py-syntax"}
    )
    assert res.status_code == 401


def test_quiz_unknown_topic_404(client, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-test")
    headers = _auth_headers(client)
    res = client.post(
        "/api/v1/ai/quiz",
        json={"field_id": "python-developer", "topic_id": "does-not-exist"},
        headers=headers,
    )
    assert res.status_code == 404


def test_resume_bullets_requires_auth(client):
    res = client.post("/api/v1/ai/resume-bullets", json={"field_id": "python-developer"})
    assert res.status_code == 401


def test_resume_bullets_requires_completed_topics(client):
    headers = _auth_headers(client)
    res = client.post(
        "/api/v1/ai/resume-bullets", json={"field_id": "python-developer"}, headers=headers
    )
    assert res.status_code == 400


def test_regenerate_requires_auth(client):
    res = client.post("/api/v1/ai/generated/some-field/regenerate")
    assert res.status_code == 401


def test_regenerate_unknown_field_404(client):
    headers = _auth_headers(client)
    res = client.post("/api/v1/ai/generated/does-not-exist/regenerate", headers=headers)
    assert res.status_code == 404


def test_delete_generated_requires_auth(client):
    res = client.delete("/api/v1/ai/generated/some-field")
    assert res.status_code == 401
