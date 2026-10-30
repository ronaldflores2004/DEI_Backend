from app.shared.ai.provider_chain import AIProviderChain

from tests.clinical_fixtures import world  # noqa: F401


def test_admin_manages_crisis_lines_shown_to_patient(world):

    admin = world.as_admin()

    created = admin.post(
        "/admin/crisis-lines",
        json={
            "country_code": "bo",
            "city": "Santa Cruz",
            "name": "Ambulancia",
            "phone": "161",
        },
    )

    assert created.status_code == 200, created.text
    assert created.json()["country_code"] == "BO"

    world.accept_consents()
    entry_id = world.create_entry("Tengo ganas de morir")
    support = world.manual_analysis(entry_id)["crisis_support"]

    assert support["lines"] == [
        {"name": "Ambulancia (Santa Cruz)", "phone": "161"}
    ]

    line_id = created.json()["id"]
    response = world.as_admin().patch(
        f"/admin/crisis-lines/{line_id}",
        json={"is_active": False},
    )

    assert response.json()["is_active"] is False


def test_without_managed_lines_the_fixed_list_is_used(world):

    world.accept_consents()
    entry_id = world.create_entry("No quiero vivir")
    support = world.manual_analysis(entry_id)["crisis_support"]

    assert any(line["phone"] == "800 11 30 40" for line in support["lines"])


def test_only_admin_manages_settings(world):

    assert world.as_patient().get("/admin/ai-settings").status_code == 403
    assert world.as_professional().get("/admin/crisis-lines").status_code == 403


def test_admin_chooses_ai_provider_chain(world):

    admin = world.as_admin()

    assert admin.get("/admin/ai-settings").json()["source"] == "env"

    updated = admin.put(
        "/admin/ai-settings",
        json={"provider_chain": ["gemini", "ollama"]},
    ).json()

    assert updated == {
        "provider_chain": ["GEMINI", "OLLAMA"],
        "source": "admin",
        "supported_providers": ["OLLAMA", "GEMINI", "FAKE"],
    }

    used = []

    def fake_provider(name):
        used.append(name)
        return name

    AIProviderChain.run(
        task="prueba",
        get_provider=fake_provider,
        call=lambda provider: "ok",
    )

    # Se usa la cadena del admin, no la del .env.
    assert used == ["GEMINI"]

    assert admin.delete("/admin/ai-settings").json()["source"] == "env"


def test_invalid_ai_chain_is_rejected(world):

    admin = world.as_admin()

    assert admin.put("/admin/ai-settings", json={"provider_chain": ["CHATGPT"]}).status_code == 400
    assert admin.put("/admin/ai-settings", json={"provider_chain": ["OLLAMA", "OLLAMA"]}).status_code == 400


def test_fake_provider_rejected_in_production(world, monkeypatch):

    from app.core.config import settings

    monkeypatch.setattr(settings, "APP_ENV", "production")

    response = world.as_admin().put(
        "/admin/ai-settings",
        json={"provider_chain": ["OLLAMA", "FAKE"]},
    )

    assert response.status_code == 400
