"""FastAPI character manager endpoints — persistence CRUD."""

import re

from fastapi import APIRouter, HTTPException, Response

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
from osric_character_gen.services.character_manager import (
    CharacterManagerService,
    CharacterNotFoundError,
)

router = APIRouter(prefix="/api/v1/characters", tags=["character-manager"])

_service = CharacterManagerService()


@router.post("/save", response_model=SaveCharacterResponse, status_code=201)
async def save_character(request: SaveCharacterRequest) -> SaveCharacterResponse:
    """Save a new character, returning a unique secret key."""
    return _service.save_character(request)


@router.get("/{secret_key}", response_model=CharacterDetailResponse)
async def get_character(secret_key: str) -> CharacterDetailResponse:
    """Retrieve a character by its secret key."""
    try:
        return _service.get_character(secret_key)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None


@router.put("/{secret_key}", response_model=CharacterDetailResponse)
async def update_character(secret_key: str, request: UpdateCharacterRequest) -> CharacterDetailResponse:
    """Update a character by its secret key."""
    try:
        return _service.update_character(secret_key, request)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None


@router.delete("/{secret_key}")
async def archive_character(secret_key: str) -> dict:
    """Soft-delete (archive) a character."""
    if not _service.archive_character(secret_key):
        raise HTTPException(status_code=404, detail="Character not found") from None
    return {"detail": "Character archived"}


@router.get("/{secret_key}/versions", response_model=list[CharacterVersionSummary])
async def list_versions(secret_key: str) -> list[CharacterVersionSummary]:
    """List version history for a character."""
    try:
        return _service.list_versions(secret_key)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None


@router.get("/{secret_key}/versions/{version_number}", response_model=CharacterVersionResponse)
async def get_version(secret_key: str, version_number: int) -> CharacterVersionResponse:
    """Retrieve a specific version of a character."""
    try:
        return _service.get_version(secret_key, version_number)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None


@router.get("/{secret_key}/pdf")
async def export_character_pdf(secret_key: str) -> Response:
    """Export a saved character as PDF."""
    try:
        sheet = _service.get_character_for_pdf(secret_key)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None

    try:
        from osric_character_gen.domain.pdf_sheet_generator import PDFSheetGenerator

        pdf_gen = PDFSheetGenerator()
        pdf_bytes = pdf_gen.generate(sheet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {e}") from e

    safe_name = re.sub(r"[^\w\s-]", "", sheet.name).strip().replace(" ", "_")
    safe_class = sheet.character_class.value.replace("-", "_")
    filename = f"{safe_name}_Lvl{sheet.level}_{safe_class}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{secret_key}/json")
async def export_character_json(secret_key: str) -> Response:
    """Export a saved character as downloadable JSON."""
    try:
        detail = _service.get_character(secret_key)
    except CharacterNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found") from None

    json_bytes = detail.character.model_dump_json(indent=2).encode("utf-8")
    safe_name = re.sub(r"[^\w\s-]", "", detail.character.name).strip().replace(" ", "_")
    filename = f"{safe_name}.json"

    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{secret_key}/campaign/{campaign_id}")
async def join_campaign(secret_key: str, campaign_id: str) -> dict:
    """Associate a character with a campaign."""
    from osric_character_gen.services.campaign_service import CampaignService

    camp_svc = CampaignService()
    if not camp_svc.campaign_exists(campaign_id):
        raise HTTPException(status_code=404, detail="Campaign not found")

    conflict = _service.join_campaign(secret_key, campaign_id)
    if conflict is not None:
        raise HTTPException(status_code=409, detail="Character already belongs to a campaign")
    return {"detail": "Character joined campaign"}


@router.delete("/{secret_key}/campaign")
async def leave_campaign(secret_key: str) -> dict:
    """Remove a character from its campaign."""
    _service.leave_campaign(secret_key)
    return {"detail": "Character left campaign"}
