"""Tests for persistence.database module."""

import sqlite3

import pytest

from osric_character_gen.persistence.database import (
    close_database,
    get_connection,
    init_database,
    reset_connection,
)


@pytest.fixture(autouse=True)
def _reset_db():
    """Reset singleton connection before and after each test."""
    reset_connection()
    yield
    reset_connection()


class TestInitDatabase:
    def test_creates_tables(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        conn = get_connection(db_path)

        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
        table_names = {row["name"] for row in tables}
        assert "campaign" in table_names
        assert "character" in table_names
        assert "character_version" in table_names
        assert "schema_version" in table_names

    def test_idempotent(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        init_database(db_path)  # Should not raise

    def test_wal_mode_enabled(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        conn = get_connection(db_path)
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal"

    def test_foreign_keys_enabled(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        conn = get_connection(db_path)
        fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        assert fk == 1


class TestConnectionManagement:
    def test_get_connection_returns_same_instance(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        c1 = get_connection(db_path)
        c2 = get_connection(db_path)
        assert c1 is c2

    def test_close_and_reopen(self, tmp_path) -> None:
        db_path = str(tmp_path / "test.db")
        init_database(db_path)
        close_database()
        reset_connection()
        conn = get_connection(db_path)
        assert conn is not None

    def test_creates_parent_directory(self, tmp_path) -> None:
        db_path = str(tmp_path / "subdir" / "nested" / "test.db")
        init_database(db_path)
        conn = get_connection(db_path)
        assert conn is not None
