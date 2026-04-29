"""Key generation and hashing for character sheet manager."""

import hashlib
import secrets


def generate_secret_key(num_bytes: int = 24) -> str:
    """Generate a URL-safe secret key for character access.

    24 bytes → 32 base64url characters.
    """
    return secrets.token_urlsafe(num_bytes)


def generate_admin_key(num_bytes: int = 36) -> str:
    """Generate a URL-safe admin key for campaign access.

    36 bytes → 48 base64url characters.
    """
    return secrets.token_urlsafe(num_bytes)


def hash_key(key: str) -> str:
    """Hash a key with SHA-256 for storage. Returns hex digest."""
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def strip_html(text: str) -> str:
    """Strip HTML tags from text for XSS prevention."""
    import re

    return re.sub(r"<[^>]+>", "", text)
