import pytest
from starlette.testclient import TestClient

from app.database.db_manager import clear_users
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")
def cleanup():
    yield  # This line makes sure the tests run before the cleanup code
    clear_users(['john_doe', 'jane_smith'])


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("john_doe", "john_doe@example.com", "password123"),
        ("jane_smith", "jane_smith@example.com", "password456"),
    ],
    ids=["valid_username_email_password_1", "valid_username_email_password_2"]
)
def test_register_user_with_valid_data(username, email, password):
    # Arrange
    user = {"username": username, "email": email, "password": password}

    # Act
    response = client.post("/register", json=user)

    # Assert
    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["email"] == email


@pytest.mark.parametrize(
    "username, password",
    [
        ("john_doe", "password123"),  # Test with valid username and password
        ("jane_smith", "password456"),  # Test with valid username and password
    ],
    ids=["valid_username_password_1", "valid_username_password_2"]
)
def test_login_with_valid_credentials(username, password):
    # Act
    response = client.post("/login", data={"username": username, "password": password})

    # Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
