from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.shared.enums.session_status_enum import (
    SessionStatusEnum
)

class TherapySession(Base):

    __tablename__ = "therapy_sessions"

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

    session_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default=SessionStatusEnum.SCHEDULED
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    patient = relationship(
        "PatientProfile",
        back_populates="sessions"
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="sessions"
    )

    clinical_notes = relationship(
        "ClinicalNote",
        back_populates="session"
    )