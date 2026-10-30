import time

import pytest

from sqlalchemy import text

from app.analysis.models.emotional_analysis import EmotionalAnalysis
from app.notifications.models.notification import Notification
from app.shared.enums.risk_level_enum import RiskLevelEnum
from app.shared.safety.risk_phrase_screening import (
    highest_risk,
    screen_risk_phrases,
)

from tests.clinical_fixtures import world  # noqa: F401


# =====================================
# Filtro de frases de riesgo
# =====================================

@pytest.mark.parametrize("phrase, expected", [
    ("Tengo ganas de morir", RiskLevelEnum.HIGH),
    ("A veces pienso que estarían mejor sin mí", RiskLevelEnum.HIGH),
    ("Anoche me corté los brazos", RiskLevelEnum.HIGH),
    ("Me voy a matar", RiskLevelEnum.CRITICAL),
    ("Ya compré las pastillas, esta noche lo hago", RiskLevelEnum.CRITICAL),
    ("Hoy salí a caminar con mi perro", None),
    ("Me corté el pelo", None),
    ("Me mató de risa el chiste", None),
    (None, None),
])
def test_screen_risk_phrases(phrase, expected):

    assert screen_risk_phrases(phrase) == expected


def test_highest_risk_keeps_the_most_severe():

    assert highest_risk("LOW", RiskLevelEnum.HIGH) == RiskLevelEnum.HIGH
    assert highest_risk("CRITICAL", None) == RiskLevelEnum.CRITICAL
    assert highest_risk("no-valido", None) is None


# =====================================
# Riesgo fijado por el sistema y crisis
# =====================================

def test_patient_cannot_set_own_risk(world):

    world.accept_consents()
    entry_id = world.create_entry("Hoy salí a caminar")

    analysis = world.manual_analysis(entry_id, risk_level="CRITICAL")

    assert analysis["risk_level"] is None
    assert analysis["crisis_support"] is None


def test_high_risk_gives_crisis_support_and_alerts_professional(world):

    world.accept_consents()
    world.link_professional()
    entry_id = world.create_entry("Tengo ganas de morir")

    analysis = world.manual_analysis(entry_id, risk_level="LOW")

    assert analysis["risk_level"] == "HIGH"
    support = analysis["crisis_support"]
    assert support["professional_notified"] is True
    assert any(line["phone"] == "800 11 30 40" for line in support["lines"])

    db = world.Session()
    notification = db.query(Notification).filter_by(type="RISK_ALERT").one()
    # La notificación no expone lo que escribió el paciente.
    assert "morir" not in notification.message


def test_auto_analysis_never_below_phrase_filter(world):

    world.accept_consents()
    entry_id = world.create_entry("Me voy a matar, ya no aguanto")

    response = world.as_patient().post(f"/analysis/entries/{entry_id}/auto")

    assert response.status_code == 200, response.text
    assert response.json()["risk_level"] == "CRITICAL"


# =====================================
# Consentimientos
# =====================================

def test_diary_requires_informed_consent(world):

    response = world.as_patient().post(
        "/entries",
        json={"entry_type": "TEXT", "text_content": "Hola"},
    )

    assert response.status_code == 403


def test_outdated_consent_version_is_rejected(world):

    response = world.as_patient().post(
        "/platform-consents",
        json={"consent_type": "INFORMED_CONSENT", "version": "0.1"},
    )

    assert response.status_code == 400


def test_ai_analysis_requires_ai_consent_and_can_be_revoked(world):

    world.accept_consents(ai=False)
    entry_id = world.create_entry("Hoy fue un día difícil")
    client = world.as_patient()

    assert client.post(f"/analysis/entries/{entry_id}/auto").status_code == 403

    client.post("/platform-consents", json={"consent_type": "AI_PROCESSING", "version": "1.0"})
    assert client.post(f"/analysis/entries/{entry_id}/auto").status_code == 200

    client.patch("/platform-consents/AI_PROCESSING/revoke")
    assert client.post(f"/analysis/entries/{entry_id}/reanalyze").status_code == 403

    assert client.patch("/platform-consents/INFORMED_CONSENT/revoke").status_code == 400


def test_weekly_summary_skips_ai_without_consent(world, monkeypatch):

    world.accept_consents()
    entry_id = world.create_entry("Me siento con ansiedad por el trabajo")
    world.as_patient().post(f"/analysis/entries/{entry_id}/auto")
    world.as_patient().patch("/platform-consents/AI_PROCESSING/revoke")

    from app.shared.ai.provider_chain import AIProviderChain

    def fail(**kwargs):
        raise AssertionError("No debe llamarse a la IA")

    monkeypatch.setattr(AIProviderChain, "run", staticmethod(fail))

    response = world.as_patient().get("/analysis/weekly-summary")

    assert response.status_code == 200, response.text
    assert response.json()["ai_summary"] is None


# =====================================
# Historial compartido y alertas con estado
# =====================================

@pytest.mark.parametrize("sharing_mode, expected_alerts", [
    ("NEW_ONLY", 1),
    ("FULL_HISTORY", 2),
])
def test_sharing_mode_limits_what_professional_sees(world, sharing_mode, expected_alerts):

    world.accept_consents()
    old_entry = world.create_entry("Tengo ganas de morir")
    world.manual_analysis(old_entry)

    time.sleep(0.01)
    world.link_professional(sharing_mode)
    time.sleep(0.01)

    new_entry = world.create_entry("No quiero vivir")
    world.manual_analysis(new_entry)

    alerts = world.as_professional().get("/risk-alerts").json()

    assert alerts[0]["alerts_count"] == expected_alerts


