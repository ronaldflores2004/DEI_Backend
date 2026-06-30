from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.entries.schemas.emotional_entry_create import (
    EmotionalEntryCreate
)

from app.entries.schemas.emotional_entry_response import (
    EmotionalEntryResponse
)

import os
import uuid
import shutil

router = APIRouter(
    prefix="/entries",
    tags=["Emotional Entries"]
)


# =====================================
# Crear entrada de texto
# =====================================

@router.post(
    "",
    response_model=EmotionalEntryResponse
)
def create_entry(
    entry: EmotionalEntryCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    emotional_entry = EmotionalEntry(
        patient_id=patient.id,
        entry_type=entry.entry_type,
        text_content=entry.text_content
    )

    db.add(emotional_entry)

    db.commit()

    db.refresh(emotional_entry)

    return emotional_entry


# =====================================
# Crear entrada de audio
# =====================================

@router.post("/audio")
async def create_audio_entry(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
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

    emotional_entry = EmotionalEntry(
        patient_id=patient.id,
        entry_type="AUDIO",
        audio_path=file_path
    )

    db.add(emotional_entry)

    db.commit()

    db.refresh(emotional_entry)

    return emotional_entry


# =====================================
# Listar entradas
# =====================================

@router.get(
    "",
    response_model=list[EmotionalEntryResponse]
)
def get_entries(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    entries = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.patient_id
            == patient.id
        )
        .order_by(
            EmotionalEntry.created_at.desc()
        )
        .all()
    )

    return entries


# =====================================
# Obtener entrada
# =====================================

@router.get(
    "/{entry_id}",
    response_model=EmotionalEntryResponse
)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id,
            EmotionalEntry.patient_id == patient.id
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    return entry


# =====================================
# Archivar entrada
# =====================================

@router.patch("/{entry_id}/archive")
def archive_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id,
            EmotionalEntry.patient_id == patient.id
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    entry.is_archived = True

    db.commit()

    return {
        "message": "Entrada archivada"
    }