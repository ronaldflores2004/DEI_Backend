from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index
)

from app.core.database import Base

from app.shared.enums.risk_alert_status_enum import (
    RiskAlertStatusEnum
)


class RiskAlert(Base):
    """
    Alerta de riesgo HIGH o CRITICAL para un
    profesional, con su seguimiento.
    """

    __tablename__ = "risk_alerts"

    __table_args__ = (

        Index(
            "ix_risk_alerts_professional_status",
            "professional_id",
            "status"
        ),

        Index(
            "uq_risk_alert_analysis_professional",
            "analysis_id",
            "professional_id",
            unique=True
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patient_profiles.id"),
        nullable=False
    )

    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False
    )

    analysis_id = Column(
        Integer,
        ForeignKey("emotional_analyses.id"),
        nullable=False
    )

    risk_level = Column(
        String(50),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default=RiskAlertStatusEnum.NEW
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    seen_at = Column(
        DateTime,
        nullable=True
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )

    # Qué hizo el profesional (llamada, sesión, derivación).
    resolution_note = Column(
        String(1000),
        nullable=True
    )
