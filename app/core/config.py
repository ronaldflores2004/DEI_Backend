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

    # development o production. En production no se
    # permite el proveedor FAKE: inventa resultados,
    # incluido el nivel de riesgo.
    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development"
    ).lower()

    # Por defecto, primero la IA local (sin costo
    # de tokens) y Gemini como respaldo.
    AI_PROVIDER: str = os.getenv(
        "AI_PROVIDER",
        "OLLAMA"
    )

    AI_FALLBACK_PROVIDER: str = os.getenv(
        "AI_FALLBACK_PROVIDER",
        "GEMINI"
    )
    
    # Orden en que se prueban los proveedores de IA.
    # Ejemplo: OLLAMA,GEMINI,FAKE
    # Si no se define, se arma con AI_PROVIDER y
    # AI_FALLBACK_PROVIDER para no romper los .env actuales.
    AI_PROVIDER_CHAIN: list[str] = [
        provider.strip().upper()
        for provider in os.getenv(
            "AI_PROVIDER_CHAIN",
            f"{AI_PROVIDER},{AI_FALLBACK_PROVIDER}"
        ).split(",")
        if provider.strip()
    ]

    # =================================================
    # IA local (Ollama)
    # =================================================

    OLLAMA_BASE_URL: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    ).rstrip("/")

    OLLAMA_MODEL: str = os.getenv(
        "OLLAMA_MODEL",
        "llama3.1:8b"
    )

    OLLAMA_TIMEOUT_SECONDS: float = float(
        os.getenv("OLLAMA_TIMEOUT_SECONDS", "120")
    )

    # =================================================
    # Transcripción (Whisper)
    # =================================================

    TRANSCRIPTION_PROVIDER: str = os.getenv(
        "TRANSCRIPTION_PROVIDER",
        "WHISPER_API"
    )

    # Servidor Whisper compatible con la API de OpenAI
    # (/v1/audio/transcriptions), por ejemplo
    # faster-whisper-server o speaches en la otra laptop.
    WHISPER_API_URL: str = os.getenv(
        "WHISPER_API_URL",
        "http://localhost:8000"
    ).rstrip("/")

    WHISPER_MODEL: str = os.getenv(
        "WHISPER_MODEL",
        "small"
    )

    WHISPER_LANGUAGE: str = os.getenv(
        "WHISPER_LANGUAGE",
        "es"
    )

    WHISPER_TIMEOUT_SECONDS: float = float(
        os.getenv("WHISPER_TIMEOUT_SECONDS", "300")
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

if (
    settings.APP_ENV == "production"
    and "FAKE" in settings.AI_PROVIDER_CHAIN
):
    raise RuntimeError(
        "AI_PROVIDER_CHAIN no puede incluir FAKE en "
        "producción: inventa análisis y niveles de riesgo."
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