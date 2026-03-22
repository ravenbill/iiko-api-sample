from __future__ import annotations

from typing import Mapping


def get_known_client_slugs(env: Mapping[str, str]) -> list[str]:
    raw_value = env.get("IIKO_CLIENTS", "")
    return [slug.strip().lower() for slug in raw_value.split(",") if slug.strip()]


def slug_to_env_key(slug: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in slug).upper()
