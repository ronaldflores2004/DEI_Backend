from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class Consent(Base):

    __tablename__ = "consents"

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

    granted = Column(
        Boolean,
        default=True
    )

    granted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    revoked_at = Column(
        DateTime,
        nullable=True
    )