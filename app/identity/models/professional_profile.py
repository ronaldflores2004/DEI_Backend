from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class ProfessionalProfile(Base):

    __tablename__ = "professional_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    license_number = Column(
        String(100),
        nullable=False
    )

    specialties = Column(
        String(500),
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    verified_by_admin = Column(
        Integer,
        nullable=True
    )

    verified_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )