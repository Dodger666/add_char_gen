"""FastAPI campaign endpoints."""

from fastapi import APIRouter, HTTPException, Query

from osric_character_gen.models.manager_requests import (
    CreateCampaignRequest,
    UpdateCampaignRequest,
)
from osric_character_gen.models.manager_responses import (
    CampaignCharacterListResponse,
    CampaignDetailResponse,
    CharacterDetailResponse,
    CreateCampaignResponse,
    RotateKeyResponse,
)
from osric_character_gen.services.campaign_service import (
    CampaignNotFoundError,
    CampaignService,
)

router = APIRouter(prefix="/api/v1/campaigns", tags=["campaigns"])

_service = CampaignService()


@router.post("", response_model=CreateCampaignResponse, status_code=201)
async def create_campaign(request: CreateCampaignRequest) -> CreateCampaignResponse:
    """Create a new campaign, returns admin key."""
    return _service.create_campaign(request)


@router.get("/{admin_key}/characters", response_model=CampaignCharacterListResponse)
async def list_campaign_characters(
    admin_key: str,
    class_filter: str | None = Query(default=None),
    ancestry_filter: str | None = Query(default=None),
    level_min: int | None = Query(default=None, ge=1),
    level_max: int | None = Query(default=None, le=20),
    include_archived: bool = Query(default=False),
    sort_by: str = Query(default="name"),
    sort_order: str = Query(default="asc"),
) -> CampaignCharacterListResponse:
    """List all characters in a campaign."""
    try:
        return _service.list_characters(
            admin_key,
            class_filter=class_filter,
            ancestry_filter=ancestry_filter,
            level_min=level_min,
            level_max=level_max,
            include_archived=include_archived,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except CampaignNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found") from None


@router.get("/{admin_key}/characters/{character_id}", response_model=CharacterDetailResponse)
async def get_campaign_character(admin_key: str, character_id: str) -> CharacterDetailResponse:
    """View a single character in a campaign (read-only)."""
    try:
        return _service.get_character_in_campaign(admin_key, character_id)
    except CampaignNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found") from None


@router.put("/{admin_key}", response_model=CampaignDetailResponse)
async def update_campaign(admin_key: str, request: UpdateCampaignRequest) -> CampaignDetailResponse:
    """Update campaign metadata."""
    try:
        return _service.update_campaign(admin_key, request)
    except CampaignNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found") from None


@router.post("/{admin_key}/rotate-key", response_model=RotateKeyResponse)
async def rotate_admin_key(admin_key: str) -> RotateKeyResponse:
    """Rotate admin key. Old key becomes invalid."""
    try:
        return _service.rotate_key(admin_key)
    except CampaignNotFoundError:
        raise HTTPException(status_code=404, detail="Campaign not found") from None
