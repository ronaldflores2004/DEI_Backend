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

    AI_PROVIDER: str = os.getenv(
        "AI_PROVIDER",
        "GEMINI"
    )

    AI_FALLBACK_PROVIDER: str = os.getenv(
        "AI_FALLBACK_PROVIDER",
        "FAKE"
    )
    
    TRANSCRIPTION_PROVIDER: str = os.getenv(
        "TRANSCRIPTION_PROVIDER",
        "LOCAL"
    )
    
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]


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

if len(settings.SECRET_KEY) < 32:
    raise RuntimeError(
        "SECRET_KEY debe tener al menos 32 caracteres."
    )
    
if settings.ALGORITHM != "HS256":
    raise RuntimeError(
        "ALGORITHM no soportado. Use HS256."
    )

# =====================================================
# Compatibilidad con el código existente
# Se eliminará cuando toda la migración termine.
# =====================================================

DATABASE_URL = settings.DATABASE_URL
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
GEMINI_API_KEY = settings.GEMINI_API_KEY
AI_PROVIDER = settings.AI_PROVIDER
AI_FALLBACK_PROVIDER = settings.AI_FALLBACK_PROVIDER
TRANSCRIPTION_PROVIDER = settings.TRANSCRIPTION_PROVIDER