from pydantic import BaseModel, Field

from osric_character_gen.models.character import CharacterSheet


class GenerateCharacterResponse(BaseModel):
    character: CharacterSheet
    generation_metadata: dict = Field(
        default_factory=dict,
        description="Metadata about the generation process",
    )
    pdf_base64: str | None = None
