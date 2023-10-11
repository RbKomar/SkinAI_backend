import cv2
import numpy as np
from faker import Faker
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

fake = Faker()


def test_upload_image_endpoint_with_valid_data():
    # Register a user
    user = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=8),
    }
    register_response = client.post("/register", json=user)
    assert register_response.status_code == 200

    # Log in
    login_response = client.post(
        "/login", data={"username": user["username"], "password": user["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    fake_image = np.random.randint(0, 255, (15, 15, 3), dtype=np.uint8)
    image_bytes = cv2.imencode(".jpg", fake_image)[1].tobytes()

    # Arrange
    files = {
        "image": ("image1.jpg", image_bytes, "image/jpeg"),
        "description": (None, "Image 1"),
    }

    # Act
    response = client.post("/image/upload", headers=headers, files=files)
    print(response.json())

    # Assert
    assert response.status_code == 200
    assert response.json()["description"] == "Image 1"
    assert isinstance(response.json()["malignancy_percentage"], int)
