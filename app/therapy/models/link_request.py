from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.shared.enums.link_request_status_enum import (
    LinkRequestStatusEnum
)


class LinkRequest(Base):

    __tablename__ = "link_requests"
    
    __table_args__ = (

        Index(
            "ix_link_request_patient_professional_status",
            "patient_id",
            "professional_id",
            "status"
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

    professional_id = Column(
        Integer,
        ForeignKey("professional_profiles.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default=LinkRequestStatusEnum.PENDING
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    patient = relationship(
        "PatientProfile"
    )

    professional = relationship(
        "ProfessionalProfile"
    )