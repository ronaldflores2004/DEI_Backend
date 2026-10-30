from functools import lru_cache

from google import genai

from app.core.config import (
    settings
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client:
    """
    Crea el cliente de Gemini solo cuando se usa,
    así el backend puede arrancar sin GEMINI_API_KEY
    si trabaja únicamente con la IA local.
    """

    if not settings.GEMINI_API_KEY:
        raise AIProviderException(
            "GEMINI_API_KEY no configurada."
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY
    )
