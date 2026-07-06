from sqlalchemy.orm import Session

from app.therapy.models.patient_professional import (
    PatientProfessional,
)


class PatientProfessionalRepository:
    """
    Repositorio para el acceso a datos de
    PatientProfessional.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        relation_id: int,
    ) -> PatientProfessional | None:

        return (
            db.query(PatientProfessional)
            .filter(
                PatientProfessional.id == relation_id
            )
            .first()
        )

    @staticmethod
    def get_active_relation(
        db: Session,
        patient_id: int,
        professional_id: int,
    ) -> PatientProfessional | None:

        return (
            db.query(PatientProfessional)
            .filter(
                PatientProfessional.patient_id == patient_id,
                PatientProfessional.professional_id == professional_id,
                PatientProfessional.active == True,
            )
            .first()
        )

    @staticmethod
    def get_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[PatientProfessional]:

        return (
            db.query(PatientProfessional)
            .filter(
                PatientProfessional.professional_id == professional_id
            )
            .all()
        )

    @staticmethod
    def get_active_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[PatientProfessional]:

        return (
            db.query(PatientProfessional)
            .filter(
                PatientProfessional.professional_id == professional_id,
                PatientProfessional.active == True,
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        relation: PatientProfessional,
    ) -> PatientProfessional:

        db.add(relation)

        db.commit()

        db.refresh(relation)

        return relation