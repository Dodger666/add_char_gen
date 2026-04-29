"""Tests for core.security module."""

import re

from osric_character_gen.core.security import (
    generate_admin_key,
    generate_secret_key,
    hash_key,
    strip_html,
)


class TestGenerateSecretKey:
    def test_default_length_is_32_chars(self) -> None:
        key = generate_secret_key()
        assert len(key) == 32

    def test_url_safe_characters(self) -> None:
        key = generate_secret_key()
        assert re.fullmatch(r"[A-Za-z0-9_-]+", key)

    def test_uniqueness(self) -> None:
        keys = {generate_secret_key() for _ in range(100)}
        assert len(keys) == 100

    def test_custom_byte_length(self) -> None:
        key = generate_secret_key(num_bytes=12)
        assert len(key) == 16  # 12 bytes → 16 base64url chars


class TestGenerateAdminKey:
    def test_default_length_is_48_chars(self) -> None:
        key = generate_admin_key()
        assert len(key) == 48

    def test_url_safe_characters(self) -> None:
        key = generate_admin_key()
        assert re.fullmatch(r"[A-Za-z0-9_-]+", key)

    def test_uniqueness(self) -> None:
        keys = {generate_admin_key() for _ in range(100)}
        assert len(keys) == 100


class TestHashKey:
    def test_returns_64_char_hex(self) -> None:
        h = hash_key("test-key")
        assert len(h) == 64
        assert re.fullmatch(r"[0-9a-f]+", h)

    def test_deterministic(self) -> None:
        assert hash_key("same") == hash_key("same")

    def test_different_keys_different_hashes(self) -> None:
        assert hash_key("key-a") != hash_key("key-b")


class TestStripHtml:
    def test_strips_tags(self) -> None:
        assert strip_html("<b>bold</b>") == "bold"

    def test_strips_script(self) -> None:
        assert strip_html('<script>alert("xss")</script>') == 'alert("xss")'

    def test_plain_text_unchanged(self) -> None:
        assert strip_html("hello world") == "hello world"

    def test_empty_string(self) -> None:
        assert strip_html("") == ""
