from datetime import datetime

from sqlalchemy.orm import Session

from app.entries.models.emotional_entry import (
    EmotionalEntry,
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis,
)


class EmotionalAnalysisRepository:
    """
    Repositorio para el acceso a datos de
    EmotionalAnalysis.
    """

    # =====================================
    # CRUD
    # =====================================

    @staticmethod
    def get_by_id(
        db: Session,
        analysis_id: int,
    ) -> EmotionalAnalysis | None:

        return (
            db.query(EmotionalAnalysis)
            .filter(
                EmotionalAnalysis.id == analysis_id
            )
            .first()
        )

    @staticmethod
    def get_by_entry(
        db: Session,
        entry_id: int,
    ) -> EmotionalAnalysis | None:

        return (
            db.query(EmotionalAnalysis)
            .filter(
                EmotionalAnalysis.entry_id == entry_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        analysis: EmotionalAnalysis,
    ) -> EmotionalAnalysis:

        db.add(analysis)

        db.commit()

        db.refresh(analysis)

        return analysis

    # =====================================
    # CONSULTAS DE DOMINIO
    # =====================================

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalAnalysis]:

        return (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id
            )
            .all()
        )

    @staticmethod
    def get_weekly_by_patient(
        db: Session,
        patient_id: int,
        since: datetime,
    ) -> list[EmotionalAnalysis]:

        return (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id,
                EmotionalAnalysis.analyzed_at
                >= since
            )
            .all()
        )

    @staticmethod
    def get_latest_by_patient(
        db: Session,
        patient_id: int,
    ) -> EmotionalAnalysis | None:

        return (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id
            )
            .order_by(
                EmotionalAnalysis.analyzed_at.desc()
            )
            .first()
        )

    @staticmethod
    def count_by_patient(
        db: Session,
        patient_id: int,
    ) -> int:

        return (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id
            )
            .count()
        )

    @staticmethod
    def get_high_risk_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalAnalysis]:

        return (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id,
                EmotionalAnalysis.risk_level.in_(
                    [
                        "Medio",
                        "Alto",
                        "Crítico"
                    ]
                )
            )
            .all()
        )
    
    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(EmotionalAnalysis)
            .count()
        )