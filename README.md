# OSRIC 3.0 Character Generator

A FastAPI-based REST API that automatically generates complete OSRIC 3.0 (Old School Reference & Index Compilation) player characters following the rules from the Player Guide.

## Features

- Generates complete level-1 characters with all stats, equipment, and spells
- Supports all 10 classes: Assassin, Cleric, Druid, Fighter, Illusionist, Magic-User, Monk, Paladin, Ranger, Thief
- Supports all 7 ancestries: Dwarf, Elf, Gnome, Half-Elf, Half-Orc, Halfling, Human
- Deterministic generation via optional seed parameter
- PDF character sheet generation (fillable A4 format)
- JSON API with full character data
- Health check endpoint

## Tech Stack

- **Python 3.13** with type hints
- **FastAPI** + Uvicorn
- **Pydantic v2** for data validation
- **fpdf2** for PDF generation
- **pytest** with 187 tests, 91% coverage
- **Ruff** for linting and formatting
- **uv** for package management
- **Docker** for deployment

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Install dependencies
uv sync --all-extras

# Run the server
uv run uvicorn osric_character_gen.main:app --reload
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/characters/generate` | Generate character (JSON) |
| GET | `/api/v1/characters/generate/pdf` | Generate character (PDF download) |
| GET | `/health` | Health check |

### Generate a Character

```bash
# Random character (or open in browser)
curl http://localhost:8000/api/v1/characters/generate

# Deterministic character (same seed = same character)
curl http://localhost:8000/api/v1/characters/generate?seed=42

# PDF character sheet
curl http://localhost:8000/api/v1/characters/generate/pdf?seed=42 --output character.pdf
```

You can also open these URLs directly in your browser:
- http://localhost:8000/api/v1/characters/generate
- http://localhost:8000/api/v1/characters/generate?seed=42
- http://localhost:8000/api/v1/characters/generate/pdf?seed=42

## Development

### Run Tests

```bash
uv run pytest -v

# With coverage
uv run pytest --cov=src --cov-report=term-missing
```

### Lint & Format

```bash
uv run ruff check .
uv run ruff format .
```

### Docker

```bash
# Build and run
docker compose up --build

# Or build manually
docker build -t osric-character-gen .
docker run -p 8000:8000 osric-character-gen
```

## Project Structure

```
src/osric_character_gen/
├── main.py                  # FastAPI app entry point
├── api/v1/endpoints/        # API routes
├── models/                  # Pydantic models
├── data/                    # Static OSRIC game tables
├── domain/                  # Business logic modules
│   ├── dice.py              # Seeded RNG
│   ├── class_selector.py    # Class eligibility & selection
│   ├── ancestry_selector.py # Ancestry selection & adjustments
│   ├── stats_calculator.py  # Derived stats (AC, saves, THAC0, etc.)
│   ├── equipment_purchaser.py # Gold-based equipment purchasing
│   ├── spell_selector.py    # Spell selection for casters
│   ├── physical_generator.py # Height, weight, age
│   └── pdf_sheet_generator.py # PDF character sheet
└── services/
    └── character_generator.py # Orchestration service
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
