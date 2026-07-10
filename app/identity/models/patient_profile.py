from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class PatientProfile(Base):

    __tablename__ = "patient_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    birth_date = Column(
        Date,
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    user = relationship(
        "User",
        back_populates="patient_profile"
    )

    entries = relationship(
        "EmotionalEntry",
        back_populates="patient"
    )

    sessions = relationship(
        "TherapySession",
        back_populates="patient"
    )

    recommendations = relationship(
        "PatientRecommendation",
        back_populates="patient"
    )

    relations = relationship(
        "PatientProfessional",
        back_populates="patient"
    )

    consents = relationship(
        "Consent",
        back_populates="patient"
    )