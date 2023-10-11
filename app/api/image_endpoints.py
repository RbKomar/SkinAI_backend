import random

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.api.auth import get_current_user
from app.database.db_manager import (
    insert_image,
    save_image_to_disk,
    fetch_images_by_user,
    fetch_image_by_id,
)
from app.models.image import ImageUpload
from app.models.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def mock_malignancy_prediction() -> int:
    return random.randint(0, 100)


@router.post("/image/")
async def process_image(
    request: Request,
    image: ImageUpload,
    current_user: User = Depends(get_current_user),
):
    # Logic for image processing
    malignancy_percentage = mock_malignancy_prediction()
    return {
        "description": image.description,
        "malignancy_percentage": malignancy_percentage,
    }


@router.post("/image/upload/")
@limiter.limit("5/minute")
async def upload_image_endpoint(
    request: Request,
    description: str = Form(...),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    image_data = await image.read()  # This reads the file data

    # Save the image to disk
    image_path = save_image_to_disk(image_data, image.filename)
    # Insert image details into the database
    malignancy_percentage = mock_malignancy_prediction()
    try:
        insert_image(
            {
                "image_path": image_path,
                "description": description,
                "malignancy_percentage": malignancy_percentage,
            },
            current_user.id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving image data. {e}"
        ) from e
    return {
        "description": description,
        "malignancy_percentage": malignancy_percentage,
    }


@router.get("/image/{image_id}/")
async def get_image_by_id(image_id: int):
    image_data = fetch_image_by_id(image_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    return image_data


@router.get("/user/{user_id}/images/")
async def get_user_images(user_id: int):
    images_data = fetch_images_by_user(user_id)
    if not images_data:
        raise HTTPException(
            status_code=404, detail="No images found for the user"
        )
    return images_data
