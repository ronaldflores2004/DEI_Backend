from datetime import date

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.dependencies import get_current_user
from app.main import app

from app.identity.models.patient_profile import PatientProfile
from app.identity.models.professional_profile import ProfessionalProfile
from app.identity.models.user import User


class ClinicalWorld:
    """
    Base de datos en memoria con un paciente y un
    profesional verificado, y un cliente HTTP que
    actúa como cualquiera de los dos.
    """

    def __init__(self, monkeypatch):

        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        Base.metadata.create_all(engine)

        self.Session = sessionmaker(bind=engine)
        self.engine = engine

        db = self.Session()

        patient_user = User(email="paciente@test.com", password_hash="x", role="PATIENT")
        professional_user = User(email="psico@test.com", password_hash="x", role="PROFESSIONAL")

        db.add_all([patient_user, professional_user])
        db.commit()

        patient = PatientProfile(
            user_id=patient_user.id,
            first_name="Ana",
            last_name="Paz",
            birth_date=date(2000, 1, 1),
            gender="FEMALE",
        )

        professional = ProfessionalProfile(
            user_id=professional_user.id,
            first_name="Luis",
            last_name="Ruiz",
            license_number="123",
            specialties="TCC",
            is_verified=True,
        )

        db.add_all([patient, professional])
        db.commit()

        self.patient_user_id = patient_user.id
        self.professional_user_id = professional_user.id
        self.patient_id = patient.id
        self.professional_id = professional.id
        self._current_user_id = patient_user.id

        db.close()

        def override_db():
            session = self.Session()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_db] = override_db
        app.dependency_overrides[get_current_user] = (
            lambda: self.Session().get(User, self._current_user_id)
        )

        # Sin servicios externos: proveedor simulado.
        monkeypatch.setattr(settings, "AI_PROVIDER_CHAIN", ["FAKE"])

        self.client = TestClient(app)

    def as_patient(self) -> TestClient:
        self._current_user_id = self.patient_user_id
        return self.client

    def as_professional(self) -> TestClient:
        self._current_user_id = self.professional_user_id
        return self.client

    def accept_consents(self, ai: bool = True) -> None:

        client = self.as_patient()

        types = ["INFORMED_CONSENT"] + (["AI_PROCESSING"] if ai else [])

        for consent_type in types:
            response = client.post(
                "/platform-consents",
                json={"consent_type": consent_type, "version": "1.0"},
            )
            assert response.status_code == 200, response.text

    def link_professional(self, sharing_mode: str = "NEW_ONLY") -> None:

        response = self.as_patient().post(
            "/therapy/link-requests",
            json={"professional_id": self.professional_id, "sharing_mode": sharing_mode},
        )
        assert response.status_code == 200, response.text

        request_id = response.json()["id"]

        response = self.as_professional().patch(
            f"/therapy/link-requests/{request_id}/accept"
        )
        assert response.status_code == 200, response.text

        response = self.as_patient().post(
            "/therapy/consents",
            json={"professional_id": self.professional_id},
        )
        assert response.status_code == 200, response.text

    def create_entry(self, text: str) -> int:

        response = self.as_patient().post(
            "/entries",
            json={"entry_type": "TEXT", "text_content": text},
        )
        assert response.status_code == 200, response.text

        return response.json()["id"]

    def manual_analysis(self, entry_id: int, **extra) -> dict:

        response = self.as_patient().post(
            f"/analysis/entries/{entry_id}",
            json={
                "primary_emotion": "Tristeza",
                "emotion_intensity": "HIGH",
                "analysis_json": {},
                **extra,
            },
        )
        assert response.status_code == 200, response.text

        return response.json()

    def close(self) -> None:
        app.dependency_overrides.clear()
        self.engine.dispose()


@pytest.fixture
def world(monkeypatch):

    clinical_world = ClinicalWorld(monkeypatch)

    yield clinical_world

    clinical_world.close()
