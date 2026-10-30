import logging
import time

from app.core.config import settings

logger = logging.getLogger(__name__)

AI_PROVIDER_CHAIN_KEY = "AI_PROVIDER_CHAIN"

# Proveedores implementados para análisis, resumen
# y recomendaciones. Para sumar otra IA en línea hay
# que implementar su proveedor y agregarlo aquí.
SUPPORTED_PROVIDERS = ["OLLAMA", "GEMINI", "FAKE"]

# Segundos que se reutiliza el valor leído de la base.
CACHE_SECONDS = 30

_cache: dict = {"value": None, "expires": 0.0}


def parse_chain(
    value: str | list[str]
) -> list[str]:

    items = value.split(",") if isinstance(value, str) else value

    return [
        item.strip().upper()
        for item in items
        if item and item.strip()
    ]


def validate_chain(
    chain: list[str]
) -> None:
    """
    Lanza ValueError si la cadena no es válida.
    """

    if not chain:
        raise ValueError("La cadena de proveedores está vacía.")

    unknown = [
        name
        for name in chain
        if name not in SUPPORTED_PROVIDERS
    ]

    if unknown:
        raise ValueError(
            f"Proveedores no soportados: {', '.join(unknown)}. "
            f"Disponibles: {', '.join(SUPPORTED_PROVIDERS)}."
        )

    if len(set(chain)) != len(chain):
        raise ValueError("Hay proveedores repetidos.")

    if (
        settings.APP_ENV == "production"
        and "FAKE" in chain
    ):
        raise ValueError(
            "FAKE no está permitido en producción."
        )


def clear_cache() -> None:

    _cache["value"] = None
    _cache["expires"] = 0.0


def get_ai_provider_chain() -> list[str]:
    """
    Cadena elegida por el administrador o, si no
    eligió ninguna, la de AI_PROVIDER_CHAIN del .env.
    """

    if _cache["value"] and time.monotonic() < _cache["expires"]:
        return _cache["value"]

    chain = settings.AI_PROVIDER_CHAIN

    try:

        from app.core.database import SessionLocal

        from app.administration.repositories.system_setting_repository import (
            SystemSettingRepository
        )

        db = SessionLocal()

        try:
            setting = SystemSettingRepository.get(
                db=db,
                key=AI_PROVIDER_CHAIN_KEY
            )
        finally:
            db.close()

        if setting:
            stored = parse_chain(setting.value)
            validate_chain(stored)
            chain = stored

    except Exception:

        logger.warning(
            "No se pudo leer la cadena de IA del "
            "administrador; se usa la del .env.",
            exc_info=True
        )

    _cache["value"] = chain
    _cache["expires"] = time.monotonic() + CACHE_SECONDS

    return chain
