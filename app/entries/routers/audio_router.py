from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
import os
import uuid

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...)
):

    extension = os.path.splitext(
        file.filename
    )[1]

    unique_filename = (
        str(uuid.uuid4())
        + extension
    )

    file_path = os.path.join(
        "uploads",
        "audio",
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "Audio guardado",
        "path": file_path
    }