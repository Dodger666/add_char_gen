from pydantic import BaseModel, Field


class GenerateCharacterRequest(BaseModel):
    seed: int | None = Field(
        default=None,
        description="Optional seed for deterministic generation. If omitted, a random seed is used.",
    )
