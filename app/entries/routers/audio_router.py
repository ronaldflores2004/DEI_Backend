from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from app.core.dependencies import (
    get_current_user
)

from app.identity.models.user import User

import os
import shutil
import uuid

router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg"
}


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_user
    )
):

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Formato no permitido. "
                "Use mp3, wav, m4a u ogg."
            )
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=(
                "El archivo excede "
                "el límite de 10 MB."
            )
        )

    await file.seek(0)

    os.makedirs(
        "uploads/audio",
        exist_ok=True
    )

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        "uploads",
        "audio",
        unique_filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "Audio guardado",
        "path": file_path
    }