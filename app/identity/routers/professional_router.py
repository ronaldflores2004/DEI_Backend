from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.schemas.professional_profile_create import (
    ProfessionalProfileCreate
)

from app.identity.schemas.professional_profile_response import (
    ProfessionalProfileResponse
)

from app.identity.services.professional_service import (
    ProfessionalService
)



router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"]
)


@router.post(
    "/profile",
    response_model=ProfessionalProfileResponse
)
def create_professional_profile(
    profile: ProfessionalProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.create_profile(
        db=db,
        current_user=current_user,
        profile=profile
    )


@router.get("/pending")
def get_pending_professionals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.get_pending(
        db=db,
        current_user=current_user
    )


@router.patch("/{professional_id}/verify")
def verify_professional(
    professional_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.verify_professional(
        professional_id=professional_id,
        db=db,
        current_user=current_user
    )