"""Tests for persistence.character_repository module."""

import json

import pytest

from osric_character_gen.persistence.character_repository import CharacterRepository
from osric_character_gen.persistence.database import init_database, reset_connection


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
def repo(db_path) -> CharacterRepository:
    return CharacterRepository(db_path)


SAMPLE_DATA = {"name": "Thorn", "character_class": "Fighter", "level": 1}


class TestInsertAndFind:
    def test_insert_and_find(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        row = repo.find_by_secret_key_hash("hash-abc")
        assert row is not None
        assert row["id"] == "char-1"
        assert row["name"] == "Thorn"
        assert json.loads(row["character_data"]) == SAMPLE_DATA

    def test_find_nonexistent_returns_none(self, repo: CharacterRepository) -> None:
        assert repo.find_by_secret_key_hash("nonexistent") is None

    def test_insert_with_campaign(self, repo: CharacterRepository, db_path: str) -> None:
        from osric_character_gen.persistence.campaign_repository import CampaignRepository

        camp_repo = CampaignRepository(db_path)
        camp_repo.insert("camp-1", "admin-hash", "Test Campaign")
        repo.insert(
            character_id="char-2",
            secret_key_hash="hash-def",
            character_data=SAMPLE_DATA,
            name="Elf",
            character_class="Magic-User",
            ancestry="Elf",
            level=3,
            campaign_id="camp-1",
        )
        row = repo.find_by_secret_key_hash("hash-def")
        assert row["campaign_id"] == "camp-1"


class TestUpdate:
    def test_update_character(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        updated_data = {**SAMPLE_DATA, "level": 5}
        row = repo.update(
            secret_key_hash="hash-abc",
            character_data=updated_data,
            name="Thorn the Brave",
            character_class="Fighter",
            ancestry="Human",
            level=5,
            notes="Level up!",
        )
        assert row is not None
        assert row["name"] == "Thorn the Brave"
        assert row["level"] == 5
        assert row["notes"] == "Level up!"

    def test_update_nonexistent_returns_none(self, repo: CharacterRepository) -> None:
        row = repo.update(
            secret_key_hash="nonexistent",
            character_data=SAMPLE_DATA,
            name="Nobody",
            character_class="Thief",
            ancestry="Human",
            level=1,
        )
        # Row fetched by hash won't exist
        assert row is None


class TestArchive:
    def test_archive_character(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        assert repo.archive("hash-abc") is True
        # Archived characters are not found
        assert repo.find_by_secret_key_hash("hash-abc") is None

    def test_archive_nonexistent_returns_false(self, repo: CharacterRepository) -> None:
        assert repo.archive("nonexistent") is False


class TestCampaignQueries:
    def test_find_by_campaign(self, repo: CharacterRepository, db_path: str) -> None:
        from osric_character_gen.persistence.campaign_repository import CampaignRepository

        camp_repo = CampaignRepository(db_path)
        camp_repo.insert("camp-1", "admin-hash", "Test Campaign")

        for i in range(3):
            repo.insert(
                character_id=f"char-{i}",
                secret_key_hash=f"hash-{i}",
                character_data=SAMPLE_DATA,
                name=f"Hero {i}",
                character_class="Fighter",
                ancestry="Human",
                level=i + 1,
                campaign_id="camp-1",
            )

        rows = repo.find_by_campaign("camp-1")
        assert len(rows) == 3

    def test_find_by_campaign_excludes_archived(self, repo: CharacterRepository, db_path: str) -> None:
        from osric_character_gen.persistence.campaign_repository import CampaignRepository

        camp_repo = CampaignRepository(db_path)
        camp_repo.insert("camp-1", "admin-hash", "Test Campaign")

        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-1",
            character_data=SAMPLE_DATA,
            name="Active",
            character_class="Fighter",
            ancestry="Human",
            level=1,
            campaign_id="camp-1",
        )
        repo.insert(
            character_id="char-2",
            secret_key_hash="hash-2",
            character_data=SAMPLE_DATA,
            name="Archived",
            character_class="Thief",
            ancestry="Elf",
            level=2,
            campaign_id="camp-1",
        )
        repo.archive("hash-2")

        rows = repo.find_by_campaign("camp-1")
        assert len(rows) == 1
        assert rows[0]["name"] == "Active"

    def test_find_by_campaign_with_filters(self, repo: CharacterRepository, db_path: str) -> None:
        from osric_character_gen.persistence.campaign_repository import CampaignRepository

        camp_repo = CampaignRepository(db_path)
        camp_repo.insert("camp-1", "admin-hash", "Test Campaign")

        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-1",
            character_data=SAMPLE_DATA,
            name="Fighter",
            character_class="Fighter",
            ancestry="Human",
            level=5,
            campaign_id="camp-1",
        )
        repo.insert(
            character_id="char-2",
            secret_key_hash="hash-2",
            character_data=SAMPLE_DATA,
            name="Wizard",
            character_class="Magic-User",
            ancestry="Elf",
            level=3,
            campaign_id="camp-1",
        )

        rows = repo.find_by_campaign("camp-1", class_filter="Fighter")
        assert len(rows) == 1
        assert rows[0]["name"] == "Fighter"

        rows = repo.find_by_campaign("camp-1", level_min=4)
        assert len(rows) == 1

    def test_set_and_leave_campaign(self, repo: CharacterRepository, db_path: str) -> None:
        from osric_character_gen.persistence.campaign_repository import CampaignRepository

        camp_repo = CampaignRepository(db_path)
        camp_repo.insert("camp-1", "admin-hash", "Test Campaign")

        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-1",
            character_data=SAMPLE_DATA,
            name="Wanderer",
            character_class="Ranger",
            ancestry="Human",
            level=1,
        )

        assert repo.set_campaign("hash-1", "camp-1") is True
        assert repo.get_campaign_id("hash-1") == "camp-1"

        assert repo.set_campaign("hash-1", None) is True
        assert repo.get_campaign_id("hash-1") is None


