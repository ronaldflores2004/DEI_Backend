from sqlalchemy.orm import Session

from app.identity.models.professional_profile import (
    ProfessionalProfile,
)


class ProfessionalRepository:
    """
    Repositorio para el acceso a datos de ProfessionalProfile.
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
                ProfessionalProfile.is_verified == False
            )
            .all()
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