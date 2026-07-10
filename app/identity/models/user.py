from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    patient_profile = relationship(
        "PatientProfile",
        back_populates="user",
        uselist=False
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="user",
        uselist=False
    )

    notifications = relationship(
        "Notification",
        back_populates="user"
    )