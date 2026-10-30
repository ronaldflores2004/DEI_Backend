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


class AccessAuditLog(Base):
    """
    Registro de cada acceso de un profesional a
    datos de un paciente. El paciente puede
    consultarlo.
    """

    __tablename__ = "access_audit_logs"

    __table_args__ = (

        Index(
            "ix_access_audit_patient_created",
            "patient_id",
            "created_at"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patient_profiles.id"),
        nullable=False
    )

    action = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
