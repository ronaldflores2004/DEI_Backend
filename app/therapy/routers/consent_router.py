from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.therapy.schemas.consent_create import (
    ConsentCreate
)

from app.therapy.schemas.consent_response import (
    ConsentResponse
)

from app.therapy.services.consent_service import (
    ConsentService
)


router = APIRouter(
    prefix="/therapy/consents",
    tags=["Consents"]
)


@router.post(
    "",
    response_model=ConsentResponse
)
def create_consent(
    consent: ConsentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ConsentService.create_consent(
        data=consent,
        current_user=current_user,
        db=db
    )

@router.get(
    "",
    response_model=list[ConsentResponse]
)
def get_my_consents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ConsentService.get_my_consents(
        current_user=current_user,
        db=db
    )


@router.patch("/{consent_id}/revoke")
def revoke_consent(
    consent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ConsentService.revoke_consent(
        consent_id=consent_id,
        current_user=current_user,
        db=db
    )