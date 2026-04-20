"""FastAPI application entry point."""

from fastapi import FastAPI

from osric_character_gen.api.v1.endpoints.characters import router as characters_router
from osric_character_gen.api.v1.endpoints.frontend import router as frontend_router

app = FastAPI(
    title="OSRIC 3.0 Character Generator",
    description="Generate complete OSRIC 3.0 player characters via REST API",
    version="0.1.0",
)

app.include_router(characters_router)
app.include_router(frontend_router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
