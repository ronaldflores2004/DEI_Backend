from sqlalchemy.orm import Session

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation,
)


class PatientRecommendationRepository:
    """
    Repositorio para el acceso a datos de
    PatientRecommendation.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        recommendation_id: int,
    ) -> PatientRecommendation | None:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.id
                == recommendation_id
            )
            .first()
        )

    @staticmethod
    def get_by_analysis(
        db: Session,
        analysis_id: int,
    ) -> PatientRecommendation | None:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.analysis_id
                == analysis_id
            )
            .first()
        )

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[PatientRecommendation]:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.patient_id
                == patient_id
            )
            .order_by(
                PatientRecommendation.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_latest_by_patient(
        db: Session,
        patient_id: int,
    ) -> PatientRecommendation | None:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.patient_id
                == patient_id
            )
            .order_by(
                PatientRecommendation.created_at.desc()
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        recommendation: PatientRecommendation,
    ) -> PatientRecommendation:

        db.add(recommendation)

        db.commit()

        db.refresh(recommendation)

        return recommendation

    @staticmethod
    def update(
        db: Session,
        recommendation: PatientRecommendation,
    ) -> PatientRecommendation:

        db.commit()

        db.refresh(recommendation)

        return recommendation

    @staticmethod
    def count_by_patient(
        db: Session,
        patient_id: int,
    ) -> int:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.patient_id
                == patient_id
            )
            .count()
        )

    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(PatientRecommendation)
            .count()
        )