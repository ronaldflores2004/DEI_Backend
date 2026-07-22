from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.sessions.schemas.clinical_note_create import (
    ClinicalNoteCreate
)

from app.sessions.schemas.clinical_note_response import (
    ClinicalNoteResponse
)

from app.sessions.services.clinical_note_service import (
    ClinicalNoteService
)

router = APIRouter(
    prefix="/sessions",
    tags=["Clinical Notes"]
)


@router.post(
    "/{session_id}/notes",
    response_model=ClinicalNoteResponse
)
def create_clinical_note(
    session_id: int,
    data: ClinicalNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ClinicalNoteService.create_note(
        session_id,
        current_user.id,
        data,
        db
    )


@router.get(
    "/{session_id}/notes",
    response_model=list[ClinicalNoteResponse]
)
def list_clinical_notes(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ClinicalNoteService.get_notes(
        session_id,
        current_user.id,
        db
    )