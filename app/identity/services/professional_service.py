from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

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

from app.shared.enums.role_enum import RoleEnum


class ProfessionalService:
    """
    Servicio encargado de la gestión de
    perfiles profesionales.
    """

    @staticmethod
    def create_profile(
        db: Session,
        current_user: User,
        profile: ProfessionalProfileCreate,
    ) -> ProfessionalProfile:

        if current_user.role != RoleEnum.PROFESSIONAL:
            raise HTTPException(
                status_code=403,
                detail="Solo profesionales pueden crear este perfil"
            )

        existing_profile = (
            ProfessionalRepository.get_by_user_id(
                db=db,
                user_id=current_user.id
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

        return ProfessionalRepository.create(
            db=db,
            profile=professional
        )

    @staticmethod
    def get_pending(
        db: Session,
        current_user: User,
    ) -> list[ProfessionalProfile]:

        if current_user.role != RoleEnum.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Solo administradores"
            )

        return ProfessionalRepository.get_pending(
            db=db
        )

    @staticmethod
    def verify_professional(
        professional_id: int,
        db: Session,
        current_user: User,
    ) -> dict:

        if current_user.role != RoleEnum.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Solo administradores"
            )

        professional = (
            ProfessionalRepository.get_by_id(
                db=db,
                professional_id=professional_id
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

        ProfessionalRepository.update(
            db=db,
            profile=professional
        )

        return {
            "message": "Profesional verificado"
        }