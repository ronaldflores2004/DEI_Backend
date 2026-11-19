from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index
)

from app.core.database import Base


class PasswordResetCode(Base):
    """
    Código de un solo uso para restablecer la
    contraseña. Nunca se guarda el código en claro,
    solo su HMAC.
    """

    __tablename__ = "password_reset_codes"

    __table_args__ = (

        Index(
            "ix_password_reset_codes_user_created",
            "user_id",
            "created_at"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # HMAC-SHA256 en hexadecimal del código.
    code_hash = Column(
        String(64),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    failed_attempts = Column(
        Integer,
        nullable=False,
        default=0
    )

    # Fecha en que se usó o se anuló. Mientras sea
    # nula y no haya expirado, el código sirve.
    consumed_at = Column(
        DateTime,
        nullable=True
    )

    requested_ip = Column(
        String(45),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
