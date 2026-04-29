"""Tests for the character sheet manager front-end pages."""

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


# ---------------------------------------------------------------------------
# New Character Page: /character/new
# ---------------------------------------------------------------------------
class TestNewCharacterPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/character/new")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_contains_editable_form(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "<form" in html.lower() or 'id="character-form"' in html

    def test_contains_save_button(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "Save" in html

    def test_contains_generate_button(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "Generate Random" in html

    def test_contains_ability_score_inputs(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            assert ability in html.lower(), f"Missing ability input: {ability}"

    def test_contains_class_select(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "Fighter" in html
        assert "Cleric" in html
        assert "Magic-User" in html

    def test_contains_ancestry_select(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "Human" in html
        assert "Dwarf" in html
        assert "Elf" in html

    def test_contains_encumbrance_panel(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "encumbrance" in html.lower()
        assert "movement" in html.lower()

    def test_contains_encumbrance_calculator_js(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "calculateEncumbrance" in html

    def test_self_contained(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "<style>" in html or "<style" in html
        assert "<script>" in html or "<script" in html

    def test_references_save_api(self, client: TestClient) -> None:
        html = client.get("/character/new").text
        assert "/api/v1/characters/save" in html


# ---------------------------------------------------------------------------
# Edit Character Page: /character/{secret_key}/edit
# ---------------------------------------------------------------------------
class TestEditCharacterPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/character/some-key/edit")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_contains_editable_form(self, client: TestClient) -> None:
        html = client.get("/character/some-key/edit").text
        assert "<form" in html.lower() or 'id="character-form"' in html

    def test_embeds_secret_key(self, client: TestClient) -> None:
        html = client.get("/character/test-secret-key-abc/edit").text
        assert "test-secret-key-abc" in html

    def test_references_update_api(self, client: TestClient) -> None:
        html = client.get("/character/some-key/edit").text
        assert "/api/v1/characters/" in html


# ---------------------------------------------------------------------------
# View Character Page (read-only): /character/{secret_key}/view
# ---------------------------------------------------------------------------
class TestViewCharacterPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/character/some-key/view")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_embeds_secret_key(self, client: TestClient) -> None:
        html = client.get("/character/view-key-123/view").text
        assert "view-key-123" in html

    def test_is_read_only(self, client: TestClient) -> None:
        html = client.get("/character/some-key/view").text
        assert "readonly" in html.lower() or "disabled" in html.lower() or "read-only" in html.lower()


# ---------------------------------------------------------------------------
# Create Campaign Page: /campaign/new
# ---------------------------------------------------------------------------
class TestNewCampaignPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/campaign/new")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_contains_campaign_form(self, client: TestClient) -> None:
        html = client.get("/campaign/new").text
        assert "campaign" in html.lower()
        assert "name" in html.lower()

    def test_references_campaign_api(self, client: TestClient) -> None:
        html = client.get("/campaign/new").text
        assert "/api/v1/campaigns" in html


# ---------------------------------------------------------------------------
# Campaign Dashboard: /campaign/{admin_key}
# ---------------------------------------------------------------------------
class TestCampaignDashboardPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/campaign/some-admin-key")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_embeds_admin_key(self, client: TestClient) -> None:
        html = client.get("/campaign/admin-key-xyz/").text
        assert "admin-key-xyz" in html

    def test_references_campaign_characters_api(self, client: TestClient) -> None:
        html = client.get("/campaign/some-key").text
        assert "/api/v1/campaigns/" in html


# ---------------------------------------------------------------------------
# Campaign Character View: /campaign/{admin_key}/character/{character_id}
# ---------------------------------------------------------------------------
class TestCampaignCharacterViewPage:
    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/campaign/admin-key/character/char-id-123")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_embeds_keys(self, client: TestClient) -> None:
        html = client.get("/campaign/admin-key-test/character/char-id-test").text
        assert "admin-key-test" in html
        assert "char-id-test" in html

    def test_is_read_only(self, client: TestClient) -> None:
        html = client.get("/campaign/admin-key/character/char-id").text
        assert "read-only" in html.lower() or "readonly" in html.lower()
