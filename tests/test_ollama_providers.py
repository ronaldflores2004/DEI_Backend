import json

import pytest

from types import SimpleNamespace

from app.analysis.providers.ollama_provider import OllamaProvider
from app.analysis.summary_providers.ollama_provider import (
    OllamaSummaryProvider
)
from app.recommendations.providers.ollama_provider import (
    OllamaRecommendationProvider
)
from app.shared.ai.ollama_client import OllamaClient
from app.shared.enums.risk_level_enum import RiskLevelEnum
from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)

from tests.fakes import install_fake_http, ollama_reply, unreachable


def test_analysis_sends_json_request_to_configured_server(monkeypatch):

    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["body"] = json.loads(request.content)
        return ollama_reply(json.dumps({
            "primary_emotion": "Tristeza",
            "emotion_intensity": "MEDIUM",
            "risk_level": "LOW",
            "analysis_json": {"sentiment": "Negativo", "topics": [], "triggers": []}
        }))

    install_fake_http(monkeypatch, handler)

    result = OllamaProvider().analyze("Hoy me siento triste")

    assert seen["url"] == "http://ollama.test:11434/api/chat"
    assert seen["body"]["model"] == "llama3.1:8b"
    assert seen["body"]["format"] == "json"
    assert seen["body"]["stream"] is False
    assert result["provider"] == "OLLAMA"
    assert result["model"] == "llama3.1:8b"
    assert result["risk_level"] is RiskLevelEnum.LOW


def test_unreachable_ollama_raises_provider_exception(monkeypatch):

    install_fake_http(monkeypatch, unreachable)

    with pytest.raises(AIProviderException):
        OllamaProvider().analyze("texto")


def test_server_error_raises_provider_exception(monkeypatch):

    install_fake_http(
        monkeypatch,
        lambda request: ollama_reply("x").__class__(500, text="model not found")
    )

    with pytest.raises(AIProviderException):
        OllamaSummaryProvider().generate("Calma", "Calma", "LOW", [], [])


def test_summary_returns_plain_text(monkeypatch):

    install_fake_http(
        monkeypatch,
        lambda request: ollama_reply('"Esta semana predominó la calma."\n')
    )

    summary = OllamaSummaryProvider().generate(
        "Calma", "Alegría", "LOW", ["familia"], []
    )

    assert summary == "Esta semana predominó la calma."


def test_recommendation_requires_title_and_content(monkeypatch):

    analysis = SimpleNamespace(
        primary_emotion="Estrés",
        emotion_intensity="HIGH",
        risk_level="MEDIUM",
        analysis_json={"topics": ["exámenes"], "triggers": []}
    )

    install_fake_http(
        monkeypatch,
        lambda request: ollama_reply(json.dumps({
            "title": "Pausas activas",
            "content": "Toma descansos cortos."
        }))
    )

    result = OllamaRecommendationProvider().generate(analysis)

    assert result == {
        "title": "Pausas activas",
        "content": "Toma descansos cortos.",
        "source": "OLLAMA"
    }

    install_fake_http(
        monkeypatch,
        lambda request: ollama_reply(json.dumps({"title": "Solo título"}))
    )

    with pytest.raises(AIProviderException):
        OllamaRecommendationProvider().generate(analysis)


def test_health_reports_model_availability(monkeypatch):

    install_fake_http(
        monkeypatch,
        lambda request: ollama_reply("").__class__(
            200,
            json={"models": [{"name": "llama3.1:8b"}, {"name": "qwen2.5:7b"}]}
        )
    )

    health = OllamaClient.health()

    assert health["reachable"] is True
    assert health["model_available"] is True

    install_fake_http(monkeypatch, unreachable)

    assert OllamaClient.health()["reachable"] is False
