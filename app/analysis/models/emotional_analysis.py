from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    JSON
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class EmotionalAnalysis(Base):

    __tablename__ = "emotional_analyses"
    
    __table_args__ = (

        Index(
            "ix_emotional_analysis_entry",
            "entry_id"
        ),

        Index(
            "ix_emotional_analysis_risk",
            "risk_level"
        ),

    )

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
    
    entry = relationship(
        "EmotionalEntry",
        back_populates="analysis"
    )

    recommendations = relationship(
        "PatientRecommendation",
        back_populates="analysis"
    )