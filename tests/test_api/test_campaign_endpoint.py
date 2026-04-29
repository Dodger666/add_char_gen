"""Tests for campaign API endpoints."""

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


class TestCreateCampaign:
    def test_create_campaign(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Dragon Slayers", "description": "A grand adventure"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["admin_key"]) == 48
        assert data["campaign_id"]

    def test_create_campaign_without_description(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Simple Campaign"},
        )
        assert resp.status_code == 201

    def test_create_campaign_empty_name_returns_422(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/campaigns",
            json={"name": ""},
        )
        assert resp.status_code == 422


class TestListCampaignCharacters:
    def test_list_characters(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test Campaign"},
        )
        admin_key = camp_resp.json()["admin_key"]
        campaign_id = camp_resp.json()["campaign_id"]

        # Add characters
        for i in range(3):
            client.post(
                "/api/v1/characters/save",
                json={
                    "character": _minimal_character(name=f"Hero {i}"),
                    "campaign_id": campaign_id,
                },
            )

        list_resp = client.get(f"/api/v1/campaigns/{admin_key}/characters")
        assert list_resp.status_code == 200
        data = list_resp.json()
        assert data["total"] == 3
        assert data["campaign_name"] == "Test Campaign"

    def test_list_nonexistent_campaign_returns_404(self, client: TestClient) -> None:
        resp = client.get("/api/v1/campaigns/nonexistent-key-12345678/characters")
        assert resp.status_code == 404

    def test_list_with_filters(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test"},
        )
        admin_key = camp_resp.json()["admin_key"]
        campaign_id = camp_resp.json()["campaign_id"]

        client.post(
            "/api/v1/characters/save",
            json={
                "character": _minimal_character(name="Fighter", character_class="Fighter", level=5),
                "campaign_id": campaign_id,
            },
        )
        client.post(
            "/api/v1/characters/save",
            json={
                "character": _minimal_character(name="Thief", character_class="Thief", level=3),
                "campaign_id": campaign_id,
            },
        )

        resp = client.get(
            f"/api/v1/campaigns/{admin_key}/characters",
            params={"class_filter": "Fighter"},
        )
        assert resp.json()["total"] == 1


class TestGetCampaignCharacter:
    def test_get_character_in_campaign(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test"},
        )
        admin_key = camp_resp.json()["admin_key"]
        campaign_id = camp_resp.json()["campaign_id"]

        save_resp = client.post(
            "/api/v1/characters/save",
            json={
                "character": _minimal_character(),
                "campaign_id": campaign_id,
            },
        )
        character_id = save_resp.json()["character_id"]

        resp = client.get(f"/api/v1/campaigns/{admin_key}/characters/{character_id}")
        assert resp.status_code == 200
        assert resp.json()["character"]["name"] == "Thorn"

    def test_get_nonexistent_character_returns_404(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test"},
        )
        admin_key = camp_resp.json()["admin_key"]

        resp = client.get(f"/api/v1/campaigns/{admin_key}/characters/nonexistent")
        assert resp.status_code == 404


class TestUpdateCampaign:
    def test_update_campaign(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Old Name"},
        )
        admin_key = camp_resp.json()["admin_key"]

        resp = client.put(
            f"/api/v1/campaigns/{admin_key}",
            json={"name": "New Name", "description": "Updated desc"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    def test_update_nonexistent_returns_404(self, client: TestClient) -> None:
        resp = client.put(
            "/api/v1/campaigns/nonexistent-key-12345678",
            json={"name": "Whatever"},
        )
        assert resp.status_code == 404


class TestRotateKey:
    def test_rotate_key(self, client: TestClient) -> None:
        camp_resp = client.post(
            "/api/v1/campaigns",
            json={"name": "Test"},
        )
        admin_key = camp_resp.json()["admin_key"]

        rotate_resp = client.post(f"/api/v1/campaigns/{admin_key}/rotate-key")
        assert rotate_resp.status_code == 200
        new_key = rotate_resp.json()["new_admin_key"]
        assert len(new_key) == 48
        assert new_key != admin_key

        # Old key no longer works
        old_resp = client.get(f"/api/v1/campaigns/{admin_key}/characters")
        assert old_resp.status_code == 404

        # New key works
        new_resp = client.get(f"/api/v1/campaigns/{new_key}/characters")
        assert new_resp.status_code == 200

    def test_rotate_nonexistent_returns_404(self, client: TestClient) -> None:
        resp = client.post("/api/v1/campaigns/nonexistent-key-12345678/rotate-key")
        assert resp.status_code == 404
