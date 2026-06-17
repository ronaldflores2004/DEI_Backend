from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.patient_profile import PatientProfile
from app.identity.models.professional_profile import ProfessionalProfile

from app.therapy.models.consent import Consent
from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.therapy.schemas.consent_create import ConsentCreate
from app.therapy.schemas.consent_response import ConsentResponse

from datetime import datetime

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

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    relationship = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.patient_id == patient.id,
            PatientProfessional.professional_id == consent.professional_id,
            PatientProfessional.active == True
        )
        .first()
    )

    if not relationship:
        raise HTTPException(
            status_code=400,
            detail="No existe relación terapéutica activa"
        )

    existing = (
        db.query(Consent)
        .filter(
            Consent.patient_id == patient.id,
            Consent.professional_id == consent.professional_id,
            Consent.granted == True
        )
        .first()
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

    db.add(new_consent)

    db.commit()

    db.refresh(new_consent)

    return new_consent

@router.get("")
def get_my_consents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    consents = (
        db.query(Consent)
        .filter(
            Consent.patient_id == patient.id
        )
        .all()
    )

    return consents

@router.patch("/{consent_id}/revoke")
def revoke_consent(
    consent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    consent = (
        db.query(Consent)
        .filter(
            Consent.id == consent_id,
            Consent.patient_id == patient.id
        )
        .first()
    )

    if not consent:
        raise HTTPException(
            status_code=404,
            detail="Consentimiento no encontrado"
        )

    consent.granted = False
    consent.revoked_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Consentimiento revocado"
    }