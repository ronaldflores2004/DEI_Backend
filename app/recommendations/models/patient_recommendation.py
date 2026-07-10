from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class PatientRecommendation(Base):

    __tablename__ = "patient_recommendations"
    
    __table_args__ = (

        Index(
            "ix_patient_recommendation_patient",
            "patient_id"
        ),

        Index(
            "ix_patient_recommendation_analysis",
            "analysis_id",
            unique=True
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
    
    analysis_id = Column(
    Integer,
    ForeignKey("emotional_analyses.id"),
    nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    source = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    patient = relationship(
        "PatientProfile",
        back_populates="recommendations"
    )

    analysis = relationship(
        "EmotionalAnalysis",
        back_populates="recommendations"
    )