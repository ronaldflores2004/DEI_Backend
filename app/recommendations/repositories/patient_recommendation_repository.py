from sqlalchemy.orm import Session

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation,
)

from app.shared.enums.recommendation_status_enum import (
    RecommendationStatusEnum
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
        status: str = RecommendationStatusEnum.APPROVED,
    ) -> list[PatientRecommendation]:
        """
        Por defecto solo las aprobadas: el paciente
        nunca ve una recomendación sin revisar.
        """

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.patient_id
                == patient_id,
                PatientRecommendation.status == status
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
                == patient_id,
                PatientRecommendation.status
                == RecommendationStatusEnum.APPROVED
            )
            .order_by(
                PatientRecommendation.created_at.desc()
            )
            .first()
        )

    @staticmethod
    def get_pending_by_patients(
        db: Session,
        patient_ids: list[int],
    ) -> list[PatientRecommendation]:

        return (
            db.query(PatientRecommendation)
            .filter(
                PatientRecommendation.patient_id.in_(patient_ids),
                PatientRecommendation.status
                == RecommendationStatusEnum.PENDING_REVIEW
            )
            .order_by(
                PatientRecommendation.created_at
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        recommendation: PatientRecommendation,
    ) -> PatientRecommendation:

        db.commit()
        db.refresh(recommendation)

        return recommendation

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