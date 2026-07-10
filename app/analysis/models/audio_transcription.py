from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class AudioTranscription(Base):

    __tablename__ = "audio_transcriptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    entry_id = Column(
        Integer,
        ForeignKey("emotional_entries.id"),
        nullable=False
    )

    transcription_text = Column(
        Text,
        nullable=False
    )

    provider = Column(
        String(100),
        nullable=False
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
    
    entry = relationship(
        "EmotionalEntry",
        back_populates="transcription"
    )