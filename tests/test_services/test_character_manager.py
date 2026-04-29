"""Tests for services.character_manager module."""

import json

import pytest

from osric_character_gen.models.character import (
    AbilityBonuses,
    AbilityScores,
    Alignment,
    AncestryName,
    ArmorItem,
    CharacterSheet,
    ClassName,
    CoinPurse,
    Gender,
    PhysicalCharacteristics,
    SavingThrows,
)
from osric_character_gen.models.manager_requests import (
    SaveCharacterRequest,
    UpdateCharacterRequest,
)
from osric_character_gen.persistence.database import init_database, reset_connection
from osric_character_gen.services.character_manager import (
    CharacterManagerService,
    CharacterNotFoundError,
)


@pytest.fixture(autouse=True)
def _reset_db():
    reset_connection()
    yield
    reset_connection()


@pytest.fixture
def db_path(tmp_path) -> str:
    path = str(tmp_path / "test.db")
    init_database(path)
    return path


@pytest.fixture
def svc(db_path) -> CharacterManagerService:
    return CharacterManagerService(db_path)


def _make_sheet(**overrides) -> CharacterSheet:
    defaults = {
        "name": "Thorn",
        "character_class": ClassName.FIGHTER,
        "level": 1,
        "alignment": Alignment.LG,
        "ancestry": AncestryName.HUMAN,
        "hit_points": 10,
        "armor_class_desc": 10,
        "armor_class_asc": 10,
        "physical": PhysicalCharacteristics(
            height_inches=70,
            height_display="5'10\"",
            weight_lbs=180,
            age=25,
            age_category="Adult",
            gender=Gender.MALE,
        ),
        "ability_scores": AbilityScores(
            strength=16,
            dexterity=12,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        ),
        "ability_bonuses": AbilityBonuses(str_encumbrance=70),
        "thac0": 20,
        "bthb": 0,
        "saving_throws": SavingThrows(
            aimed_magic_items=16,
            breath_weapons=17,
            death_paralysis_poison=14,
            petrifaction_polymorph=15,
            spells=17,
        ),
        "melee_to_hit_mod": 0,
        "missile_to_hit_mod": 0,
        "gold_remaining": 50.0,
        "coin_purse": CoinPurse(gold=50),
        "total_weight_lbs": 30.0,
        "encumbrance_allowance": 70,
        "encumbrance_status": "Unencumbered",
        "base_movement": 120,
        "effective_movement": 120,
    }
    defaults.update(overrides)
    return CharacterSheet(**defaults)


