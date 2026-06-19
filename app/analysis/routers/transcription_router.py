from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

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

    transcription = AudioTranscription(
        entry_id=entry.id,
        transcription_text=data.transcription_text,
        provider="MANUAL"
    )

    db.add(transcription)

    db.commit()

    db.refresh(transcription)

    return transcription