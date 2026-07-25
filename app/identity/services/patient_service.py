from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.user import User

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.identity.schemas.patient_profile_create import (
    PatientProfileCreate
)

from app.shared.enums.role_enum import (
    RoleEnum
)

class PatientService:
    """
    Servicio encargado de la gestión del
    perfil del paciente.
    """

    @staticmethod
    def create_profile(
        db: Session,
        current_user: User,
        profile: PatientProfileCreate,
    ) -> PatientProfile:
        
        if current_user.role != RoleEnum.PATIENT:
            raise HTTPException(
                status_code=403,
                detail="Solo pacientes"
            )

        existing_profile = (
            PatientRepository.get_by_user_id(
                db=db,
                user_id=current_user.id
            )
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

        return PatientRepository.create(
            db=db,
            profile=patient_profile
        )

    @staticmethod
    def get_my_profile(
        db: Session,
        current_user: User,
    ) -> PatientProfile:
        if current_user.role != RoleEnum.PATIENT:
            raise HTTPException(
                status_code=403,
                detail="Solo pacientes"
            )
            
        profile = (
            PatientRepository.get_by_user_id(
                db=db,
                user_id=current_user.id
            )
        )

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Perfil no encontrado"
            )

        return profile