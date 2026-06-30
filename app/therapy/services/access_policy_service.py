from sqlalchemy.orm import Session

from app.therapy.models.consent import Consent


def has_active_consent(
    patient_id: int,
    professional_id: int,
    db: Session
) -> bool:

    consent = (
        db.query(Consent)
        .filter(
            Consent.patient_id == patient_id,
            Consent.professional_id == professional_id,
            Consent.granted == True
        )
        .first()
    )

    return consent is not None