"""Pydantic request models for the character sheet manager."""

from pydantic import BaseModel, Field

from osric_character_gen.models.character import CharacterSheet


class SaveCharacterRequest(BaseModel):
    character: CharacterSheet
    campaign_id: str | None = Field(
        default=None,
        description="Optional campaign UUID to associate this character with",
    )
    notes: str | None = Field(
        default=None,
        max_length=10000,
        description="Optional character notes/journal",
    )


class UpdateCharacterRequest(BaseModel):
    character: CharacterSheet
    notes: str | None = Field(
        default=None,
        max_length=10000,
    )


class CreateCampaignRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class UpdateCampaignRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
