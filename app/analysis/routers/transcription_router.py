from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
)

from app.analysis.repositories.transcription_repository import (
    TranscriptionRepository
)

from app.analysis.schemas.transcription_create import (
    TranscriptionCreate
)

from app.analysis.schemas.transcription_response import (
    TranscriptionResponse
)

router = APIRouter(
    prefix="/analysis/transcriptions",
    tags=["Audio Transcriptions"]
)


@router.post(
    "/{entry_id}",
    response_model=TranscriptionResponse
)
def create_transcription(
    entry_id: int,
    data: TranscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Obtener perfil del paciente autenticado

    patient = (
        PatientRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    # Buscar entrada emocional

    entry = (
        EmotionalEntryRepository.get_by_id(
            db=db,
            entry_id=entry_id
        )
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    # Seguridad:
    # solo el propietario puede crear
    # transcripciones sobre su entrada

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "No tienes permiso para "
                "transcribir esta entrada"
            )
        )

    # Evitar múltiples transcripciones

    existing_transcription = (
        TranscriptionRepository.get_by_entry(
            db=db,
            entry_id=entry.id
        )
    )

    if existing_transcription:
        raise HTTPException(
            status_code=400,
            detail=(
                "La entrada ya tiene "
                "una transcripción"
            )
        )

    transcription = AudioTranscription(
        entry_id=entry.id,
        transcription_text=data.transcription_text,
        provider="MANUAL"
    )

    transcription = (
        TranscriptionRepository.create(
            db=db,
            transcription=transcription
        )
    )

    return transcription