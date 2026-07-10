from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class EmotionalEntry(Base):

    __tablename__ = "emotional_entries"
    
    __table_args__ = (

        Index(
            "ix_entries_patient_created",
            "patient_id",
            "created_at"
        ),

        Index(
            "ix_entries_patient_type",
            "patient_id",
            "entry_type"
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

    entry_type = Column(
        String(20),
        nullable=False
    )

    text_content = Column(
        Text,
        nullable=True
    )

    audio_path = Column(
        String(500),
        nullable=True
    )

    is_archived = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    patient = relationship(
        "PatientProfile",
        back_populates="entries"
    )

    analysis = relationship(
        "EmotionalAnalysis",
        back_populates="entry",
        uselist=False
    )

    transcription = relationship(
        "AudioTranscription",
        back_populates="entry",
        uselist=False
    )