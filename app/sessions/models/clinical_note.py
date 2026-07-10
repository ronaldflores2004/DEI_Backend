from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class ClinicalNote(Base):

    __tablename__ = "clinical_notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("therapy_sessions.id"),
        nullable=False
    )

    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False
    )

    note = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    session = relationship(
        "TherapySession",
        back_populates="clinical_notes"
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="clinical_notes"
    )