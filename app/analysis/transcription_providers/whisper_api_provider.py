import logging

import httpx

from app.core.config import (
    settings
)

from app.analysis.transcription_providers.base_provider import (
    BaseTranscriptionProvider
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


logger = logging.getLogger(__name__)


class WhisperApiTranscriptionProvider(
    BaseTranscriptionProvider
):
    """
    Transcribe audio enviándolo a un servidor Whisper
    compatible con la API de OpenAI
    (POST /v1/audio/transcriptions).

    Permite que Whisper corra en otra máquina con GPU
    (por ejemplo faster-whisper-server o speaches)
    y el backend solo haga la petición HTTP.
    """

    def transcribe(
        self,
        audio_content: bytes,
        filename: str,
    ) -> dict:

        try:

            response = httpx.post(
                f"{settings.WHISPER_API_URL}/v1/audio/transcriptions",
                files={
                    "file": (filename, audio_content)
                },
                data={
                    "model": settings.WHISPER_MODEL,
                    "language": settings.WHISPER_LANGUAGE,
                    "response_format": "json"
                },
                timeout=settings.WHISPER_TIMEOUT_SECONDS
            )

            response.raise_for_status()

            text = response.json()["text"]

        except (
            httpx.HTTPError,
            KeyError,
            TypeError,
            ValueError,
        ) as e:

            logger.warning(
                "Whisper no respondió correctamente: %s",
                e
            )

            raise AIProviderException(
                "El servicio de transcripción no está disponible."
            ) from e

        return {
            "text": (text or "").strip(),
            "provider": f"WHISPER:{settings.WHISPER_MODEL}"
        }
