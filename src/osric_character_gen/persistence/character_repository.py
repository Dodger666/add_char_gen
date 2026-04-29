"""Character CRUD operations against SQLite."""

import json
import sqlite3
import uuid
from datetime import UTC, datetime

from osric_character_gen.persistence.database import get_connection


class CharacterRepository:
    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        return get_connection(self._db_path)

    def insert(
        self,
        character_id: str,
        secret_key_hash: str,
        character_data: dict,
        name: str,
        character_class: str,
        ancestry: str,
        level: int,
        campaign_id: str | None = None,
        notes: str | None = None,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        self._conn().execute(
            """INSERT INTO character
               (id, secret_key_hash, campaign_id, character_data, name,
                character_class, ancestry, level, notes, is_archived,
                created_at, updated_at, last_accessed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)""",
            (
                character_id,
                secret_key_hash,
                campaign_id,
                json.dumps(character_data),
                name,
                character_class,
                ancestry,
                level,
                notes,
                now,
                now,
                now,
            ),
        )
        self._conn().commit()

    def find_by_secret_key_hash(self, secret_key_hash: str) -> sqlite3.Row | None:
        row = (
            self._conn()
            .execute(
                "SELECT * FROM character WHERE secret_key_hash = ? AND is_archived = 0",
                (secret_key_hash,),
            )
            .fetchone()
        )
        if row:
            now = datetime.now(UTC).isoformat()
            self._conn().execute(
                "UPDATE character SET last_accessed_at = ? WHERE id = ?",
                (now, row["id"]),
            )
            self._conn().commit()
        return row

    def update(
        self,
        secret_key_hash: str,
        character_data: dict,
        name: str,
        character_class: str,
        ancestry: str,
        level: int,
        notes: str | None = None,
    ) -> sqlite3.Row | None:
        now = datetime.now(UTC).isoformat()
        self._conn().execute(
            """UPDATE character
               SET character_data = ?, name = ?, character_class = ?,
                   ancestry = ?, level = ?, notes = ?, updated_at = ?,
                   last_accessed_at = ?
               WHERE secret_key_hash = ? AND is_archived = 0""",
            (
                json.dumps(character_data),
                name,
                character_class,
                ancestry,
                level,
                notes,
                now,
                now,
                secret_key_hash,
            ),
        )
        self._conn().commit()
        return (
            self._conn()
            .execute(
                "SELECT * FROM character WHERE secret_key_hash = ?",
                (secret_key_hash,),
            )
            .fetchone()
        )

    def archive(self, secret_key_hash: str) -> bool:
        now = datetime.now(UTC).isoformat()
        cursor = self._conn().execute(
            "UPDATE character SET is_archived = 1, updated_at = ? WHERE secret_key_hash = ? AND is_archived = 0",
            (now, secret_key_hash),
        )
        self._conn().commit()
        return cursor.rowcount > 0

    def find_by_campaign(
        self,
        campaign_id: str,
        include_archived: bool = False,
        class_filter: str | None = None,
        ancestry_filter: str | None = None,
        level_min: int | None = None,
        level_max: int | None = None,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> list[sqlite3.Row]:
        query = "SELECT * FROM character WHERE campaign_id = ?"
        params: list = [campaign_id]

        if not include_archived:
            query += " AND is_archived = 0"
        if class_filter:
            query += " AND character_class = ?"
            params.append(class_filter)
        if ancestry_filter:
            query += " AND ancestry = ?"
            params.append(ancestry_filter)
        if level_min is not None:
            query += " AND level >= ?"
            params.append(level_min)
        if level_max is not None:
            query += " AND level <= ?"
            params.append(level_max)

        allowed_sort = {"name", "character_class", "level", "updated_at"}
        col = sort_by if sort_by in allowed_sort else "name"
        direction = "DESC" if sort_order.lower() == "desc" else "ASC"
        query += f" ORDER BY {col} {direction}"

        return self._conn().execute(query, params).fetchall()

    def find_by_id_and_campaign(self, character_id: str, campaign_id: str) -> sqlite3.Row | None:
        return (
            self._conn()
            .execute(
                "SELECT * FROM character WHERE id = ? AND campaign_id = ?",
                (character_id, campaign_id),
            )
            .fetchone()
        )

    def set_campaign(self, secret_key_hash: str, campaign_id: str | None) -> bool:
        cursor = self._conn().execute(
            "UPDATE character SET campaign_id = ?, updated_at = ? WHERE secret_key_hash = ? AND is_archived = 0",
            (campaign_id, datetime.now(UTC).isoformat(), secret_key_hash),
        )
        self._conn().commit()
        return cursor.rowcount > 0

    def get_campaign_id(self, secret_key_hash: str) -> str | None:
        row = (
            self._conn()
            .execute(
                "SELECT campaign_id FROM character WHERE secret_key_hash = ? AND is_archived = 0",
                (secret_key_hash,),
            )
            .fetchone()
        )
        return row["campaign_id"] if row else None

    # --- Version history ---

    def insert_version(
        self,
        character_id: str,
        version_number: int,
        character_data: dict,
        changed_by_hash: str,
    ) -> None:
        self._conn().execute(
            """INSERT INTO character_version
               (id, character_id, version_number, character_data, changed_by_hash)
               VALUES (?, ?, ?, ?, ?)""",
            (
                str(uuid.uuid4()),
                character_id,
                version_number,
                json.dumps(character_data),
                changed_by_hash,
            ),
        )
        self._conn().commit()

    def count_versions(self, character_id: str) -> int:
        row = (
            self._conn()
            .execute(
                "SELECT COUNT(*) as cnt FROM character_version WHERE character_id = ?",
                (character_id,),
            )
            .fetchone()
        )
        return row["cnt"]

    def delete_oldest_version(self, character_id: str) -> None:
        self._conn().execute(
            """DELETE FROM character_version
               WHERE id = (
                   SELECT id FROM character_version
                   WHERE character_id = ?
                   ORDER BY version_number ASC
                   LIMIT 1
               )""",
            (character_id,),
        )
        self._conn().commit()

    def get_max_version_number(self, character_id: str) -> int:
        row = (
            self._conn()
            .execute(
                "SELECT COALESCE(MAX(version_number), 0) as max_v FROM character_version WHERE character_id = ?",
                (character_id,),
            )
            .fetchone()
        )
        return row["max_v"]

    def list_versions(self, character_id: str) -> list[sqlite3.Row]:
        return (
            self._conn()
            .execute(
                "SELECT * FROM character_version WHERE character_id = ? ORDER BY version_number DESC",
                (character_id,),
            )
            .fetchall()
        )

    def get_version(self, character_id: str, version_number: int) -> sqlite3.Row | None:
        return (
            self._conn()
            .execute(
                "SELECT * FROM character_version WHERE character_id = ? AND version_number = ?",
                (character_id, version_number),
            )
            .fetchone()
        )
