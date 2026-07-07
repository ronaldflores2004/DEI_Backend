from sqlalchemy.orm import Session

from app.identity.models.patient_profile import PatientProfile


class PatientRepository:
    """
    Repositorio para el acceso a datos de PatientProfile.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        patient_id: int,
    ) -> PatientProfile | None:

        return (
            db.query(PatientProfile)
            .filter(
                PatientProfile.id == patient_id
            )
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ) -> PatientProfile | None:

        return (
            db.query(PatientProfile)
            .filter(
                PatientProfile.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def exists(
        db: Session,
        user_id: int,
    ) -> bool:

        return (
            db.query(PatientProfile)
            .filter(
                PatientProfile.user_id == user_id
            )
            .first()
            is not None
        )

    @staticmethod
    def create(
        db: Session,
        profile: PatientProfile,
    ) -> PatientProfile:

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile
    
    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(PatientProfile)
            .count()
        )