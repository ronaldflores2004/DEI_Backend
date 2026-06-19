from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class EmotionalEntry(Base):

    __tablename__ = "emotional_entries"

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