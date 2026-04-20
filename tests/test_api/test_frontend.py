"""Tests for the front-end character sheet page."""

from fastapi.testclient import TestClient


class TestFrontendPage:
    """Tests for GET / — the HTML character sheet page."""

    def test_root_returns_html(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_page_contains_character_sheet_container(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        assert 'id="character-sheet"' in html

    def test_page_contains_download_pdf_button(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        assert 'id="download-pdf"' in html

    def test_page_contains_generate_button(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        assert 'id="generate-new"' in html

    def test_page_references_api_endpoint(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        assert "/api/v1/characters/generate" in html

    def test_page_contains_required_sections(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        required_sections = [
            "Character Information",
            "Ability Scores",
            "Saving Throws",
            "Combat",
            "Weapons",
            "Equipment",
        ]
        for section in required_sections:
            assert section in html, f"Missing section: {section}"

    def test_page_contains_osric_title(self, client: TestClient) -> None:
        response = client.get("/")
        html = response.text
        assert "OSRIC" in html

    def test_page_is_self_contained(self, client: TestClient) -> None:
        """Page should have inline CSS and JS — no external asset dependencies."""
        response = client.get("/")
        html = response.text
        assert "<style>" in html or '<style type="text/css">' in html
        assert "<script>" in html or '<script type="text/javascript">' in html
