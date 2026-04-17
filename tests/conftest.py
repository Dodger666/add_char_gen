"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from osric_character_gen.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
