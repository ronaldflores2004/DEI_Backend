from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON
)

from app.core.database import Base


class EmotionalAnalysis(Base):

    __tablename__ = "emotional_analyses"

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

    primary_emotion = Column(
        String(100),
        nullable=True
    )

    emotion_intensity = Column(
        String(50),
        nullable=True
    )

    risk_level = Column(
        String(50),
        nullable=True
    )

    analysis_json = Column(
        JSON,
        nullable=False
    )

    analyzed_at = Column(
        DateTime,
        default=datetime.utcnow
    )