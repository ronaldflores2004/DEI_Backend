from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class PatientProfessional(Base):

    __tablename__ = "patient_professionals"
    
    __table_args__ = (

        Index(
            "ix_patient_professional_patient_professional",
            "patient_id",
            "professional_id"
        ),

        Index(
            "ix_patient_professional_professional",
            "professional_id"
        ),

    )
    
    id = Column(Integer, primary_key=True, index=True)

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

    sharing_mode = Column(
        String(50),
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    ended_at = Column(
        DateTime,
        nullable=True
    )
    
    patient = relationship(
        "PatientProfile",
        back_populates="relations"
    )

    professional = relationship(
        "ProfessionalProfile",
        back_populates="relations"
    )