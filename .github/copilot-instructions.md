# GitHub Copilot Instructions

This document provides coding standards and best practices for this project. All code generation and modifications must adhere to these guidelines.

---

## 🐍 Python Version & Language Standards

- **Python Version**: Always use **Python 3.13** unless explicitly specified otherwise
- **Type Hints**: Use type hints for all function signatures, class attributes, and variables where appropriate
- **Naming Convention**: Use **snake_case** for all:
  - Function names
  - Variable names
  - Module names
  - Method names
  - File names
- **Class Names**: Use camelCase for class names
- **Constants**: Use UPPER_SNAKE_CASE for constants

---

## 🚀 Web Framework Standards

### FastAPI (Required)

- **NEVER use Flask** - Always use **FastAPI** for web applications and APIs
- FastAPI is the required framework for all web services and REST APIs
- Leverage FastAPI's automatic OpenAPI documentation
- Use Pydantic models for request/response validation
- Implement async endpoints with `async def` where appropriate
- Use dependency injection for shared resources (database connections, services, etc.)
- Organize routes with `APIRouter` for modular structure

**Example FastAPI Structure**:
```python
from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel

app = FastAPI(title="My API", version="1.0.0")
router = APIRouter(prefix="/api/v1")

class ItemRequest(BaseModel):
    name: str
    price: float

@router.post("/items")
async def create_item(item: ItemRequest) -> dict:
    return {"item_id": 1, "name": item.name}

app.include_router(router)
```

---

## 🧪 Test-Driven Development (TDD) Workflow

### Critical TDD Requirements

1. **Tests First, Always**: Generate tests BEFORE implementing business logic
2. **Never Remove Tests**: NEVER delete or comment out tests to make code pass
3. **Never Use Dummy Tests**: Tests must be real, meaningful, and validate actual behavior
4. **Stop When Tests Pass**: Implementation is complete when all tests pass

### TDD Workflow Steps

1. **Write the test** that defines the desired behavior
2. **Run the test** - it should fail (Red phase)
3. **Implement the minimum code** to make the test pass (Green phase)
4. **Refactor** while keeping tests green
5. **Repeat** for next feature

### Testing Standards

- Use **pytest** as the testing framework
- Test file naming: `test_*.py` or `*_test.py`
- Test function naming: `test_<feature_description>`
- Use fixtures for test setup and teardown
- Use parametrize for testing multiple scenarios
- Mock external dependencies (databases, APIs, etc.)
- Use `pytest-asyncio` for async tests with FastAPI

**Example Test Structure**:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item_success():
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_create_item_invalid_data():
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Item"}  # Missing price
    )
    assert response.status_code == 422
```

---

## 📊 Code Coverage Requirements

### Mandatory Coverage Standards

- **Code coverage is MANDATORY** for all business logic and technically relevant code
- Minimum coverage target: **80%** for business logic
- Measure both **line coverage** and **branch coverage**
- Generate coverage reports after every test run

### Coverage Implementation

- Use **coverage.py** with pytest
- Alternative: Use **pytest-cov** plugin for integrated coverage
- Exclude from coverage:
  - Test files themselves (optional, but recommended to include them)
  - Migration scripts
  - Configuration files
  - `__init__.py` files with only imports

### Coverage Commands

```bash
# Run tests with coverage
uv run coverage run -m pytest

# Generate coverage report
uv run coverage report -m

# Generate HTML coverage report
uv run coverage html

# Or use pytest-cov (alternative)
uv run pytest --cov=src --cov-report=html --cov-report=term
```

### Coverage Configuration

Add to `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

---

## 🔍 Code Quality & Linting (Ruff)

### Ruff Compliance (Required)

- **All code must be Ruff-compliant** before commit
- Ruff replaces: flake8, isort, Black, pyupgrade, and more
- Run Ruff linter and formatter on all code changes

### Ruff Configuration

Add to `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py313"
line-length = 88
indent-width = 4

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Ruff Commands

```bash
# Check code with Ruff
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

---

## 📦 Dependency & Package Management

