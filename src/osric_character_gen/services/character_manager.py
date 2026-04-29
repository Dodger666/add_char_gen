"""Character manager service — save/load/update/delete/version operations."""

import json
import uuid

from osric_character_gen.core.config import settings
from osric_character_gen.core.security import (
    generate_secret_key,
    hash_key,
    strip_html,
)
from osric_character_gen.models.character import CharacterSheet
from osric_character_gen.models.manager_requests import (
    SaveCharacterRequest,
    UpdateCharacterRequest,
)
from osric_character_gen.models.manager_responses import (
    CharacterDetailResponse,
    CharacterVersionResponse,
    CharacterVersionSummary,
    SaveCharacterResponse,
)
from osric_character_gen.persistence.character_repository import CharacterRepository


class CharacterNotFoundError(Exception):
    pass


class CharacterManagerService:
    def __init__(self, db_path: str | None = None) -> None:
        self._repo = CharacterRepository(db_path)

    def save_character(self, request: SaveCharacterRequest) -> SaveCharacterResponse:
        character_id = str(uuid.uuid4())
        secret_key = generate_secret_key(settings.secret_key_bytes)
        secret_key_hash = hash_key(secret_key)

        notes = strip_html(request.notes) if request.notes else None

        self._repo.insert(
            character_id=character_id,
            secret_key_hash=secret_key_hash,
            character_data=request.character.model_dump(mode="json"),
            name=request.character.name,
            character_class=request.character.character_class.value,
            ancestry=request.character.ancestry.value,
            level=request.character.level,
            campaign_id=request.campaign_id,
            notes=notes,
        )

        return SaveCharacterResponse(
            character_id=character_id,
            secret_key=secret_key,
        )

    def get_character(self, secret_key: str) -> CharacterDetailResponse:
        secret_key_hash = hash_key(secret_key)
        row = self._repo.find_by_secret_key_hash(secret_key_hash)
        if row is None:
            raise CharacterNotFoundError
        return self._row_to_detail(row)

    def update_character(self, secret_key: str, request: UpdateCharacterRequest) -> CharacterDetailResponse:
        secret_key_hash = hash_key(secret_key)

        # Fetch current state for version snapshot
        current_row = self._repo.find_by_secret_key_hash(secret_key_hash)
        if current_row is None:
            raise CharacterNotFoundError

        # Create version snapshot
        version_number = self._repo.get_max_version_number(current_row["id"]) + 1
        self._repo.insert_version(
            character_id=current_row["id"],
            version_number=version_number,
            character_data=json.loads(current_row["character_data"]),
            changed_by_hash=secret_key_hash,
        )

        # Prune old versions
        while self._repo.count_versions(current_row["id"]) > settings.max_versions_per_character:
            self._repo.delete_oldest_version(current_row["id"])

        notes = strip_html(request.notes) if request.notes else None

        updated_row = self._repo.update(
            secret_key_hash=secret_key_hash,
            character_data=request.character.model_dump(mode="json"),
            name=request.character.name,
            character_class=request.character.character_class.value,
            ancestry=request.character.ancestry.value,
            level=request.character.level,
            notes=notes,
        )

        if updated_row is None:
            raise CharacterNotFoundError

        return self._row_to_detail(updated_row)

    def archive_character(self, secret_key: str) -> bool:
        secret_key_hash = hash_key(secret_key)
        return self._repo.archive(secret_key_hash)

    def list_versions(self, secret_key: str) -> list[CharacterVersionSummary]:
        secret_key_hash = hash_key(secret_key)
        row = self._repo.find_by_secret_key_hash(secret_key_hash)
        if row is None:
            raise CharacterNotFoundError

        versions = self._repo.list_versions(row["id"])
        return [
            CharacterVersionSummary(
                version_number=v["version_number"],
                created_at=v["created_at"],
            )
            for v in versions
        ]

    def get_version(self, secret_key: str, version_number: int) -> CharacterVersionResponse:
        secret_key_hash = hash_key(secret_key)
        row = self._repo.find_by_secret_key_hash(secret_key_hash)
        if row is None:
            raise CharacterNotFoundError

        version = self._repo.get_version(row["id"], version_number)
        if version is None:
            raise CharacterNotFoundError

        return CharacterVersionResponse(
            version_number=version["version_number"],
            character_data=CharacterSheet.model_validate_json(version["character_data"]),
            created_at=version["created_at"],
        )

    def get_character_for_pdf(self, secret_key: str) -> CharacterSheet:
        secret_key_hash = hash_key(secret_key)
        row = self._repo.find_by_secret_key_hash(secret_key_hash)
        if row is None:
            raise CharacterNotFoundError
        return CharacterSheet.model_validate_json(row["character_data"])

    def join_campaign(self, secret_key: str, campaign_id: str) -> str | None:
        """Returns current campaign_id if already in a different campaign, else None."""
        secret_key_hash = hash_key(secret_key)
        current = self._repo.get_campaign_id(secret_key_hash)

        if current is not None and current != campaign_id:
            return current  # Conflict

        self._repo.set_campaign(secret_key_hash, campaign_id)
        return None

    def leave_campaign(self, secret_key: str) -> bool:
        secret_key_hash = hash_key(secret_key)
        return self._repo.set_campaign(secret_key_hash, None)

    @staticmethod
    def _row_to_detail(row) -> CharacterDetailResponse:
        return CharacterDetailResponse(
            character_id=row["id"],
            character=CharacterSheet.model_validate_json(row["character_data"]),
            notes=row["notes"],
            is_archived=bool(row["is_archived"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
