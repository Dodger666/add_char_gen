"""SQLite database initialization and connection management."""

import sqlite3
from pathlib import Path

_connection: sqlite3.Connection | None = None

_PRAGMAS = {
    "journal_mode": "wal",
    "foreign_keys": "on",
    "busy_timeout": "5000",
    "synchronous": "normal",
}

_CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS campaign (
    id TEXT PRIMARY KEY,
    admin_key_hash TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS character (
    id TEXT PRIMARY KEY,
    secret_key_hash TEXT NOT NULL UNIQUE,
    campaign_id TEXT REFERENCES campaign(id) ON DELETE SET NULL,
    character_data TEXT NOT NULL,
    name TEXT NOT NULL,
    character_class TEXT NOT NULL,
    ancestry TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    is_archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_accessed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS character_version (
    id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL REFERENCES character(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    character_data TEXT NOT NULL,
    changed_by_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(character_id, version_number)
);

CREATE INDEX IF NOT EXISTS idx_character_campaign ON character(campaign_id);
CREATE INDEX IF NOT EXISTS idx_character_class ON character(character_class);
CREATE INDEX IF NOT EXISTS idx_character_ancestry ON character(ancestry);
CREATE INDEX IF NOT EXISTS idx_character_level ON character(level);
CREATE INDEX IF NOT EXISTS idx_character_archived ON character(is_archived);
CREATE INDEX IF NOT EXISTS idx_character_version_char ON character_version(character_id);
"""


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    """Get or create the singleton database connection."""
    global _connection
    if _connection is not None:
        return _connection

    if db_path is None:
        from osric_character_gen.core.config import settings

        db_path = settings.db_path

    _connection = _create_connection(db_path)
    return _connection


def _create_connection(db_path: str) -> sqlite3.Connection:
    """Create a new SQLite connection with proper pragmas."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    for pragma, value in _PRAGMAS.items():
        conn.execute(f"PRAGMA {pragma} = {value}")
    return conn


def init_database(db_path: str | None = None) -> None:
    """Initialize the database: create tables if they don't exist."""
    conn = get_connection(db_path)
    conn.executescript(_CREATE_TABLES_SQL)
    conn.commit()


def close_database() -> None:
    """Close the singleton connection."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None


def reset_connection() -> None:
    """Reset the singleton connection (for testing)."""
    close_database()
