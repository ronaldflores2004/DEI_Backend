from fastapi.testclient import TestClient

from app.main import app


def test_app_starts_without_gemini_key():

    client = TestClient(app)

    assert client.get("/").status_code == 200


def test_ai_health_requires_authentication():

    client = TestClient(app)

    assert client.get("/health/ai").status_code == 401
