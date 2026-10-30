import pytest

from app.analysis.providers.analysis_parser import AnalysisParser
from app.shared.enums.emotion_intensity_enum import EmotionIntensityEnum
from app.shared.enums.risk_level_enum import RiskLevelEnum
from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


def test_parses_markdown_wrapped_json():

    raw = """```json
    {"primary_emotion": "Ansiedad", "emotion_intensity": "high",
     "risk_level": "Medium",
     "analysis_json": {"sentiment": "Negativo", "topics": ["trabajo"]}}
    ```"""

    result = AnalysisParser.from_text(raw, "GEMINI", "gemini-2.5-flash")

    assert result["primary_emotion"] == "Ansiedad"
    assert result["emotion_intensity"] is EmotionIntensityEnum.HIGH
    assert result["risk_level"] is RiskLevelEnum.MEDIUM
    assert result["analysis_json"]["provider"] == "GEMINI"
    assert result["analysis_json"]["triggers"] == []


@pytest.mark.parametrize(
    "raw",
    [
        "no es json",
        '{"primary_emotion": "Calma"}',
        '{"primary_emotion": "Calma", "emotion_intensity": "ALTA", "risk_level": "LOW"}',
        '{"primary_emotion": "", "emotion_intensity": "LOW", "risk_level": "LOW"}',
    ]
)
def test_invalid_responses_trigger_fallback(raw):

    with pytest.raises(AIProviderException):
        AnalysisParser.from_text(raw, "OLLAMA", "llama3.1:8b")
