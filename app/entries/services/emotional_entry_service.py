import os
import shutil
import uuid

from fastapi import (
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.entries.schemas.emotional_entry_create import (
    EmotionalEntryCreate
)

from app.shared.enums.entry_type_enum import (
    EntryTypeEnum
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg"
}

ALLOWED_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/x-m4a",
    "audio/ogg"
}

class EmotionalEntryService:
    """
    Servicio encargado de la gestión de
    entradas emocionales.
    """

    @staticmethod
    def create_entry(
        data: EmotionalEntryCreate,
        patient: PatientProfile,
        db: Session,
    ) -> EmotionalEntry:
        
        if data.entry_type != EntryTypeEnum.TEXT:
            raise HTTPException(
                status_code=400,
                detail="Este endpoint solo permite entradas de texto."
            )

        if not data.text_content.strip():
            raise HTTPException(
                status_code=400,
                detail="El contenido no puede estar vacío."
            )

        entry = EmotionalEntry(
            patient_id=patient.id,
            entry_type=data.entry_type,
            text_content=data.text_content
        )

        return EmotionalEntryRepository.create(
            db=db,
            entry=entry
        )

    @staticmethod
    async def create_audio_entry(
        file: UploadFile,
        patient: PatientProfile,
        db: Session,
    ) -> EmotionalEntry:

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Nombre de archivo inválido."
            )

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

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no permitido."
            )

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="El archivo excede el límite de 10 MB."
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

        entry = EmotionalEntry(
            patient_id=patient.id,
            entry_type=EntryTypeEnum.AUDIO,
            audio_path=file_path
        )

        return EmotionalEntryRepository.create(
            db=db,
            entry=entry
        )
        
    @staticmethod
    def get_entries(
        patient: PatientProfile,
        db: Session,
    ) -> list[EmotionalEntry]:

        return (
            EmotionalEntryRepository.get_by_patient(
                db=db,
                patient_id=patient.id
            )
        )

    @staticmethod
    def get_entry(
        entry_id: int,
        patient: PatientProfile,
        db: Session,
    ) -> EmotionalEntry:

        entry = (
            EmotionalEntryRepository.get_by_id(
                db=db,
                entry_id=entry_id
            )
        )

        if (
            not entry
            or entry.patient_id != patient.id
        ):
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        return entry

    @staticmethod
    def archive_entry(
        entry_id: int,
        patient: PatientProfile,
        db: Session,
    ) -> dict:

        entry = (
            EmotionalEntryRepository.get_by_id(
                db=db,
                entry_id=entry_id
            )
        )

        if (
            not entry
            or entry.patient_id != patient.id
        ):
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        EmotionalEntryRepository.archive(
            db=db,
            entry=entry
        )

        return {
            "message": "Entrada archivada"
        }