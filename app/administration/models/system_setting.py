from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class SystemSetting(Base):
    """
    Ajuste del sistema editable por el administrador
    sin reiniciar el backend (por ejemplo, el orden de
    proveedores de IA).
    """

    __tablename__ = "system_settings"

    key = Column(
        String(100),
        primary_key=True
    )

    value = Column(
        String(1000),
        nullable=False
    )

    updated_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
