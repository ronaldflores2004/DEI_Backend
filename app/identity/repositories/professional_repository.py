from sqlalchemy.orm import Session

from app.identity.models.professional_profile import (
    ProfessionalProfile,
)


class ProfessionalRepository:
    """
    Repositorio para el acceso a datos de
    ProfessionalProfile.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        professional_id: int,
    ) -> ProfessionalProfile | None:

        return (
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.id == professional_id
            )
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ) -> ProfessionalProfile | None:

        return (
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_pending(
        db: Session,
    ) -> list[ProfessionalProfile]:

        return (
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.is_verified.is_(False)
            )
            .all()
        )

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[ProfessionalProfile]:

        return (
            db.query(ProfessionalProfile)
            .order_by(
                ProfessionalProfile.last_name,
                ProfessionalProfile.first_name
            )
            .all()
        )

    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(ProfessionalProfile)
            .count()
        )

    @staticmethod
    def count_verified(
        db: Session,
    ) -> int:

        return (
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.is_verified.is_(True)
            )
            .count()
        )

    @staticmethod
    def count_pending(
        db: Session,
    ) -> int:

        return (
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.is_verified.is_(False)
            )
            .count()
        )

    @staticmethod
    def create(
        db: Session,
        profile: ProfessionalProfile,
    ) -> ProfessionalProfile:

        db.add(profile)

        db.commit()

        db.refresh(profile)

        return profile

    @staticmethod
    def update(
        db: Session,
        profile: ProfessionalProfile,
    ) -> ProfessionalProfile:

        db.commit()

        db.refresh(profile)

        return profile