import hashlib
import hmac
import logging
import secrets

from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password

from app.identity.models.password_reset_code import (
    PasswordResetCode
)
from app.identity.models.user import User

from app.identity.repositories.password_reset_repository import (
    PasswordResetRepository
)
from app.identity.repositories.user_repository import (
    UserRepository
)

from app.shared.email.email_sender import EmailSender

logger = logging.getLogger(__name__)


# Mismo texto exista o no la cuenta: la respuesta no
# debe revelar qué correos están registrados.
FORGOT_PASSWORD_MESSAGE = (
    "Si el correo está registrado, te enviamos un código "
    "para restablecer tu contraseña."
)

RESET_PASSWORD_MESSAGE = (
    "Contraseña actualizada. Inicia sesión con tu nueva "
    "contraseña."
)

INVALID_CODE_DETAIL = "Código inválido o expirado"

CODE_LENGTH = 6


@dataclass
class ResetEmail:
    """
    Correo pendiente de envío. Se envía en segundo
    plano para que la respuesta tarde lo mismo exista
    o no la cuenta.
    """

    to: str
    subject: str
    body: str

    def send(self) -> None:
        EmailSender.send(
            to=self.to,
            subject=self.subject,
            body=self.body
        )


class PasswordResetService:
    """
    Recuperación de contraseña con un código de 6
    dígitos enviado por correo.

    - El código se guarda como HMAC (nunca en claro).
    - Vence a los PASSWORD_RESET_CODE_TTL_MINUTES.
    - Admite PASSWORD_RESET_MAX_ATTEMPTS intentos
      fallidos; después queda anulado.
    - Pedir un código nuevo anula los anteriores.
    - Al restablecer se cierran todas las sesiones.
    """

    # =================================================
    # Utilidades
    # =================================================

    @staticmethod
    def _generate_code() -> str:
        return f"{secrets.randbelow(10 ** CODE_LENGTH):0{CODE_LENGTH}d}"

    @staticmethod
    def _hash_code(user_id: int, code: str) -> str:
        """
        HMAC con SECRET_KEY y ligado al usuario: aunque
        se filtre la tabla, no se puede probar los
        10^6 códigos sin la clave.
        """

        return hmac.new(
            settings.SECRET_KEY.encode(),
            f"password-reset:{user_id}:{code}".encode(),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def _now() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def _find_user(
        db: Session,
        email: str
    ) -> User | None:

        user = UserRepository.get_by_email(db, email)

        if user is None or not user.is_active:
            return None

        return user

    # =================================================
    # 1. Solicitar código
    # =================================================

    @staticmethod
    def request_reset(
        db: Session,
        email: str,
        requested_ip: str | None = None
    ) -> ResetEmail | None:
        """
        Crea un código y devuelve el correo a enviar, o
        None si no corresponde enviar nada (cuenta
        inexistente, desactivada o límite por hora). El
        llamador responde lo mismo en todos los casos.
        """

        user = PasswordResetService._find_user(db, email)

        if user is None:
            return None

        now = PasswordResetService._now()

        sent_last_hour = PasswordResetRepository.count_created_since(
            db=db,
            user_id=user.id,
            since=now - timedelta(hours=1)
        )

        if sent_last_hour >= settings.PASSWORD_RESET_MAX_REQUESTS_PER_HOUR:
            logger.warning(
                "Límite de códigos de recuperación alcanzado "
                "para el usuario %s.",
                user.id
            )
            return None

        code = PasswordResetService._generate_code()

        try:

            PasswordResetRepository.consume_all(
                db=db,
                user_id=user.id,
                now=now
            )

            PasswordResetRepository.add(
                db=db,
                reset_code=PasswordResetCode(
                    user_id=user.id,
                    code_hash=PasswordResetService._hash_code(
                        user.id,
                        code
                    ),
                    expires_at=now + timedelta(
                        minutes=settings.PASSWORD_RESET_CODE_TTL_MINUTES
                    ),
                    failed_attempts=0,
                    requested_ip=requested_ip,
                    created_at=now
                )
            )

            db.commit()

        except Exception:

            db.rollback()
            raise

        logger.info(
            "Código de recuperación creado para el usuario %s.",
            user.id
        )

        minutes = settings.PASSWORD_RESET_CODE_TTL_MINUTES

        return ResetEmail(
            to=user.email,
            subject="DEI: código para restablecer tu contraseña",
            body=(
                "Hola,\n\n"
                "Recibimos una solicitud para restablecer la "
                "contraseña de tu cuenta de DEI.\n\n"
                f"Tu código es: {code}\n\n"
                f"Vence en {minutes} minutos y solo se puede "
                "usar una vez. No lo compartas con nadie: el "
                "equipo de DEI nunca te lo pedirá.\n\n"
                "Si no fuiste tú, ignora este correo. Tu "
                "contraseña no cambiará.\n"
            )
        )

    # =================================================
    # 2. Verificar código
    # =================================================

    @staticmethod
    def _check_code(
        db: Session,
        email: str,
        code: str
    ) -> tuple[User, PasswordResetCode]:
        """
        Valida el código y cuenta el intento fallido.
        Lanza 400 con el mismo mensaje en cualquier
        caso de error.
        """

        invalid = HTTPException(
            status_code=400,
            detail=INVALID_CODE_DETAIL
        )

        user = PasswordResetService._find_user(db, email)

        if user is None:
            # Mismo trabajo que con una cuenta real.
            PasswordResetService._hash_code(0, code)
            raise invalid

        now = PasswordResetService._now()

        reset_code = PasswordResetRepository.get_active(
            db=db,
            user_id=user.id,
            now=now,
            for_update=True
        )

        if reset_code is None:
            PasswordResetService._hash_code(user.id, code)
            db.rollback()
            raise invalid

        expected = PasswordResetService._hash_code(
            user.id,
            code
        )

        if hmac.compare_digest(expected, reset_code.code_hash):
            return user, reset_code

        reset_code.failed_attempts = (
            reset_code.failed_attempts or 0
        ) + 1

        if reset_code.failed_attempts >= settings.PASSWORD_RESET_MAX_ATTEMPTS:
            reset_code.consumed_at = now
            logger.warning(
                "Código de recuperación anulado por intentos "
                "fallidos (usuario %s).",
                user.id
            )

        db.commit()

        raise invalid

    @staticmethod
    def verify_code(
        db: Session,
        email: str,
        code: str
    ) -> bool:
        """
        Comprueba el código sin consumirlo, para que la
        app pase a la pantalla de nueva contraseña.
        """

        PasswordResetService._check_code(db, email, code)

        db.rollback()

        return True

    # =================================================
    # 3. Restablecer contraseña
    # =================================================

    @staticmethod
    def reset_password(
        db: Session,
        email: str,
        code: str,
        new_password: str
    ) -> ResetEmail:
        """
        Cambia la contraseña, anula todos los códigos
        pendientes y cierra todas las sesiones. Devuelve
        el aviso de cambio para enviar al usuario.
        """

        user, reset_code = PasswordResetService._check_code(
            db,
            email,
            code
        )

        now = PasswordResetService._now()

        try:

            user.password_hash = hash_password(new_password)
            user.token_version = (user.token_version or 0) + 1

            reset_code.consumed_at = now

            PasswordResetRepository.consume_all(
                db=db,
                user_id=user.id,
                now=now
            )

            db.commit()

        except Exception:

            db.rollback()
            raise

        logger.info(
            "Contraseña restablecida para el usuario %s.",
            user.id
        )

        return ResetEmail(
            to=user.email,
            subject="DEI: tu contraseña fue cambiada",
            body=(
                "Hola,\n\n"
                "La contraseña de tu cuenta de DEI se cambió "
                "correctamente y se cerraron todas las sesiones "
                "abiertas.\n\n"
                "Si no fuiste tú, solicita un nuevo código "
                "desde la app de inmediato y avisa al equipo "
                "de DEI.\n"
            )
        )
