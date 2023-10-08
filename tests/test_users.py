from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user():
    # clear DB
    client.delete("/user/testuser/")
    response = client.post("/user/", json={"username": "testuser", "email": "test@test.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@test.com"
    # We no longer expect the token in the response of the create user endpoint
    assert "token" not in response.json()


def test_login_user():
    response = client.post("/login", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
