"""Tests for persistence.campaign_repository module."""

import pytest

from osric_character_gen.persistence.campaign_repository import CampaignRepository
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
def repo(db_path) -> CampaignRepository:
    return CampaignRepository(db_path)


class TestInsertAndFind:
    def test_insert_and_find_by_admin_key_hash(self, repo: CampaignRepository) -> None:
        repo.insert("camp-1", "admin-hash-abc", "Dragon Campaign", "A grand adventure")
        row = repo.find_by_admin_key_hash("admin-hash-abc")
        assert row is not None
        assert row["id"] == "camp-1"
        assert row["name"] == "Dragon Campaign"
        assert row["description"] == "A grand adventure"

    def test_find_nonexistent_returns_none(self, repo: CampaignRepository) -> None:
        assert repo.find_by_admin_key_hash("nonexistent") is None

    def test_find_by_id(self, repo: CampaignRepository) -> None:
        repo.insert("camp-1", "admin-hash-abc", "Test Campaign")
        row = repo.find_by_id("camp-1")
        assert row is not None
        assert row["name"] == "Test Campaign"


class TestUpdate:
    def test_update_campaign(self, repo: CampaignRepository) -> None:
        repo.insert("camp-1", "admin-hash-abc", "Old Name")
        row = repo.update("admin-hash-abc", "New Name", "New description")
        assert row is not None
        assert row["name"] == "New Name"
        assert row["description"] == "New description"


class TestRotateKey:
    def test_rotate_key(self, repo: CampaignRepository) -> None:
        repo.insert("camp-1", "old-hash", "Test Campaign")
        assert repo.rotate_key("old-hash", "new-hash") is True
        assert repo.find_by_admin_key_hash("old-hash") is None
        assert repo.find_by_admin_key_hash("new-hash") is not None

    def test_rotate_nonexistent_returns_false(self, repo: CampaignRepository) -> None:
        assert repo.rotate_key("nonexistent", "new-hash") is False
