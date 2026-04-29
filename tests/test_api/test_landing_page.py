"""Tests for the landing page at /."""

from fastapi.testclient import TestClient


class TestLandingPage:
    """Tests for GET / — the application start/menu page."""

    def test_returns_html(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_contains_app_title(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "OSRIC" in html

    def test_links_to_new_character(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "/character/new" in html

    def test_links_to_generator(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "/generator" in html

    def test_links_to_new_campaign(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "/campaign/new" in html

    def test_has_secret_key_lookup_form(self, client: TestClient) -> None:
        html = client.get("/").text
        # Form to enter a secret key and load a saved character
        assert "secret_key" in html.lower() or "secret key" in html.lower()

    def test_has_admin_key_lookup_form(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "admin_key" in html.lower() or "admin key" in html.lower()

    def test_self_contained(self, client: TestClient) -> None:
        html = client.get("/").text
        assert "<style>" in html
        assert "<script>" in html or "/character/" in html  # links suffice
