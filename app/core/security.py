from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# =====================================================
# Configuración de cifrado de contraseñas
# =====================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Genera el hash seguro de una contraseña.
    """
    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Verifica una contraseña contra su hash.
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Genera un JWT de acceso.
    """

    now = datetime.utcnow()

    payload = data.copy()

    payload.update({
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

