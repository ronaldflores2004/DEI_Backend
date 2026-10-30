from datetime import datetime

from sqlalchemy.orm import Session

from app.entries.models.emotional_entry import (
    EmotionalEntry,
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis,
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
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

    @staticmethod
    def update(
        db: Session,
        analysis: EmotionalAnalysis,
    ) -> EmotionalAnalysis:

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
        since: datetime | None = None,
    ) -> list[EmotionalAnalysis]:
        """
        since limita a entradas creadas desde esa
        fecha (historial compartido con un profesional).
        """

        query = (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived.is_(False)
            )
        )

        if since:
            query = query.filter(
                EmotionalEntry.created_at >= since
            )

        return (
            query
            .order_by(
                EmotionalAnalysis.analyzed_at.desc()
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
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived.is_(False),
                EmotionalAnalysis.analyzed_at >= since
            )
            .order_by(
                EmotionalAnalysis.analyzed_at.desc()
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
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived.is_(False)
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
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived.is_(False)
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
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived.is_(False),
                EmotionalAnalysis.risk_level.in_(
                    [
                        RiskLevelEnum.MEDIUM,
                        RiskLevelEnum.HIGH,
                        RiskLevelEnum.CRITICAL
                    ]
                )
            )
            .order_by(
                EmotionalAnalysis.analyzed_at.desc()
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

    # =====================================
    # OBTENER ANÁLISIS CON ENTRADAS
    # =====================================

    @staticmethod
    def get_with_entries(
        db: Session,
        patient_ids: list[int] | None = None,
    ) -> list[tuple]:

        query = (
            db.query(
                EmotionalAnalysis,
                EmotionalEntry
            )
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
        )

        if patient_ids is not None:
            query = query.filter(
                EmotionalEntry.patient_id.in_(patient_ids)
            )

        return query.all()