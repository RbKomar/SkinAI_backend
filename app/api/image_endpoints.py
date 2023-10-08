import random

from fastapi import APIRouter, Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.api.auth import get_current_user
from app.database.db_manager import insert_image, save_image_to_disk
from app.models.image import ImageUpload
from app.models.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def mock_malignancy_prediction(image_data: bytes) -> int:
    return random.randint(0, 100)


@router.post("/image/")
async def process_image(request: Request, image: ImageUpload, current_user: User = Depends(get_current_user)):
    # Logic for image processing
    malignancy_percentage = mock_malignancy_prediction(b"dummy_data")  # Passing dummy data for now
    return {"description": image.description, "malignancy_percentage": malignancy_percentage}


@router.post("/image/upload/")
@limiter.limit("5/minute")
async def upload_image_endpoint(request: Request, image: ImageUpload, current_user: User = Depends(get_current_user)):
    image_data = await image.image_file.read()
    # Save the image to disk
    image_path = save_image_to_disk(image_data, image.image_file.filename)
    # Insert image details into the database
    try:
        insert_image({
            "image_path": image_path,
            "description": image.description,
            "malignancy_percentage": mock_malignancy_prediction(image_data)
        }, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving image data.") from e
    return {"description": image.description, "malignancy_percentage": mock_malignancy_prediction(image_data)}
