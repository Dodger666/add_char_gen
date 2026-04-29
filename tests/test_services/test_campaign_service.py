"""Tests for services.campaign_service module."""

import pytest

from osric_character_gen.models.character import (
    AbilityBonuses,
    AbilityScores,
    Alignment,
    AncestryName,
    CharacterSheet,
    ClassName,
    CoinPurse,
    Gender,
    PhysicalCharacteristics,
    SavingThrows,
)
from osric_character_gen.models.manager_requests import (
    CreateCampaignRequest,
    SaveCharacterRequest,
    UpdateCampaignRequest,
)
from osric_character_gen.persistence.database import init_database, reset_connection
from osric_character_gen.services.campaign_service import (
    CampaignNotFoundError,
    CampaignService,
)
from osric_character_gen.services.character_manager import CharacterManagerService


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
def camp_svc(db_path) -> CampaignService:
    return CampaignService(db_path)


@pytest.fixture
def char_svc(db_path) -> CharacterManagerService:
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


class TestCreateCampaign:
    def test_create_returns_admin_key(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(CreateCampaignRequest(name="Dragon Slayers"))
        assert len(resp.admin_key) == 48
        assert resp.campaign_id
        assert "cannot be recovered" in resp.message

    def test_create_with_description(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(
            CreateCampaignRequest(name="Dungeon Crawl", description="A classic dungeon crawl")
        )
        detail = camp_svc.get_campaign(resp.admin_key)
        assert detail.name == "Dungeon Crawl"
        assert detail.description == "A classic dungeon crawl"

    def test_html_stripped_from_name(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(CreateCampaignRequest(name="<b>Bold</b> Campaign"))
        detail = camp_svc.get_campaign(resp.admin_key)
        assert detail.name == "Bold Campaign"


class TestGetCampaign:
    def test_get_nonexistent_raises(self, camp_svc: CampaignService) -> None:
        with pytest.raises(CampaignNotFoundError):
            camp_svc.get_campaign("bad-key")


class TestUpdateCampaign:
    def test_update_name(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(CreateCampaignRequest(name="Old Name"))
        detail = camp_svc.update_campaign(resp.admin_key, UpdateCampaignRequest(name="New Name", description="Updated"))
        assert detail.name == "New Name"
        assert detail.description == "Updated"


class TestListCharacters:
    def test_list_characters_in_campaign(self, camp_svc: CampaignService, char_svc: CharacterManagerService) -> None:
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test Campaign"))

        for i in range(3):
            sheet = _make_sheet(name=f"Hero {i}")
            save_resp = char_svc.save_character(
                SaveCharacterRequest(character=sheet, campaign_id=camp_resp.campaign_id)
            )

        result = camp_svc.list_characters(camp_resp.admin_key)
        assert result.total == 3
        assert result.campaign_name == "Test Campaign"

    def test_list_with_filter(self, camp_svc: CampaignService, char_svc: CharacterManagerService) -> None:
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))

        char_svc.save_character(
            SaveCharacterRequest(
                character=_make_sheet(name="Fighter", character_class=ClassName.FIGHTER),
                campaign_id=camp_resp.campaign_id,
            )
        )
        char_svc.save_character(
            SaveCharacterRequest(
                character=_make_sheet(name="Thief", character_class=ClassName.THIEF),
                campaign_id=camp_resp.campaign_id,
            )
        )

        result = camp_svc.list_characters(camp_resp.admin_key, class_filter="Fighter")
        assert result.total == 1
        assert result.characters[0].name == "Fighter"

    def test_list_nonexistent_campaign_raises(self, camp_svc: CampaignService) -> None:
        with pytest.raises(CampaignNotFoundError):
            camp_svc.list_characters("bad-key")


class TestGetCharacterInCampaign:
    def test_get_character_in_campaign(self, camp_svc: CampaignService, char_svc: CharacterManagerService) -> None:
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))
        save_resp = char_svc.save_character(
            SaveCharacterRequest(
                character=_make_sheet(),
                campaign_id=camp_resp.campaign_id,
            )
        )

        detail = camp_svc.get_character_in_campaign(camp_resp.admin_key, save_resp.character_id)
        assert detail.character.name == "Thorn"

    def test_get_character_not_in_campaign_raises(
        self, camp_svc: CampaignService, char_svc: CharacterManagerService
    ) -> None:
        camp_resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))
        with pytest.raises(CampaignNotFoundError):
            camp_svc.get_character_in_campaign(camp_resp.admin_key, "nonexistent-id")


class TestRotateKey:
    def test_rotate_key(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))
        rotate_resp = camp_svc.rotate_key(resp.admin_key)
        assert len(rotate_resp.new_admin_key) == 48
        assert rotate_resp.new_admin_key != resp.admin_key

        # Old key no longer works
        with pytest.raises(CampaignNotFoundError):
            camp_svc.get_campaign(resp.admin_key)

        # New key works
        detail = camp_svc.get_campaign(rotate_resp.new_admin_key)
        assert detail.name == "Test"

    def test_rotate_nonexistent_raises(self, camp_svc: CampaignService) -> None:
        with pytest.raises(CampaignNotFoundError):
            camp_svc.rotate_key("bad-key")


class TestCampaignExists:
    def test_exists(self, camp_svc: CampaignService) -> None:
        resp = camp_svc.create_campaign(CreateCampaignRequest(name="Test"))
        assert camp_svc.campaign_exists(resp.campaign_id) is True

    def test_not_exists(self, camp_svc: CampaignService) -> None:
        assert camp_svc.campaign_exists("nonexistent") is False
