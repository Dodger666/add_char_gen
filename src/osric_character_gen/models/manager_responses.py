"""Pydantic response models for the character sheet manager."""

from datetime import datetime

from pydantic import BaseModel, Field

from osric_character_gen.models.character import CharacterSheet


class SaveCharacterResponse(BaseModel):
    character_id: str
    secret_key: str = Field(
        description="32-char URL-safe token. Store this — it cannot be recovered.",
    )
    message: str = "Character saved. Store your secret key — it cannot be recovered."


class CharacterDetailResponse(BaseModel):
    character_id: str
    character: CharacterSheet
    notes: str | None
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class CharacterSummary(BaseModel):
    character_id: str
    name: str
    character_class: str
    ancestry: str
    level: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class CampaignCharacterListResponse(BaseModel):
    campaign_name: str
    campaign_description: str | None
    characters: list[CharacterSummary]
    total: int


class CreateCampaignResponse(BaseModel):
    campaign_id: str
    admin_key: str = Field(
        description="48-char URL-safe token. Store this — it cannot be recovered.",
    )
    message: str = "Campaign created. Store your admin key — it cannot be recovered."


class CampaignDetailResponse(BaseModel):
    campaign_id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class RotateKeyResponse(BaseModel):
    new_admin_key: str
    message: str = "Admin key rotated. Old key is now invalid."


class CharacterVersionSummary(BaseModel):
    version_number: int
    created_at: datetime


class CharacterVersionResponse(BaseModel):
    version_number: int
    character_data: CharacterSheet
    created_at: datetime
