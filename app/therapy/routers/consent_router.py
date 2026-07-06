from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.shared.enums.role_enum import RoleEnum

from app.therapy.models.consent import Consent

from app.therapy.repositories.consent_repository import (
    ConsentRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.schemas.consent_create import (
    ConsentCreate
)

from app.therapy.schemas.consent_response import (
    ConsentResponse
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

    if current_user.role != RoleEnum.PATIENT:
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = PatientRepository.get_by_user_id(
        db,
        current_user.id
    )

    relationship = (
        PatientProfessionalRepository.get_active_relation(
            db=db,
            patient_id=patient.id,
            professional_id=consent.professional_id
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
        professional_id=consent.professional_id
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Consentimiento ya otorgado"
        )

    new_consent = Consent(
        patient_id=patient.id,
        professional_id=consent.professional_id,
        granted=True
    )

    new_consent = ConsentRepository.create(
        db,
        new_consent
    )

    return new_consent


@router.get(
    "",
    response_model=list[ConsentResponse]
)
def get_my_consents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != RoleEnum.PATIENT:
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = PatientRepository.get_by_user_id(
        db,
        current_user.id
    )

    return ConsentRepository.get_by_patient(
        db,
        patient.id
    )


@router.patch("/{consent_id}/revoke")
def revoke_consent(
    consent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != RoleEnum.PATIENT:
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = PatientRepository.get_by_user_id(
        db,
        current_user.id
    )

    consent = ConsentRepository.get_by_id(
        db,
        consent_id
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
        db,
        consent
    )

    return {
        "message": "Consentimiento revocado"
    }