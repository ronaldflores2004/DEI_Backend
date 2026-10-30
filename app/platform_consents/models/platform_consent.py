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


class PlatformConsent(Base):
    """
    Consentimiento del paciente hacia la plataforma
    (no hacia un profesional). Cada aceptación guarda
    la versión del texto aceptado.
    """

    __tablename__ = "platform_consents"

    __table_args__ = (

        Index(
            "ix_platform_consents_patient_type",
            "patient_id",
            "consent_type"
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

    consent_type = Column(
        String(50),
        nullable=False
    )

    version = Column(
        String(20),
        nullable=False
    )

    granted_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    revoked_at = Column(
        DateTime,
        nullable=True
    )
