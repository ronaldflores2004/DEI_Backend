from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.identity.schemas.professional_profile_create import (
    ProfessionalProfileCreate
)

from app.identity.schemas.professional_profile_response import (
    ProfessionalProfileResponse
)

from app.shared.enums.role_enum import RoleEnum

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

    if current_user.role != RoleEnum.PROFESSIONAL:
        raise HTTPException(
            status_code=403,
            detail="Solo profesionales pueden crear este perfil"
        )

    existing_profile = (
        ProfessionalRepository.get_by_user_id(
            db,
            current_user.id
        )
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Perfil ya existente"
        )

    professional = ProfessionalProfile(
        user_id=current_user.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        license_number=profile.license_number,
        specialties=profile.specialties,
        is_verified=False
    )

    professional = ProfessionalRepository.create(
        db,
        professional
    )

    return professional


@router.get("/pending")
def get_pending_professionals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Solo administradores"
        )

    return ProfessionalRepository.get_pending(
        db
    )


@router.patch("/{professional_id}/verify")
def verify_professional(
    professional_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Solo administradores"
        )

    professional = (
        ProfessionalRepository.get_by_id(
            db,
            professional_id
        )
    )

    if not professional:
        raise HTTPException(
            status_code=404,
            detail="Profesional no encontrado"
        )

    professional.is_verified = True
    professional.verified_by_admin = current_user.id
    professional.verified_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Profesional verificado"
    }