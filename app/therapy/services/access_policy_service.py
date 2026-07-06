from sqlalchemy.orm import Session

from app.therapy.repositories.consent_repository import (
    ConsentRepository,
)


def has_active_consent(
    patient_id: int,
    professional_id: int,
    db: Session
) -> bool:

    consent = ConsentRepository.get_active(
        db=db,
        patient_id=patient_id,
        professional_id=professional_id,
    )

    return consent is not None