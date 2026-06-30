'''def test_register_and_get_token(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "[email protected]", "full_name": "Jane Dev", "password": "password123"},
    )
    assert res.status_code == 201
    body = res.json()
    assert "access_token" in body
    assert body["user"]["email"] == "[email protected]" '''

def test_register_and_get_token(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "jane@example.com",
            "full_name": "Jane Dev",
            "password": "password123",
        },
    )

    print("Status:", res.status_code)
    print("Response:", res.json())   # <-- Add this

    assert res.status_code == 201


def test_register_duplicate_email_fails(client):
    payload = {"email": "jane@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    res = client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 400


def test_login_with_correct_credentials(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "jane@example.com", "password": "password123"},
    )
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "jane@example.com", "password": "password123"},
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "[email protected]", "password": "password123"},
    )
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "[email protected]", "password": "wrongpass"},
    )
    assert res.status_code == 401


def test_me_requires_token(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
