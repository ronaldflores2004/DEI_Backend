from datetime import datetime

from sqlalchemy.orm import Session

from app.identity.models.password_reset_code import (
    PasswordResetCode
)


class PasswordResetRepository:
    """
    Acceso a datos de los códigos de recuperación
    de contraseña.
    """

    @staticmethod
    def count_created_since(
        db: Session,
        user_id: int,
        since: datetime
    ) -> int:

        return (
            db.query(PasswordResetCode)
            .filter(
                PasswordResetCode.user_id == user_id,
                PasswordResetCode.created_at >= since
            )
            .count()
        )

    @staticmethod
    def get_active(
        db: Session,
        user_id: int,
        now: datetime,
        for_update: bool = False
    ) -> PasswordResetCode | None:
        """
        Último código vigente (sin usar y sin expirar).
        Con for_update bloquea la fila para que dos
        intentos simultáneos no se salten el contador.
        """

        query = db.query(PasswordResetCode)

        if for_update:
            query = query.with_for_update()

        return (
            query
            .filter(
                PasswordResetCode.user_id == user_id,
                PasswordResetCode.consumed_at.is_(None),
                PasswordResetCode.expires_at > now
            )
            .order_by(
                PasswordResetCode.created_at.desc(),
                PasswordResetCode.id.desc()
            )
            .first()
        )

    @staticmethod
    def consume_all(
        db: Session,
        user_id: int,
        now: datetime
    ) -> None:
        """
        Anula todos los códigos pendientes del usuario.
        No hace commit.
        """

        (
            db.query(PasswordResetCode)
            .filter(
                PasswordResetCode.user_id == user_id,
                PasswordResetCode.consumed_at.is_(None)
            )
            .update(
                {"consumed_at": now},
                synchronize_session=False
            )
        )

    @staticmethod
    def add(
        db: Session,
        reset_code: PasswordResetCode
    ) -> None:
        """
        Agrega el código a la sesión. No hace commit.
        """

        db.add(reset_code)
