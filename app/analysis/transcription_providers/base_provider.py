from abc import ABC
from abc import abstractmethod


class BaseTranscriptionProvider(ABC):
    """
    Contrato para proveedores automáticos
    de transcripción de audio.
    """

    @abstractmethod
    def transcribe(
        self,
        audio_content: bytes,
        filename: str,
    ) -> dict:
        pass