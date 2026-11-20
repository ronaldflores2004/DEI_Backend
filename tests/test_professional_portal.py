import time

from app.identity.models.professional_profile import ProfessionalProfile
from app.identity.models.user import User

from tests.clinical_fixtures import world  # noqa: F401


def test_profile_me(world):

    response = world.as_professional().get("/professionals/profile/me")

    assert response.status_code == 200
    assert response.json()["id"] == world.professional_id

    assert world.as_patient().get("/professionals/profile/me").status_code == 403


def test_profile_me_404_without_profile(world):

    db = world.Session()
    user = User(email="nuevo@test.com", password_hash="x", role="PROFESSIONAL")
    db.add(user)
    db.commit()
    world._current_user_id = user.id
    db.close()

    assert world.client.get("/professionals/profile/me").status_code == 404


def test_directory_lists_only_verified(world):

    db = world.Session()
    user = User(email="pendiente@test.com", password_hash="x", role="PROFESSIONAL")
    db.add(user)
    db.commit()
    db.add(ProfessionalProfile(
        user_id=user.id, first_name="Eva", last_name="Sol",
        license_number="9", specialties="EMDR", is_verified=False,
    ))
    db.commit()
    db.close()

    directory = world.as_patient().get("/professionals/directory").json()

    assert directory == [{
        "id": world.professional_id,
        "first_name": "Luis",
        "last_name": "Ruiz",
        "specialties": "TCC",
    }]


def test_link_request_shows_patient_name_and_can_be_rejected(world):

    response = world.as_patient().post(
        "/therapy/link-requests",
        json={"professional_id": world.professional_id, "sharing_mode": "NEW_ONLY"},
    )
    assert response.status_code == 200, response.text

    professional = world.as_professional()
    pending = professional.get("/therapy/link-requests/pending").json()

    assert pending[0]["patient_first_name"] == "Ana"
    assert pending[0]["patient_last_name"] == "Paz"

    request_id = pending[0]["id"]

    assert professional.patch(f"/therapy/link-requests/{request_id}/reject").status_code == 200
    assert professional.get("/therapy/link-requests/pending").json() == []
    assert professional.patch(f"/therapy/link-requests/{request_id}/reject").status_code == 400
    assert professional.get("/professionals/me/patients").json() == []


def test_reject_requires_owner(world):

    response = world.as_patient().post(
        "/therapy/link-requests",
        json={"professional_id": world.professional_id, "sharing_mode": "NEW_ONLY"},
    )
    request_id = response.json()["id"]

    assert world.as_patient().patch(f"/therapy/link-requests/{request_id}/reject").status_code == 403


def test_my_patients_and_entries_respect_sharing_and_audit(world):

    world.accept_consents()
    old_entry = world.create_entry("Entrada antigua")

    time.sleep(0.01)
    world.link_professional("NEW_ONLY")
    time.sleep(0.01)

    new_entry = world.create_entry("Entrada nueva")
    world.manual_analysis(new_entry)

    professional = world.as_professional()
    patients = professional.get("/professionals/me/patients").json()

    assert len(patients) == 1
    assert patients[0]["patient_id"] == world.patient_id
    assert patients[0]["first_name"] == "Ana"
    assert patients[0]["sharing_mode"] == "NEW_ONLY"

    response = professional.get(f"/professionals/me/patients/{world.patient_id}/entries")
    assert response.status_code == 200, response.text

    entries = response.json()

    assert [entry["id"] for entry in entries] == [new_entry]
    assert entries[0]["text_content"] == "Entrada nueva"
    assert entries[0]["primary_emotion"] == "Tristeza"
    assert old_entry not in [entry["id"] for entry in entries]

    log = world.as_patient().get("/audit/my-access-log").json()

    assert "VIEW_ENTRIES" in {item["action"] for item in log}


def test_entries_full_history(world):

    world.accept_consents()
    old_entry = world.create_entry("Entrada antigua")
    time.sleep(0.01)
    world.link_professional("FULL_HISTORY")

    entries = world.as_professional().get(
        f"/professionals/me/patients/{world.patient_id}/entries"
    ).json()

    assert [entry["id"] for entry in entries] == [old_entry]
    assert entries[0]["risk_level"] is None


def test_entries_forbidden_without_relation_or_consent(world):

    professional = world.as_professional()

    assert professional.get(
        f"/professionals/me/patients/{world.patient_id}/entries"
    ).status_code == 403

    world.accept_consents()
    world.link_professional()

    consents = world.as_patient().get("/therapy/consents").json()
    consent_id = consents[0]["id"]
    revoke = world.as_patient().patch(f"/therapy/consents/{consent_id}/revoke")
    assert revoke.status_code == 200, revoke.text

    assert world.as_professional().get(
        f"/professionals/me/patients/{world.patient_id}/entries"
    ).status_code == 403
