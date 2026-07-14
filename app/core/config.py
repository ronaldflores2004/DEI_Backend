import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración global del proyecto."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()

# =====================================================
# Validación de configuración
# =====================================================

if not settings.DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no configurada."
    )

if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY no configurada."
    )
    
# =====================================================
# Compatibilidad con el código existente
# Se eliminará cuando toda la migración termine.
# =====================================================

DATABASE_URL = settings.DATABASE_URL
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
GEMINI_API_KEY = settings.GEMINI_API_KEY