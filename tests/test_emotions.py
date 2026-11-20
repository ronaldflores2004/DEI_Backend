import pytest

from app.analysis.prompts import build_analysis_prompt
from app.analysis.providers.analysis_parser import AnalysisParser
from app.shared.emotions import EMOTIONS, is_negative, normalize_emotion


@pytest.mark.parametrize("raw, expected", [
    ("TRISTEZA", "Tristeza"),
    ("estres", "Estrés"),
    ("  Ansiedad ", "Ansiedad"),
    ("nostalgia", "Nostalgia"),
    ("", None),
])
def test_normalize_emotion(raw, expected):

    assert normalize_emotion(raw) == expected


def test_negative_emotions_match_any_spelling():

    # DEI_AI devuelve mayúsculas sin tildes.
    assert is_negative("ESTRES")
    assert is_negative("Tristeza")
    assert not is_negative("CALMA")


def test_parser_stores_canonical_emotion():

    result = AnalysisParser.from_dict(
        data={
            "primary_emotion": "TRISTEZA",
            "emotion_intensity": "high",
            "risk_level": "low",
            "analysis_json": {},
        },
        provider="OLLAMA",
        model="test",
    )

    assert result["primary_emotion"] == "Tristeza"


def test_analysis_prompt_defines_risk_levels_and_emotions():

    prompt = build_analysis_prompt("hola")

    assert "CRITICAL: intención o plan" in prompt
    assert "no diagnosticas" in prompt
    assert all(emotion in prompt for emotion in EMOTIONS)
    assert '"primary_emotion": ""' in prompt


# Valores que devuelve DEI_AI (EmotionEnum de dei_ai, mayúsculas sin
# tildes). Si esta prueba falla, los catálogos de los dos repositorios
# ya no coinciden: hay que cambiar ambos.
DEI_AI_EMOTIONS = [
    "ALEGRIA", "TRISTEZA", "ANSIEDAD", "MIEDO", "IRA", "ASCO",
    "SORPRESA", "CALMA", "ESTRES", "DESANIMO", "CULPA", "VERGUENZA",
    "SOLEDAD", "FRUSTRACION", "CONFUSION", "ESPERANZA", "CONFIANZA",
    "GRATITUD", "AGOTAMIENTO", "AMOR", "PREOCUPACION", "DESESPERANZA",
]


def test_catalog_matches_dei_ai():

    assert [normalize_emotion(e) for e in DEI_AI_EMOTIONS] == EMOTIONS
    assert len(set(EMOTIONS)) == 22


def test_every_emotion_has_a_valence_or_is_neutral():

    from app.shared.emotions import NEGATIVE_EMOTIONS, POSITIVE_EMOTIONS

    assert NEGATIVE_EMOTIONS <= set(EMOTIONS)
    assert POSITIVE_EMOTIONS <= set(EMOTIONS)
    assert not NEGATIVE_EMOTIONS & POSITIVE_EMOTIONS
    assert is_negative("DESESPERANZA")
    assert is_negative("PREOCUPACION")


@pytest.mark.parametrize("raw, expected", [
    ("enojo", "Ira"),
    ("Melancolía", "Tristeza"),
    ("inquietud", "Preocupación"),
    ("CANSANCIO", "Agotamiento"),
])
def test_aliases_shared_with_dei_ai(raw, expected):

    assert normalize_emotion(raw) == expected
