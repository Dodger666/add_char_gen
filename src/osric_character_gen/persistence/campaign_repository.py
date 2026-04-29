"""Campaign CRUD operations against SQLite."""

import sqlite3
from datetime import UTC, datetime

from osric_character_gen.persistence.database import get_connection


class CampaignRepository:
    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        return get_connection(self._db_path)

    def insert(
        self,
        campaign_id: str,
        admin_key_hash: str,
        name: str,
        description: str | None = None,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        self._conn().execute(
            """INSERT INTO campaign (id, admin_key_hash, name, description, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (campaign_id, admin_key_hash, name, description, now, now),
        )
        self._conn().commit()

    def find_by_admin_key_hash(self, admin_key_hash: str) -> sqlite3.Row | None:
        return (
            self._conn()
            .execute(
                "SELECT * FROM campaign WHERE admin_key_hash = ?",
                (admin_key_hash,),
            )
            .fetchone()
        )

    def find_by_id(self, campaign_id: str) -> sqlite3.Row | None:
        return (
            self._conn()
            .execute(
                "SELECT * FROM campaign WHERE id = ?",
                (campaign_id,),
            )
            .fetchone()
        )

    def update(
        self,
        admin_key_hash: str,
        name: str,
        description: str | None = None,
    ) -> sqlite3.Row | None:
        now = datetime.now(UTC).isoformat()
        self._conn().execute(
            "UPDATE campaign SET name = ?, description = ?, updated_at = ? WHERE admin_key_hash = ?",
            (name, description, now, admin_key_hash),
        )
        self._conn().commit()
        return self.find_by_admin_key_hash(admin_key_hash)

    def rotate_key(self, old_admin_key_hash: str, new_admin_key_hash: str) -> bool:
        now = datetime.now(UTC).isoformat()
        cursor = self._conn().execute(
            "UPDATE campaign SET admin_key_hash = ?, updated_at = ? WHERE admin_key_hash = ?",
            (new_admin_key_hash, now, old_admin_key_hash),
        )
        self._conn().commit()
        return cursor.rowcount > 0
