import pytest

from app.shared.ai.provider_chain import AIProviderChain
from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


class Provider:

    def __init__(self, name, fails):
        self.name = name
        self.fails = fails

    def run(self):
        if self.fails:
            raise AIProviderException(f"{self.name} caído")
        return self.name


def build(failing):
    return lambda name: Provider(name, name in failing)


def test_uses_first_provider_when_it_works():

    result = AIProviderChain.run(
        task="prueba",
        get_provider=build(failing=set()),
        call=lambda p: p.run(),
        chain=["OLLAMA", "GEMINI", "FAKE"]
    )

    assert result == "OLLAMA"


def test_falls_back_in_order():

    result = AIProviderChain.run(
        task="prueba",
        get_provider=build(failing={"OLLAMA"}),
        call=lambda p: p.run(),
        chain=["OLLAMA", "GEMINI", "FAKE"]
    )

    assert result == "GEMINI"

    result = AIProviderChain.run(
        task="prueba",
        get_provider=build(failing={"OLLAMA", "GEMINI"}),
        call=lambda p: p.run(),
        chain=["OLLAMA", "GEMINI", "FAKE"]
    )

    assert result == "FAKE"


def test_raises_when_every_provider_fails():

    with pytest.raises(AIProviderException):
        AIProviderChain.run(
            task="prueba",
            get_provider=build(failing={"OLLAMA", "GEMINI"}),
            call=lambda p: p.run(),
            chain=["OLLAMA", "GEMINI"]
        )


def test_default_chain_comes_from_settings():

    from app.core.config import settings

    assert settings.AI_PROVIDER_CHAIN == ["OLLAMA", "GEMINI", "FAKE"]
