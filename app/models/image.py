from fastapi import UploadFile
from pydantic import BaseModel


class ImageUpload(BaseModel):
    description: str
    image_file: UploadFile
