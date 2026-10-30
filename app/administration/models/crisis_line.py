from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Index
)

from app.core.database import Base


class CrisisLine(Base):
    """
    Línea de crisis que ve el paciente ante riesgo
    alto. La gestiona el administrador.
    """

    __tablename__ = "crisis_lines"

    __table_args__ = (

        Index(
            "ix_crisis_lines_country_active",
            "country_code",
            "is_active"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Código ISO de dos letras (BO, PE, ...).
    country_code = Column(
        String(2),
        nullable=False
    )

    # Vacío = nacional.
    city = Column(
        String(100),
        nullable=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    phone = Column(
        String(50),
        nullable=False
    )

    # Menor = se muestra antes.
    sort_order = Column(
        Integer,
        nullable=False,
        default=0
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
