"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from osric_character_gen.api.v1.endpoints.campaigns import router as campaigns_router
from osric_character_gen.api.v1.endpoints.character_manager import router as character_manager_router
from osric_character_gen.api.v1.endpoints.characters import router as characters_router
from osric_character_gen.api.v1.endpoints.frontend import router as frontend_router
from osric_character_gen.api.v1.endpoints.frontend_manager import router as frontend_manager_router
from osric_character_gen.persistence.database import close_database, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
    close_database()


app = FastAPI(
    title="OSRIC 3.0 Character Generator",
    description="Generate complete OSRIC 3.0 player characters via REST API",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(characters_router)
app.include_router(character_manager_router)
app.include_router(campaigns_router)
app.include_router(frontend_manager_router)
app.include_router(frontend_router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
