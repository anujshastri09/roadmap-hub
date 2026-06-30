def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_list_fields(client):
    res = client.get("/api/v1/fields")
    assert res.status_code == 200
    fields = res.json()
    assert len(fields) == 5
    ids = {f["id"] for f in fields}
    assert "python-developer" in ids


def test_get_single_field(client):
    res = client.get("/api/v1/fields/python-developer")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Python Developer"
    assert len(data["stages"]) > 0


def test_get_unknown_field_returns_404(client):
    res = client.get("/api/v1/fields/does-not-exist")
    assert res.status_code == 404


def test_search_finds_fastapi_topic(client):
    res = client.get("/api/v1/search?q=fastapi")
    assert res.status_code == 200
    body = res.json()
    assert body["result_count"] >= 1


def test_stats_endpoint(client):
    res = client.get("/api/v1/stats")
    assert res.status_code == 200
    body = res.json()
    assert body["field_count"] == 5
    assert body["topic_count"] > 0
