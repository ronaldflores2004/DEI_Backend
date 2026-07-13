from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.user import User

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.shared.enums.role_enum import (
    RoleEnum
)

from app.therapy.models.consent import (
    Consent
)

from app.therapy.repositories.consent_repository import (
    ConsentRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.schemas.consent_create import (
    ConsentCreate
)


class ConsentService:
    """
    Servicio encargado de la gestión de
    consentimientos terapéuticos.
    """

    @staticmethod
    def create_consent(
        data: ConsentCreate,
        current_user: User,
        db: Session,
    ) -> Consent:

        if current_user.role != RoleEnum.PATIENT:
            raise HTTPException(
                status_code=403,
                detail="Solo pacientes"
            )

        patient = PatientRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Perfil de paciente no encontrado"
            )

        relationship = (
            PatientProfessionalRepository.get_active_relation(
                db=db,
                patient_id=patient.id,
                professional_id=data.professional_id
            )
        )

        if not relationship:
            raise HTTPException(
                status_code=400,
                detail="No existe relación terapéutica activa"
            )

        existing = ConsentRepository.get_active(
            db=db,
            patient_id=patient.id,
            professional_id=data.professional_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Consentimiento ya otorgado"
            )

        consent = Consent(
            patient_id=patient.id,
            professional_id=data.professional_id,
            granted=True
        )

        return ConsentRepository.create(
            db=db,
            consent=consent
        )

    @staticmethod
    def get_my_consents(
        current_user: User,
        db: Session,
    ) -> list[Consent]:

        if current_user.role != RoleEnum.PATIENT:
            raise HTTPException(
                status_code=403,
                detail="Solo pacientes"
            )

        patient = PatientRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Perfil de paciente no encontrado"
            )

        return ConsentRepository.get_by_patient(
            db=db,
            patient_id=patient.id
        )

    @staticmethod
    def revoke_consent(
        consent_id: int,
        current_user: User,
        db: Session,
    ) -> dict:

        if current_user.role != RoleEnum.PATIENT:
            raise HTTPException(
                status_code=403,
                detail="Solo pacientes"
            )

        patient = PatientRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Perfil de paciente no encontrado"
            )

        consent = ConsentRepository.get_by_id(
            db=db,
            consent_id=consent_id
        )

        if (
            not consent
            or consent.patient_id != patient.id
        ):
            raise HTTPException(
                status_code=404,
                detail="Consentimiento no encontrado"
            )

        consent.granted = False
        consent.revoked_at = datetime.utcnow()

        ConsentRepository.update(
            db=db,
            consent=consent
        )

        return {
            "message": "Consentimiento revocado"
        }