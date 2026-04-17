"""FastAPI character generation endpoints."""

from fastapi import APIRouter, HTTPException, Query, Response

from osric_character_gen.models.responses import GenerateCharacterResponse
from osric_character_gen.services.character_generator import (
    CharacterGeneratorService,
    MaxRetriesExceededError,
)

router = APIRouter(prefix="/api/v1/characters", tags=["characters"])

_service = CharacterGeneratorService()


@router.get("/generate", response_model=GenerateCharacterResponse)
async def generate_character(
    seed: int | None = Query(default=None, description="Optional seed for deterministic generation"),
) -> GenerateCharacterResponse:
    """Generate a complete OSRIC 3.0 character as JSON."""
    try:
        sheet, metadata = _service.generate(seed=seed)
    except MaxRetriesExceededError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return GenerateCharacterResponse(
        character=sheet,
        generation_metadata=metadata,
    )


@router.get("/generate/pdf")
async def generate_character_pdf(
    seed: int | None = Query(default=None, description="Optional seed for deterministic generation"),
) -> Response:
    """Generate a complete OSRIC 3.0 character as downloadable PDF."""
    try:
        sheet, _metadata = _service.generate(seed=seed)
    except MaxRetriesExceededError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    try:
        from osric_character_gen.domain.pdf_sheet_generator import PDFSheetGenerator

        pdf_gen = PDFSheetGenerator()
        pdf_bytes = pdf_gen.generate(sheet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {e}") from e

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="osric_character_sheet.pdf"'},
    )
