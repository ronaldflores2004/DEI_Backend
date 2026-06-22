from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.sessions.schemas.therapy_session_create import (
    TherapySessionCreate
)

from app.sessions.schemas.therapy_session_response import (
    TherapySessionResponse
)

from app.sessions.services.therapy_session_service import (
    create_session,
    get_sessions
)

from app.sessions.schemas.session_status_response import (
    SessionStatusResponse
)

from app.sessions.services.therapy_session_service import (
    complete_session,
    cancel_session
)

router = APIRouter(
    prefix="/sessions",
    tags=["Therapy Sessions"]
)


@router.post(
    "",
    response_model=TherapySessionResponse
)
def create_therapy_session(
    data: TherapySessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_session(
        current_user.id,
        data,
        db
    )


@router.get(
    "",
    response_model=list[TherapySessionResponse]
)
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_sessions(
        current_user.id,
        db
    )
    
@router.patch(
    "/{session_id}/complete",
    response_model=SessionStatusResponse
)
def complete_therapy_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return complete_session(
        session_id,
        current_user.id,
        db
    )


@router.patch(
    "/{session_id}/cancel",
    response_model=SessionStatusResponse
)
def cancel_therapy_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return cancel_session(
        session_id,
        current_user.id,
        db
    )