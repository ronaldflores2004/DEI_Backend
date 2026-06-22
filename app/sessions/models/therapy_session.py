from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class TherapySession(Base):

    __tablename__ = "therapy_sessions"

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

    session_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="SCHEDULED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )