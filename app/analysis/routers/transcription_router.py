from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.analysis.schemas.transcription_create import (
    TranscriptionCreate
)

from app.analysis.schemas.transcription_update import (
    TranscriptionUpdate
)

from app.analysis.schemas.transcription_response import (
    TranscriptionResponse
)

from app.analysis.services.transcription_service import (
    TranscriptionService
)

router = APIRouter(
    prefix="/analysis/transcriptions",
    tags=["Audio Transcriptions"]
)


# =====================================
# Crear transcripción
# =====================================

@router.post(
    "/{entry_id}",
    response_model=TranscriptionResponse
)
def create(
    entry_id: int,
    data: TranscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TranscriptionService.create_transcription(
        entry_id=entry_id,
        data=data,
        db=db,
        current_user=current_user
    )


# =====================================
# Actualizar transcripción
# =====================================

@router.patch(
    "/{transcription_id}",
    response_model=TranscriptionResponse
)
def update(
    transcription_id: int,
    data: TranscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TranscriptionService.update_transcription(
        transcription_id=transcription_id,
        data=data,
        db=db,
        current_user=current_user
    )
    
# =====================================
# Generar transcripción automática
# =====================================

@router.post(
    "/{entry_id}/auto",
    response_model=TranscriptionResponse
)
def generate_auto_transcription(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TranscriptionService.generate_transcription(
        entry_id=entry_id,
        db=db,
        current_user=current_user
    )