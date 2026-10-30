import json
import os
from functools import lru_cache

from cryptography.fernet import Fernet, MultiFernet

from sqlalchemy.types import Text, TypeDecorator


# =====================================
# CIFRADO DE DATOS CLÍNICOS EN REPOSO
# =====================================
#
# DATA_ENCRYPTION_KEYS: una o más claves Fernet
# separadas por comas. La primera cifra; todas
# descifran, lo que permite rotar claves.
#
# Generar una clave:
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
#
# Si se pierde la clave, los diarios no se pueden
# recuperar: guardarla fuera del servidor.

# Todo token Fernet empieza así (versión 0x80 en
# base64). Sirve para leer datos anteriores al
# cifrado, que siguen en texto plano.
TOKEN_PREFIX = "gAAAAA"


@lru_cache
def _get_cipher() -> MultiFernet:

    keys = [
        key.strip()
        for key in os.getenv(
            "DATA_ENCRYPTION_KEYS",
            ""
        ).split(",")
        if key.strip()
    ]

    if not keys:
        raise RuntimeError(
            "DATA_ENCRYPTION_KEYS no configurada."
        )

    return MultiFernet([
        Fernet(key.encode())
        for key in keys
    ])


def validate_encryption_config() -> None:
    """
    Falla al arrancar si no hay una clave válida.
    """

    _get_cipher()


def encrypt_text(
    value: str | None
) -> str | None:

    if value is None:
        return None

    return _get_cipher().encrypt(
        value.encode()
    ).decode()


def decrypt_text(
    value: str | None
) -> str | None:

    if value is None:
        return None

    if not value.startswith(TOKEN_PREFIX):
        return value

    return _get_cipher().decrypt(
        value.encode()
    ).decode()


def encrypt_bytes(
    value: bytes
) -> bytes:

    return _get_cipher().encrypt(value)


def decrypt_bytes(
    value: bytes
) -> bytes:

    if not value.startswith(TOKEN_PREFIX.encode()):
        return value

    return _get_cipher().decrypt(value)


class EncryptedText(TypeDecorator):
    """
    Texto cifrado en la base de datos y en claro
    en el código.
    """

    impl = Text

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return encrypt_text(value)

    def process_result_value(self, value, dialect):
        return decrypt_text(value)


class EncryptedJSON(TypeDecorator):
    """
    JSON guardado como texto cifrado.
    """

    impl = Text

    cache_ok = True

    def process_bind_param(self, value, dialect):

        if value is None:
            return None

        return encrypt_text(
            json.dumps(value, ensure_ascii=False)
        )

    def process_result_value(self, value, dialect):

        if value is None:
            return None

        return json.loads(decrypt_text(value))
