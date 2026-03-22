from __future__ import annotations

from dataclasses import dataclass
from os import environ, getenv
from typing import Mapping, Sequence

from .shared.accounts import get_known_client_slugs, slug_to_env_key

DEFAULT_BASE_URL = "https://api-ry.iiko.services/api/1"
DEFAULT_TIMEOUT_SECONDS = 10.0


@dataclass(frozen=True)
class IikoSettings:
    slug: str
    name: str
    base_url: str
    api_login: str
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls, client_slug: str | None = None) -> "IikoSettings":
        if client_slug is not None:
            return get_client_settings(client_slug)

        known_client_slugs = get_known_client_slugs(environ)
        if known_client_slugs:
            return get_client_settings(known_client_slugs[0])

        return cls(
            slug="default",
            name="Default",
            base_url=_get_base_url(environ),
            api_login=getenv("IIKO_API_LOGIN", ""),
            timeout_seconds=_get_timeout_seconds(environ),
        )


def get_client_settings(
    client_slug: str,
    env: Mapping[str, str] | None = None,
) -> IikoSettings:
    env = environ if env is None else env
    normalized_slug = client_slug.strip().lower()
    known_client_slugs = get_known_client_slugs(env)
    if normalized_slug not in known_client_slugs:
        raise ValueError(f"Unknown client: {client_slug}")

    env_key = slug_to_env_key(normalized_slug)
    name = env.get(f"IIKO_CLIENT_{env_key}_NAME", normalized_slug)
    api_login = env.get(f"IIKO_CLIENT_{env_key}_API_LOGIN", "")

    return IikoSettings(
        slug=normalized_slug,
        name=name,
        base_url=_get_base_url(env),
        api_login=api_login,
        timeout_seconds=_get_timeout_seconds(env),
    )


def get_client_settings_many(
    client_slugs: Sequence[str],
    env: Mapping[str, str] | None = None,
) -> list[IikoSettings]:
    env = environ if env is None else env
    return [get_client_settings(client_slug, env=env) for client_slug in client_slugs]


def _get_base_url(env: Mapping[str, str]) -> str:
    return env.get("IIKO_BASE_URL", DEFAULT_BASE_URL)


def _get_timeout_seconds(env: Mapping[str, str]) -> float:
    return float(env.get("IIKO_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))
