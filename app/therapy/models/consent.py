from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

import sqlalchemy as sa

from app.core.database import Base


class Consent(Base):

    __tablename__ = "consents"
    
    __table_args__ = (

        Index(
            "ix_consent_patient_professional",
            "patient_id",
            "professional_id"
        ),
        Index(
            "uq_active_consent_patient_professional",
            "patient_id",
            "professional_id",
            unique=True,
            postgresql_where=sa.text("granted = true")
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

    granted = Column(
        Boolean,
        default=True
    )

    granted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    revoked_at = Column(
        DateTime,
        nullable=True
    )
    
    patient = relationship(
        "PatientProfile",
        back_populates="consents"
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="consents"
    )