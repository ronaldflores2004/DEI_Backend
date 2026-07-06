from sqlalchemy.orm import Session

from app.therapy.models.consent import (
    Consent,
)


class ConsentRepository:
    """
    Repositorio para el acceso a datos de
    Consent.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        consent_id: int,
    ) -> Consent | None:

        return (
            db.query(Consent)
            .filter(
                Consent.id == consent_id
            )
            .first()
        )

    @staticmethod
    def get_active(
        db: Session,
        patient_id: int,
        professional_id: int,
    ) -> Consent | None:

        return (
            db.query(Consent)
            .filter(
                Consent.patient_id == patient_id,
                Consent.professional_id == professional_id,
                Consent.granted == True,
            )
            .first()
        )

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[Consent]:

        return (
            db.query(Consent)
            .filter(
                Consent.patient_id == patient_id
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        consent: Consent,
    ) -> Consent:

        db.add(consent)

        db.commit()

        db.refresh(consent)

        return consent