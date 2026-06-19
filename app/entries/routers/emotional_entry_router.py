from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.patient_profile import PatientProfile

from app.entries.models.emotional_entry import EmotionalEntry

from app.entries.schemas.emotional_entry_create import (
    EmotionalEntryCreate
)

from app.entries.schemas.emotional_entry_response import (
    EmotionalEntryResponse
)

from fastapi import UploadFile
from fastapi import File

import os
import uuid
import shutil

router = APIRouter(
    prefix="/entries",
    tags=["Emotional Entries"]
)

@router.post(
    "",
    response_model=EmotionalEntryResponse
)
def create_entry(
    entry: EmotionalEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Perfil de paciente no encontrado"
        )

    emotional_entry = EmotionalEntry(
        patient_id=patient.id,
        entry_type=entry.entry_type,
        text_content=entry.text_content
    )

    db.add(emotional_entry)

    db.commit()

    db.refresh(emotional_entry)

    return emotional_entry


@router.post("/audio")
async def create_audio_entry(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Perfil de paciente no encontrado"
        )

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

@router.get(
    "",
    response_model=list[EmotionalEntryResponse]
)
def get_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    entries = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.patient_id == patient.id
        )
        .order_by(
            EmotionalEntry.created_at.desc()
        )
        .all()
    )

    return entries

@router.get(
    "/{entry_id}",
    response_model=EmotionalEntryResponse
)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

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

@router.patch("/{entry_id}/archive")
def archive_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

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