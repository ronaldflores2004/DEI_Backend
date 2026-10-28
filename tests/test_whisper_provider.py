import httpx
import pytest

from app.analysis.transcription_providers.provider_factory import (
    TranscriptionProviderFactory
)
from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)

from tests.fakes import install_fake_http, unreachable


def test_whisper_api_uploads_audio(monkeypatch):

    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["body"] = request.content
        return httpx.Response(200, json={"text": " Hola, hoy fue un buen día. "})

    install_fake_http(monkeypatch, handler)

    provider = TranscriptionProviderFactory.get_provider("WHISPER_API")

    result = provider.transcribe(b"audio-bytes", "nota.webm")

    assert seen["url"] == "http://whisper.test:8000/v1/audio/transcriptions"
    assert b"audio-bytes" in seen["body"]
    assert b'name="language"' in seen["body"]
    assert result["text"] == "Hola, hoy fue un buen día."
    assert result["provider"].startswith("WHISPER:")


def test_whisper_api_unreachable(monkeypatch):

    install_fake_http(monkeypatch, unreachable)

    provider = TranscriptionProviderFactory.get_provider("WHISPER_API")

    with pytest.raises(AIProviderException):
        provider.transcribe(b"audio", "nota.webm")
