from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.patient_profile import PatientProfile

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.identity.schemas.patient_profile_create import (
    PatientProfileCreate
)

from app.identity.schemas.patient_profile_response import (
    PatientProfileResponse
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

    existing_profile = PatientRepository.get_by_user_id(
        db,
        current_user.id
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="El perfil ya existe"
        )

    patient_profile = PatientProfile(
        user_id=current_user.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        birth_date=profile.birth_date,
        gender=profile.gender
    )

    patient_profile = PatientRepository.create(
        db,
        patient_profile
    )

    return patient_profile


@router.get(
    "/profile/me",
    response_model=PatientProfileResponse
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    profile = PatientRepository.get_by_user_id(
        db,
        current_user.id
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil no encontrado"
        )

    return profile