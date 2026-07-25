from fastapi import APIRouter
from fastapi import Depends
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

from app.entries.schemas.emotional_entry_create import (
    EmotionalEntryCreate
)

from app.entries.schemas.emotional_entry_response import (
    EmotionalEntryResponse
)

from app.entries.services.emotional_entry_service import (
    EmotionalEntryService
)



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

    return EmotionalEntryService.create_entry(
        data=entry,
        patient=patient,
        db=db
    )

# =====================================
# Crear entrada de audio
# =====================================

@router.post("/audio", response_model=EmotionalEntryResponse)
async def create_audio_entry(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return await EmotionalEntryService.create_audio_entry(
        file=file,
        patient=patient,
        db=db
    )

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

        return EmotionalEntryService.get_entries(
        patient=patient,
        db=db
    )


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

        return EmotionalEntryService.get_entry(
        entry_id=entry_id,
        patient=patient,
        db=db
    )


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

    return EmotionalEntryService.archive_entry(
        entry_id=entry_id,
        patient=patient,
        db=db
    )