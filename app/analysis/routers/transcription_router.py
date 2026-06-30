from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
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
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    # Buscar entrada emocional
    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id
        )
        .first()
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
    # para una misma entrada
    existing_transcription = (
        db.query(AudioTranscription)
        .filter(
            AudioTranscription.entry_id == entry.id
        )
        .first()
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

    db.add(transcription)

    db.commit()

    db.refresh(transcription)

    return transcription