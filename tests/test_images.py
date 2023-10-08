from datetime import datetime, timedelta

import jwt

# sourcery skip: dont-import-test-modules
from tests.test_users import client

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def generate_mock_token(username: str):
    """Generate a mock JWT token for testing."""
    expiration = datetime.utcnow() + timedelta(days=1)
    to_encode = {"sub": username, "exp": expiration}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Update the test_process_image function:

def test_process_image():
    # Generate a mock token for a test user
    token = generate_mock_token("testuser")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    files = {"image_file": ("test_image.jpg", b"fake_image_content", "image/jpeg")}
    response = client.post("/image/", headers=headers, files=files, data={"description": "test image"})

    # Assertions
    assert response.status_code == 200
