import logging
import os
import tempfile

from functools import lru_cache

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


@lru_cache(maxsize=1)
def _load_model():
    """
    Carga faster-whisper una sola vez.

    Es una dependencia opcional y pesada; solo se
    necesita si Whisper corre en la misma máquina
    que el backend:  pip install faster-whisper
    """

    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise AIProviderException(
            "faster-whisper no está instalado. "
            "Instálalo o usa TRANSCRIPTION_PROVIDER=WHISPER_API."
        ) from e

    return WhisperModel(
        settings.WHISPER_MODEL
    )


class LocalTranscriptionProvider(
    BaseTranscriptionProvider
):
    """
    Transcribe audio con Whisper ejecutándose
    dentro del mismo proceso del backend.
    """

    def transcribe(
        self,
        audio_content: bytes,
        filename: str,
    ) -> dict:

        model = _load_model()

        suffix = os.path.splitext(filename)[1]

        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False
        ) as tmp:

            tmp.write(audio_content)
            path = tmp.name

        try:

            segments, _ = model.transcribe(
                path,
                language=settings.WHISPER_LANGUAGE
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            )

        except Exception as e:

            logger.error(
                "Whisper local falló transcribiendo %s: %s",
                filename,
                e
            )

            raise AIProviderException(
                "Whisper local no pudo transcribir el audio."
            ) from e

        finally:
            os.remove(path)

        return {
            "text": text.strip(),
            "provider": f"WHISPER_LOCAL:{settings.WHISPER_MODEL}"
        }
