from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.schemas.patient_profile_create import (
    PatientProfileCreate
)

from app.identity.schemas.patient_profile_response import (
    PatientProfileResponse
)

from app.identity.services.patient_service import (
    PatientService
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "/profile",
    response_model=PatientProfileResponse
)
def create_profile(
    profile: PatientProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return PatientService.create_profile(
        db=db,
        current_user=current_user,
        profile=profile
    )


@router.get(
    "/profile/me",
    response_model=PatientProfileResponse
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return PatientService.get_my_profile(
        db=db,
        current_user=current_user
    )