class TestVersionHistory:
    def test_insert_and_list_versions(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        repo.insert_version("char-1", 1, SAMPLE_DATA, "hash-abc")
        repo.insert_version("char-1", 2, {**SAMPLE_DATA, "level": 2}, "hash-abc")

        versions = repo.list_versions("char-1")
        assert len(versions) == 2
        assert versions[0]["version_number"] == 2  # DESC order

    def test_get_specific_version(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        repo.insert_version("char-1", 1, SAMPLE_DATA, "hash-abc")
        v = repo.get_version("char-1", 1)
        assert v is not None
        assert json.loads(v["character_data"]) == SAMPLE_DATA

    def test_get_nonexistent_version_returns_none(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        assert repo.get_version("char-1", 99) is None

    def test_delete_oldest_version(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        repo.insert_version("char-1", 1, SAMPLE_DATA, "hash-abc")
        repo.insert_version("char-1", 2, SAMPLE_DATA, "hash-abc")
        repo.insert_version("char-1", 3, SAMPLE_DATA, "hash-abc")

        assert repo.count_versions("char-1") == 3
        repo.delete_oldest_version("char-1")
        assert repo.count_versions("char-1") == 2
        assert repo.get_version("char-1", 1) is None  # oldest deleted

    def test_max_version_number(self, repo: CharacterRepository) -> None:
        repo.insert(
            character_id="char-1",
            secret_key_hash="hash-abc",
            character_data=SAMPLE_DATA,
            name="Thorn",
            character_class="Fighter",
            ancestry="Human",
            level=1,
        )
        assert repo.get_max_version_number("char-1") == 0
        repo.insert_version("char-1", 1, SAMPLE_DATA, "hash-abc")
        repo.insert_version("char-1", 2, SAMPLE_DATA, "hash-abc")
        assert repo.get_max_version_number("char-1") == 2
