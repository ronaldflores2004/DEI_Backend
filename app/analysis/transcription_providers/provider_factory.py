from app.analysis.transcription_providers.base_provider import (
    BaseTranscriptionProvider
)

from app.analysis.transcription_providers.local_provider import (
    LocalTranscriptionProvider
)

from app.analysis.transcription_providers.whisper_api_provider import (
    WhisperApiTranscriptionProvider
)


class TranscriptionProviderFactory:
    """
    Fábrica encargada de devolver
    el proveedor de transcripción automática.
    """

    @staticmethod
    def get_provider(
        provider: str,
    ) -> BaseTranscriptionProvider:

        provider = provider.upper()

        if provider == "WHISPER_API":
            return WhisperApiTranscriptionProvider()

        if provider == "LOCAL":
            return LocalTranscriptionProvider()

        raise ValueError(
            f"Proveedor de transcripción "
            f"'{provider}' no soportado."
        )