def test_from_date_requires_share_from(world):

    response = world.as_patient().post(
        "/therapy/link-requests",
        json={"professional_id": world.professional_id, "sharing_mode": "FROM_DATE"},
    )

    assert response.status_code == 422


def test_risk_alert_lifecycle_and_audit(world):

    world.accept_consents()
    world.link_professional()
    world.manual_analysis(world.create_entry("Tengo ganas de morir"))

    professional = world.as_professional()
    inbox = professional.get("/risk-alerts/inbox").json()

    assert [alert["status"] for alert in inbox] == ["NEW"]

    alert_id = inbox[0]["id"]

    assert professional.patch(f"/risk-alerts/{alert_id}/seen").json()["status"] == "SEEN"

    resolved = professional.patch(
        f"/risk-alerts/{alert_id}/resolve",
        json={"resolution_note": "Llamé a la paciente"},
    ).json()

    assert resolved["status"] == "RESOLVED"
    assert professional.get("/risk-alerts/inbox?status=NEW").json() == []

    log = world.as_patient().get("/audit/my-access-log").json()
    actions = {item["action"] for item in log}

    assert {"VIEW_RISK_ALERTS", "REVIEW_RISK_ALERT"} <= actions
    assert log[0]["professional_name"] == "Luis Ruiz"


# =====================================
# Recomendaciones revisadas por el profesional
# =====================================

def _auto_analysis_id(world, text_content: str) -> int:

    entry_id = world.create_entry(text_content)
    response = world.as_patient().post(f"/analysis/entries/{entry_id}/auto")
    assert response.status_code == 200, response.text

    return response.json()["id"]


def test_ai_recommendation_waits_for_professional_review(world):

    world.accept_consents()
    world.link_professional()
    analysis_id = _auto_analysis_id(world, "Me siento con estrés por los exámenes")

    patient = world.as_patient()
    generated = patient.post(f"/recommendations/generate/{analysis_id}").json()

    assert generated["status"] == "PENDING_REVIEW"
    assert generated["content"] is None
    assert patient.get("/recommendations").json() == []

    professional = world.as_professional()
    pending = professional.get("/recommendations/review/pending").json()

    assert [item["id"] for item in pending] == [generated["id"]]

    approved = professional.patch(
        f"/recommendations/review/{generated['id']}/approve",
        json={"content": "Practica respiración 4-7-8 antes de estudiar."},
    ).json()

    assert approved["status"] == "APPROVED"

    visible = world.as_patient().get("/recommendations").json()

    assert visible[0]["content"] == "Practica respiración 4-7-8 antes de estudiar."


def test_no_ai_recommendation_for_high_risk_without_professional(world):

    world.accept_consents()
    entry_id = world.create_entry("Tengo ganas de morir")
    analysis_id = world.manual_analysis(entry_id)["id"]

    response = world.as_patient().post(f"/recommendations/generate/{analysis_id}")

    assert response.status_code == 409


# =====================================
# Datos del paciente y cifrado
# =====================================

def test_clinical_text_is_encrypted_at_rest(world):

    world.accept_consents()
    entry_id = world.create_entry("Texto íntimo del diario")
    world.manual_analysis(entry_id)

    with world.engine.connect() as connection:
        raw_entry = connection.execute(text("SELECT text_content FROM emotional_entries")).scalar()
        raw_analysis = connection.execute(text("SELECT analysis_json FROM emotional_analyses")).scalar()

    assert raw_entry.startswith("gAAAAA")
    assert raw_analysis.startswith("gAAAAA")

    db = world.Session()
    assert db.get(EmotionalAnalysis, 1).analysis_json == {}


def test_export_and_erase_my_data(world):

    world.accept_consents()
    world.link_professional()
    world.manual_analysis(world.create_entry("Tengo ganas de morir"))

    patient = world.as_patient()
    exported = patient.get("/patients/me/data/export").json()

    assert exported["entries"][0]["text_content"] == "Tengo ganas de morir"
    assert exported["entries"][0]["analysis"]["risk_level"] == "HIGH"

    assert patient.post("/patients/me/data/erase", json={"confirmation": "si"}).status_code == 400
    assert patient.post("/patients/me/data/erase", json={"confirmation": "ELIMINAR"}).status_code == 200

    with world.engine.connect() as connection:
        assert connection.execute(text("SELECT count(*) FROM emotional_entries")).scalar() == 0
        assert connection.execute(text("SELECT count(*) FROM risk_alerts")).scalar() == 0
        assert connection.execute(text("SELECT active FROM patient_professionals")).scalar() == 0
        assert connection.execute(text("SELECT is_active FROM users WHERE role = 'PATIENT'")).scalar() == 0


# =====================================
# Configuración de producción
# =====================================

def test_production_rejects_fake_provider():

    import os
    import subprocess
    import sys

    env = {
        **os.environ,
        "APP_ENV": "production",
        "AI_PROVIDER_CHAIN": "OLLAMA,FAKE",
    }

    result = subprocess.run(
        [sys.executable, "-c", "import app.core.config"],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "FAKE" in result.stderr
