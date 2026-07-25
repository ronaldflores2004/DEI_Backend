from app.analysis.transcription_providers.base_provider import (
    BaseTranscriptionProvider
)


class LocalTranscriptionProvider(
    BaseTranscriptionProvider
):

    def transcribe(
        self,
        audio_content: bytes,
        filename: str,
    ) -> dict:

        raise NotImplementedError(
            "Local Transcription Provider aún no implementado."
        )