class TestSaveCharacter:
    def test_save_returns_secret_key(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        request = SaveCharacterRequest(character=sheet)
        response = svc.save_character(request)

        assert len(response.secret_key) == 32
        assert response.character_id
        assert "cannot be recovered" in response.message

    def test_saved_character_retrievable(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        request = SaveCharacterRequest(character=sheet, notes="Test note")
        save_resp = svc.save_character(request)

        detail = svc.get_character(save_resp.secret_key)
        assert detail.character.name == "Thorn"
        assert detail.notes == "Test note"
        assert detail.is_archived is False

    def test_save_with_campaign(self, svc: CharacterManagerService, db_path: str) -> None:
        from osric_character_gen.services.campaign_service import CampaignService
        from osric_character_gen.models.manager_requests import CreateCampaignRequest

        camp_svc = CampaignService(db_path)
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test Campaign"))

        sheet = _make_sheet()
        request = SaveCharacterRequest(character=sheet, campaign_id=camp_resp.campaign_id)
        save_resp = svc.save_character(request)

        detail = svc.get_character(save_resp.secret_key)
        assert detail.character_id == save_resp.character_id


class TestGetCharacter:
    def test_nonexistent_raises(self, svc: CharacterManagerService) -> None:
        with pytest.raises(CharacterNotFoundError):
            svc.get_character("nonexistent-key")


class TestUpdateCharacter:
    def test_update_changes_data(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        updated_sheet = _make_sheet(name="Thorn the Brave", level=5)
        update_req = UpdateCharacterRequest(character=updated_sheet, notes="Leveled up!")
        detail = svc.update_character(save_resp.secret_key, update_req)

        assert detail.character.name == "Thorn the Brave"
        assert detail.character.level == 5
        assert detail.notes == "Leveled up!"

    def test_update_creates_version(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        updated_sheet = _make_sheet(name="Thorn v2")
        svc.update_character(save_resp.secret_key, UpdateCharacterRequest(character=updated_sheet))

        versions = svc.list_versions(save_resp.secret_key)
        assert len(versions) == 1

    def test_update_nonexistent_raises(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        with pytest.raises(CharacterNotFoundError):
            svc.update_character("bad-key", UpdateCharacterRequest(character=sheet))

    def test_html_in_notes_stripped(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        updated_sheet = _make_sheet()
        update_req = UpdateCharacterRequest(character=updated_sheet, notes="<b>Bold</b> text")
        detail = svc.update_character(save_resp.secret_key, update_req)
        assert detail.notes == "Bold text"


class TestArchiveCharacter:
    def test_archive_and_not_found(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        assert svc.archive_character(save_resp.secret_key) is True

        with pytest.raises(CharacterNotFoundError):
            svc.get_character(save_resp.secret_key)

    def test_archive_nonexistent_returns_false(self, svc: CharacterManagerService) -> None:
        assert svc.archive_character("bad-key") is False


class TestVersionHistory:
    def test_multiple_updates_create_versions(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        for i in range(3):
            updated = _make_sheet(name=f"Thorn v{i + 2}")
            svc.update_character(save_resp.secret_key, UpdateCharacterRequest(character=updated))

        versions = svc.list_versions(save_resp.secret_key)
        assert len(versions) == 3

    def test_get_specific_version(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        updated = _make_sheet(name="Thorn v2")
        svc.update_character(save_resp.secret_key, UpdateCharacterRequest(character=updated))

        version = svc.get_version(save_resp.secret_key, 1)
        assert version.character_data.name == "Thorn"  # Original name in version

    def test_version_pruning(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        # Create 22 updates (> max 20 versions)
        for i in range(22):
            updated = _make_sheet(name=f"Thorn v{i + 2}")
            svc.update_character(save_resp.secret_key, UpdateCharacterRequest(character=updated))

        versions = svc.list_versions(save_resp.secret_key)
        assert len(versions) == 20


class TestCampaignMembership:
    def test_join_campaign(self, svc: CharacterManagerService, db_path: str) -> None:
        from osric_character_gen.services.campaign_service import CampaignService
        from osric_character_gen.models.manager_requests import CreateCampaignRequest

        camp_svc = CampaignService(db_path)
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))

        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))

        conflict = svc.join_campaign(save_resp.secret_key, camp_resp.campaign_id)
        assert conflict is None

    def test_join_different_campaign_returns_conflict(self, svc: CharacterManagerService, db_path: str) -> None:
        from osric_character_gen.services.campaign_service import CampaignService
        from osric_character_gen.models.manager_requests import CreateCampaignRequest

        camp_svc = CampaignService(db_path)
        camp1 = camp_svc.create_campaign(CreateCampaignRequest(name="Campaign 1"))
        camp2 = camp_svc.create_campaign(CreateCampaignRequest(name="Campaign 2"))

        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))
        svc.join_campaign(save_resp.secret_key, camp1.campaign_id)

        conflict = svc.join_campaign(save_resp.secret_key, camp2.campaign_id)
        assert conflict == camp1.campaign_id

    def test_leave_campaign(self, svc: CharacterManagerService, db_path: str) -> None:
        from osric_character_gen.services.campaign_service import CampaignService
        from osric_character_gen.models.manager_requests import CreateCampaignRequest

        camp_svc = CampaignService(db_path)
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))

        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))
        svc.join_campaign(save_resp.secret_key, camp_resp.campaign_id)

        assert svc.leave_campaign(save_resp.secret_key) is True


class TestPdfExport:
    def test_get_character_for_pdf(self, svc: CharacterManagerService) -> None:
        sheet = _make_sheet()
        save_resp = svc.save_character(SaveCharacterRequest(character=sheet))
        result = svc.get_character_for_pdf(save_resp.secret_key)
        assert isinstance(result, CharacterSheet)
        assert result.name == "Thorn"

    def test_pdf_nonexistent_raises(self, svc: CharacterManagerService) -> None:
        with pytest.raises(CharacterNotFoundError):
            svc.get_character_for_pdf("bad-key")
