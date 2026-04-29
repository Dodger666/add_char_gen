"""Tests for character manager API endpoints."""

import pytest
from fastapi.testclient import TestClient

from osric_character_gen.main import app
from osric_character_gen.persistence.database import init_database, reset_connection


@pytest.fixture(autouse=True)
def _fresh_db(tmp_path):
    reset_connection()
    db_path = str(tmp_path / "test.db")
    init_database(db_path)
    yield
    reset_connection()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _minimal_character(**overrides) -> dict:
    base = {
        "name": "Thorn",
        "character_class": "Fighter",
        "level": 1,
        "alignment": "Lawful Good",
        "ancestry": "Human",
        "hit_points": 10,
        "armor_class_desc": 10,
        "armor_class_asc": 10,
        "physical": {
            "height_inches": 70,
            "height_display": "5'10\"",
            "weight_lbs": 180,
            "age": 25,
            "age_category": "Adult",
            "gender": "Male",
        },
        "ability_scores": {
            "strength": 16,
            "dexterity": 12,
            "constitution": 14,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        },
        "ability_bonuses": {"str_encumbrance": 70},
        "thac0": 20,
        "bthb": 0,
        "saving_throws": {
            "aimed_magic_items": 16,
            "breath_weapons": 17,
            "death_paralysis_poison": 14,
            "petrifaction_polymorph": 15,
            "spells": 17,
        },
        "melee_to_hit_mod": 0,
        "missile_to_hit_mod": 0,
        "gold_remaining": 50.0,
        "coin_purse": {"gold": 50},
        "total_weight_lbs": 30.0,
        "encumbrance_allowance": 70,
        "encumbrance_status": "Unencumbered",
        "base_movement": 120,
        "effective_movement": 120,
    }
    base.update(overrides)
    return base


class TestSaveEndpoint:
    def test_save_character(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["secret_key"]) == 32
        assert data["character_id"]

    def test_save_with_notes(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character(), "notes": "My first character"},
        )
        assert resp.status_code == 201

    def test_save_invalid_character(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/characters/save",
            json={"character": {"name": "Bad"}},  # Missing required fields
        )
        assert resp.status_code == 422


class TestGetEndpoint:
    def test_get_saved_character(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        get_resp = client.get(f"/api/v1/characters/{secret_key}")
        assert get_resp.status_code == 200
        assert get_resp.json()["character"]["name"] == "Thorn"

    def test_get_nonexistent_returns_404(self, client: TestClient) -> None:
        resp = client.get("/api/v1/characters/nonexistent-key-here-1234")
        assert resp.status_code == 404


class TestUpdateEndpoint:
    def test_update_character(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        update_resp = client.put(
            f"/api/v1/characters/{secret_key}",
            json={"character": _minimal_character(name="Thorn the Brave", level=5)},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["character"]["name"] == "Thorn the Brave"

    def test_update_nonexistent_returns_404(self, client: TestClient) -> None:
        resp = client.put(
            "/api/v1/characters/nonexistent-key-here-1234",
            json={"character": _minimal_character()},
        )
        assert resp.status_code == 404


class TestDeleteEndpoint:
    def test_archive_character(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        del_resp = client.delete(f"/api/v1/characters/{secret_key}")
        assert del_resp.status_code == 200
        assert del_resp.json()["detail"] == "Character archived"

        # Can no longer be found
        get_resp = client.get(f"/api/v1/characters/{secret_key}")
        assert get_resp.status_code == 404

    def test_archive_nonexistent_returns_404(self, client: TestClient) -> None:
        resp = client.delete("/api/v1/characters/nonexistent-key-here-1234")
        assert resp.status_code == 404


class TestVersionEndpoints:
    def test_list_versions_after_updates(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        # Make 2 updates
        for i in range(2):
            client.put(
                f"/api/v1/characters/{secret_key}",
                json={"character": _minimal_character(name=f"Thorn v{i + 2}")},
            )

        versions_resp = client.get(f"/api/v1/characters/{secret_key}/versions")
        assert versions_resp.status_code == 200
        assert len(versions_resp.json()) == 2

    def test_get_specific_version(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        client.put(
            f"/api/v1/characters/{secret_key}",
            json={"character": _minimal_character(name="Thorn v2")},
        )

        version_resp = client.get(f"/api/v1/characters/{secret_key}/versions/1")
        assert version_resp.status_code == 200
        assert version_resp.json()["character_data"]["name"] == "Thorn"


class TestJsonExport:
    def test_json_export(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        json_resp = client.get(f"/api/v1/characters/{secret_key}/json")
        assert json_resp.status_code == 200
        assert "attachment" in json_resp.headers.get("content-disposition", "")


class TestCampaignMembershipEndpoints:
    def test_join_and_leave_campaign(self, client: TestClient) -> None:
        # Create campaign
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test Campaign"},
        )
        assert camp_resp.status_code == 201
        campaign_id = camp_resp.json()["campaign_id"]

        # Save character
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        # Join
        join_resp = client.post(f"/api/v1/characters/{secret_key}/campaign/{campaign_id}")
        assert join_resp.status_code == 200

        # Leave
        leave_resp = client.delete(f"/api/v1/characters/{secret_key}/campaign")
        assert leave_resp.status_code == 200

    def test_join_nonexistent_campaign_returns_404(self, client: TestClient) -> None:
        save_resp = client.post(
            "/api/v1/characters/save",
            json={"character": _minimal_character()},
        )
        secret_key = save_resp.json()["secret_key"]

        resp = client.post(f"/api/v1/characters/{secret_key}/campaign/nonexistent-id")
        assert resp.status_code == 404
