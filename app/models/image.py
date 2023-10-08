from fastapi import UploadFile
from pydantic import BaseModel


class ImageUpload(BaseModel):
    image_file: UploadFile
    description: str
