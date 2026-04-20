"""Tests for character generation API endpoints."""

import pytest
from fastapi.testclient import TestClient

from osric_character_gen.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestGenerateEndpoint:
    def test_generate_success(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate?seed=42")
        assert response.status_code == 200
        data = response.json()
        assert "character" in data
        assert "generation_metadata" in data
        assert data["character"]["level"] == 1

    def test_generate_without_seed(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate")
        assert response.status_code == 200
        data = response.json()
        assert "character" in data

    def test_generate_deterministic(self, client: TestClient) -> None:
        r1 = client.get("/api/v1/characters/generate?seed=42")
        r2 = client.get("/api/v1/characters/generate?seed=42")
        assert r1.json()["character"] == r2.json()["character"]

    def test_generate_invalid_seed_type(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate?seed=not_a_number")
        assert response.status_code == 422

    def test_generate_response_schema(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate?seed=42")
        data = response.json()
        char = data["character"]
        assert "character_class" in char
        assert "ancestry" in char
        assert "ability_scores" in char
        assert "saving_throws" in char
        assert "hit_points" in char
        assert "armor_class_desc" in char
        assert "armor_class_asc" in char

    def test_generate_ability_scores_present(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate?seed=42")
        scores = response.json()["character"]["ability_scores"]
        for attr in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            assert attr in scores
            assert 1 <= scores[attr] <= 19

    def test_generate_str_minor_major_present(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate?seed=42")
        bonuses = response.json()["character"]["ability_bonuses"]
        assert "str_minor_test" in bonuses
        assert "str_major_test" in bonuses
        assert bonuses["str_minor_test"] != "—"
        assert bonuses["str_major_test"] != "—"


class TestHealthEndpoint:
    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestPDFEndpoint:
    def test_pdf_endpoint_returns_pdf(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate/pdf?seed=42")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert b"%PDF" in response.content[:10]

    def test_pdf_endpoint_content_disposition(self, client: TestClient) -> None:
        response = client.get("/api/v1/characters/generate/pdf?seed=42")
        assert "attachment" in response.headers.get("content-disposition", "")

    def test_pdf_filename_contains_character_details(self, client: TestClient) -> None:
        json_resp = client.get("/api/v1/characters/generate?seed=42")
        char = json_resp.json()["character"]
        pdf_resp = client.get("/api/v1/characters/generate/pdf?seed=42")
        disposition = pdf_resp.headers["content-disposition"]
        safe_class = char["character_class"].replace("-", "_")
        assert f"Lvl{char['level']}" in disposition
        assert safe_class in disposition
        assert disposition.endswith('.pdf"')
