"""Campaign service — create, list characters, rotate key."""

import uuid

from osric_character_gen.core.config import settings
from osric_character_gen.core.security import (
    generate_admin_key,
    hash_key,
    strip_html,
)
from osric_character_gen.models.character import CharacterSheet
from osric_character_gen.models.manager_requests import (
    CreateCampaignRequest,
    UpdateCampaignRequest,
)
from osric_character_gen.models.manager_responses import (
    CampaignCharacterListResponse,
    CampaignDetailResponse,
    CharacterDetailResponse,
    CharacterSummary,
    CreateCampaignResponse,
    RotateKeyResponse,
)
from osric_character_gen.persistence.campaign_repository import CampaignRepository
from osric_character_gen.persistence.character_repository import CharacterRepository


class CampaignNotFoundError(Exception):
    pass


class CampaignService:
    def __init__(self, db_path: str | None = None) -> None:
        self._campaign_repo = CampaignRepository(db_path)
        self._character_repo = CharacterRepository(db_path)

    def create_campaign(self, request: CreateCampaignRequest) -> CreateCampaignResponse:
        campaign_id = str(uuid.uuid4())
        admin_key = generate_admin_key(settings.admin_key_bytes)
        admin_key_hash = hash_key(admin_key)

        name = strip_html(request.name)
        description = strip_html(request.description) if request.description else None

        self._campaign_repo.insert(
            campaign_id=campaign_id,
            admin_key_hash=admin_key_hash,
            name=name,
            description=description,
        )

        return CreateCampaignResponse(
            campaign_id=campaign_id,
            admin_key=admin_key,
        )

    def get_campaign(self, admin_key: str) -> CampaignDetailResponse:
        admin_key_hash = hash_key(admin_key)
        row = self._campaign_repo.find_by_admin_key_hash(admin_key_hash)
        if row is None:
            raise CampaignNotFoundError
        return CampaignDetailResponse(
            campaign_id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def update_campaign(self, admin_key: str, request: UpdateCampaignRequest) -> CampaignDetailResponse:
        admin_key_hash = hash_key(admin_key)
        name = strip_html(request.name)
        description = strip_html(request.description) if request.description else None

        row = self._campaign_repo.update(admin_key_hash, name, description)
        if row is None:
            raise CampaignNotFoundError
        return CampaignDetailResponse(
            campaign_id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_characters(
        self,
        admin_key: str,
        class_filter: str | None = None,
        ancestry_filter: str | None = None,
        level_min: int | None = None,
        level_max: int | None = None,
        include_archived: bool = False,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> CampaignCharacterListResponse:
        admin_key_hash = hash_key(admin_key)
        campaign_row = self._campaign_repo.find_by_admin_key_hash(admin_key_hash)
        if campaign_row is None:
            raise CampaignNotFoundError

        rows = self._character_repo.find_by_campaign(
            campaign_id=campaign_row["id"],
            include_archived=include_archived,
            class_filter=class_filter,
            ancestry_filter=ancestry_filter,
            level_min=level_min,
            level_max=level_max,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        characters = [
            CharacterSummary(
                character_id=r["id"],
                name=r["name"],
                character_class=r["character_class"],
                ancestry=r["ancestry"],
                level=r["level"],
                is_archived=bool(r["is_archived"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"],
            )
            for r in rows
        ]

        return CampaignCharacterListResponse(
            campaign_name=campaign_row["name"],
            campaign_description=campaign_row["description"],
            characters=characters,
            total=len(characters),
        )

    def get_character_in_campaign(self, admin_key: str, character_id: str) -> CharacterDetailResponse:
        admin_key_hash = hash_key(admin_key)
        campaign_row = self._campaign_repo.find_by_admin_key_hash(admin_key_hash)
        if campaign_row is None:
            raise CampaignNotFoundError

        row = self._character_repo.find_by_id_and_campaign(character_id, campaign_row["id"])
        if row is None:
            raise CampaignNotFoundError

        return CharacterDetailResponse(
            character_id=row["id"],
            character=CharacterSheet.model_validate_json(row["character_data"]),
            notes=row["notes"],
            is_archived=bool(row["is_archived"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def rotate_key(self, admin_key: str) -> RotateKeyResponse:
        old_hash = hash_key(admin_key)
        new_key = generate_admin_key(settings.admin_key_bytes)
        new_hash = hash_key(new_key)

        if not self._campaign_repo.rotate_key(old_hash, new_hash):
            raise CampaignNotFoundError

        return RotateKeyResponse(new_admin_key=new_key)

    def campaign_exists(self, campaign_id: str) -> bool:
        return self._campaign_repo.find_by_id(campaign_id) is not None
