from sqlalchemy.orm import Session

from app.platform_consents.models.platform_consent import (
    PlatformConsent
)


class PlatformConsentRepository:
    """
    Repositorio para el acceso a datos de
    PlatformConsent.
    """

    @staticmethod
    def get_active(
        db: Session,
        patient_id: int,
        consent_type: str,
    ) -> PlatformConsent | None:

        return (
            db.query(PlatformConsent)
            .filter(
                PlatformConsent.patient_id == patient_id,
                PlatformConsent.consent_type == consent_type,
                PlatformConsent.revoked_at.is_(None),
            )
            .order_by(
                PlatformConsent.granted_at.desc()
            )
            .first()
        )

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[PlatformConsent]:

        return (
            db.query(PlatformConsent)
            .filter(
                PlatformConsent.patient_id == patient_id
            )
            .order_by(
                PlatformConsent.granted_at.desc()
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        consent: PlatformConsent,
    ) -> PlatformConsent:

        db.add(consent)
        db.commit()
        db.refresh(consent)

        return consent

    @staticmethod
    def update(
        db: Session,
        consent: PlatformConsent,
    ) -> PlatformConsent:

        db.commit()
        db.refresh(consent)

        return consent