### Use uv (Required)

- **Never use pip, poetry, or pipenv** - Always use **uv** for package management
- Use **pyproject.toml** for project configuration (not setup.py or requirements.txt)
- uv manages Python versions, dependencies, and virtual environments

### uv Workflow

```bash
# Initialize new project
uv init project-name

# Add dependencies
uv add fastapi uvicorn pydantic

# Add dev dependencies
uv add --dev pytest pytest-cov ruff coverage

# Sync environment with lockfile
uv sync

# Run commands in uv environment
uv run python main.py
uv run pytest
uv run ruff check .

# Install specific Python version
uv python install 3.13

# Pin Python version for project
uv python pin 3.13
```

### pyproject.toml Structure

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "coverage>=7.6.0",
    "ruff>=0.8.0",
    "httpx>=0.27.0",  # For FastAPI TestClient
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
# ... (see Ruff section above)

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
```

---

## 🐳 Docker Standards

### Docker-Friendly Development

- Projects must be **Docker-friendly** but **keep development runs local**
- Provide `Dockerfile` and `docker-compose.yml` for production deployments
- Use multi-stage builds for smaller production images
- Development should use local virtual environments via uv

### Dockerfile Example (FastAPI + uv)

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY ./src ./src

# Set environment to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml Example

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      - db
    volumes:
      - ./src:/app/src  # For hot reload in dev
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Local Development (Non-Docker)

```bash
# Use uv for local development
uv sync
uv run uvicorn src.main:app --reload
```

---

## 📁 Project Structure

### Recommended Project Layout

```
project-name/
├── .github/
│   ├── workflows/          # CI/CD workflows
│   └── copilot-instructions.md
├── src/
│   └── project_name/       # Main package (use snake_case)
│       ├── __init__.py
│       ├── main.py         # FastAPI app entry point
│       ├── api/            # API routes
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── endpoints/
│       ├── core/           # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── dependencies.py
│       ├── models/         # Pydantic models
│       │   └── __init__.py
│       └── services/       # Business logic
│           └── __init__.py
├── tests/                  # Test directory
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_api/
│   └── test_services/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml         # Project config (uv/ruff/pytest)
├── uv.lock                # Dependency lockfile
└── README.md
```

---

## ✅ Pre-Commit Checklist

Before committing code, ensure:

1. ✅ All tests pass: `uv run pytest`
2. ✅ Code coverage meets requirements: `uv run pytest --cov`
3. ✅ Ruff linting passes: `uv run ruff check .`
4. ✅ Code is formatted: `uv run ruff format .`
5. ✅ Type hints are present and correct
6. ✅ No tests were deleted or made dummy
7. ✅ New features have tests written FIRST

---

## 🚫 Forbidden Practices

### NEVER DO THESE:

1. ❌ **Never use Flask** - Use FastAPI instead
2. ❌ **Never remove or comment out tests** to make code pass
3. ❌ **Never create dummy/placeholder tests** that don't validate behavior
4. ❌ **Never use pip, poetry, or pipenv** - Use uv instead
5. ❌ **Never skip code coverage** for business logic
6. ❌ **Never commit code without running tests**
7. ❌ **Never use camelCase** for Python identifiers (except class names)
8. ❌ **Never implement before writing tests** (violates TDD)

---

## 🎯 Summary

| Requirement | Tool/Standard | Status |
|------------|---------------|---------|
| Python Version | 3.13 | Mandatory |
| Web Framework | FastAPI (never Flask) | Mandatory |
| Naming Convention | snake_case | Mandatory |
| Development Workflow | TDD (tests first) | Mandatory |
| Testing Framework | pytest | Mandatory |
| Code Coverage | coverage.py / pytest-cov | Mandatory (80%+) |
| Linting & Formatting | Ruff | Mandatory |
| Package Management | uv + pyproject.toml | Mandatory |
| Docker Support | Dockerfile + docker-compose.yml | Required |
| Local Development | uv (non-Docker) | Preferred |

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Last Updated**: 2025-12-16
