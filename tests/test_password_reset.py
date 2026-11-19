import re

from datetime import datetime, timedelta

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import hash_password, verify_password
from app.main import app

from app.identity.models.password_reset_code import PasswordResetCode
from app.identity.models.user import User
from app.identity.routers import auth_router
from app.shared.email.email_sender import EmailSender


EMAIL = "paciente@test.com"
OLD_PASSWORD = "clave-antigua-123"
NEW_PASSWORD = "clave-nueva-456"


class ResetWorld:
    """
    Base en memoria con un usuario real (contraseña con
    hash y JWT de verdad) y los correos capturados.
    """

    def __init__(self, monkeypatch):

        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        db = self.Session()
        user = User(
            email=EMAIL,
            password_hash=hash_password(OLD_PASSWORD),
            role="PATIENT",
            is_active=True,
        )
        db.add(user)
        db.commit()
        self.user_id = user.id
        db.close()

        def override_db():
            session = self.Session()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_db] = override_db

        self.sent = []

        def fake_send(to, subject, body):
            self.sent.append({"to": to, "subject": subject, "body": body})
            return True

        monkeypatch.setattr(EmailSender, "send", staticmethod(fake_send))

        auth_router.forgot_password_limiter.reset()
        auth_router.reset_code_limiter.reset()

        self.client = TestClient(app)

    def login(self, password: str):
        return self.client.post(
            "/auth/login",
            data={"username": EMAIL, "password": password},
        )

    def forgot(self, email: str = EMAIL):
        return self.client.post("/auth/forgot-password", json={"email": email})

    def last_code(self) -> str:
        return re.search(r"\b(\d{6})\b", self.sent[-1]["body"]).group(1)

    def reset(self, code: str, password: str = NEW_PASSWORD, email: str = EMAIL):
        return self.client.post(
            "/auth/reset-password",
            json={"email": email, "code": code, "new_password": password},
        )

    def codes(self) -> list[PasswordResetCode]:
        db = self.Session()
        try:
            return db.query(PasswordResetCode).order_by(PasswordResetCode.id).all()
        finally:
            db.close()

    def close(self):
        app.dependency_overrides.clear()
        auth_router.forgot_password_limiter.reset()
        auth_router.reset_code_limiter.reset()
        self.engine.dispose()


@pytest.fixture
def world(monkeypatch):
    reset_world = ResetWorld(monkeypatch)
    yield reset_world
    reset_world.close()


def wrong(code: str) -> str:
    return f"{(int(code) + 1) % 1_000_000:06d}"


def test_full_flow_changes_password(world):

    response = world.forgot()

    assert response.status_code == 202
    assert len(world.sent) == 1
    assert world.sent[0]["to"] == EMAIL

    code = world.last_code()

    assert world.client.post(
        "/auth/verify-reset-code",
        json={"email": EMAIL, "code": code},
    ).json() == {"valid": True}

    response = world.reset(code)

    assert response.status_code == 200, response.text
    assert world.login(NEW_PASSWORD).status_code == 200
    assert world.login(OLD_PASSWORD).status_code == 401

    # Aviso de cambio de contraseña.
    assert world.sent[-1]["subject"] == "DEI: tu contraseña fue cambiada"


def test_response_does_not_reveal_if_email_exists(world):

    existing = world.forgot()
    missing = world.forgot("nadie@test.com")

    assert existing.status_code == missing.status_code == 202
    assert existing.json() == missing.json()
    assert len(world.sent) == 1


def test_inactive_user_gets_no_code(world):

    db = world.Session()
    db.get(User, world.user_id).is_active = False
    db.commit()
    db.close()

    assert world.forgot().status_code == 202
    assert world.sent == []


def test_code_is_stored_hashed(world):

    world.forgot()
    code = world.last_code()

    stored = world.codes()[0]

    assert code not in stored.code_hash
    assert len(stored.code_hash) == 64


def test_code_is_single_use(world):

    world.forgot()
    code = world.last_code()

    assert world.reset(code).status_code == 200

    response = world.reset(code, password="otra-clave-789")

    assert response.status_code == 400
    assert response.json()["detail"] == "Código inválido o expirado"


def test_expired_code_is_rejected(world):

    world.forgot()
    code = world.last_code()

    db = world.Session()
    stored = db.query(PasswordResetCode).one()
    stored.expires_at = datetime.utcnow() - timedelta(seconds=1)
    db.commit()
    db.close()

    assert world.reset(code).status_code == 400
    assert world.login(OLD_PASSWORD).status_code == 200


def test_new_code_invalidates_previous(world):

    world.forgot()
    first = world.last_code()

    world.forgot()
    second = world.last_code()

    if first != second:
        assert world.reset(first).status_code == 400

    assert world.reset(second).status_code == 200


def test_code_is_voided_after_max_failed_attempts(world):

    world.forgot()
    code = world.last_code()

    for _ in range(5):
        assert world.reset(wrong(code)).status_code == 400

    # Ni siquiera el código correcto sirve ya.
    assert world.reset(code).status_code == 400
    assert world.codes()[0].consumed_at is not None


def test_code_from_another_account_does_not_work(world):

    db = world.Session()
    db.add(User(email="otro@test.com", password_hash=hash_password("x" * 8), role="PATIENT"))
    db.commit()
    db.close()

    world.forgot("otro@test.com")
    code = world.last_code()

    assert world.reset(code, email=EMAIL).status_code == 400


def test_reset_closes_existing_sessions(world):

    token = world.login(OLD_PASSWORD).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    assert world.client.get("/auth/me", headers=headers).status_code == 200

    world.forgot()
    world.reset(world.last_code())

    assert world.client.get("/auth/me", headers=headers).status_code == 401

    new_token = world.login(NEW_PASSWORD).json()["access_token"]

    assert world.client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {new_token}"},
    ).status_code == 200


def test_weak_password_is_rejected(world):

    world.forgot()

    response = world.reset(world.last_code(), password="corta")

    assert response.status_code == 422

    db = world.Session()
    user = db.get(User, world.user_id)
    assert verify_password(OLD_PASSWORD, user.password_hash)
    db.close()


def test_codes_per_account_are_limited(world):

    for _ in range(4):
        assert world.forgot().status_code == 202

    # 3 por hora; la cuarta responde igual pero no envía.
    assert len(world.sent) == 3


def test_forgot_password_is_rate_limited_by_ip(world):

    for _ in range(5):
        assert world.forgot("nadie@test.com").status_code == 202

    response = world.forgot("nadie@test.com")

    assert response.status_code == 429
    assert int(response.headers["Retry-After"]) > 0


def test_reset_attempts_are_rate_limited_by_ip(world):

    for _ in range(10):
        world.reset("000000", email="nadie@test.com")

    assert world.reset("000000", email="nadie@test.com").status_code == 429


def test_malformed_code_is_rejected(world):

    assert world.reset("12ab56").status_code == 422
