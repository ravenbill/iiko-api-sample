from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import pytest

from iiko_api_sample.config import IikoSettings
from iiko_api_sample.shared.errors import IikoApiError


class RecordingTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any], dict[str, str] | None]] = []
        self.responses: dict[str, Any] = {}
        self.errors: dict[str, Exception] = {}

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        self.calls.append((path, payload, headers))
        if path in self.errors:
            raise self.errors[path]
        response = self.responses[path]
        if isinstance(response, dict):
            return response
        raise AssertionError(f"Unexpected response for {path!r}")


async def fake_token_provider(_settings: IikoSettings) -> str:
    return "token-123"


def build_settings() -> IikoSettings:
    return IikoSettings(
        slug="client_one",
        name="Client One",
        base_url="https://api-ru.iiko.services",
        api_login="login-one",
        timeout_seconds=10.0,
    )


def test_create_guest_returns_existing_guest_when_match_found() -> None:
    from iiko_api_sample.commands.create_guest import create_guest

    transport = RecordingTransport()
    transport.responses["/loyalty/iiko/customer/info"] = {
        "id": "guest-1",
        "name": "Alice",
        "cards": [{"track": "track-1", "number": "card-1"}],
        "walletBalances": [],
    }

    result = asyncio.run(
        create_guest(
            settings=build_settings(),
            organization_id="org-1",
            card_track="track-1",
            card_number="card-1",
            name="Alice",
            transport=transport,
            token_provider=fake_token_provider,
        )
    )

    assert result == {"status": "existing", "guest_id": "guest-1", "name": "Alice"}
    assert transport.calls == [
        (
            "/loyalty/iiko/customer/info",
            {
                "type": "cardTrack",
                "cardTrack": "track-1",
                "organizationId": "org-1",
            },
            {"Authorization": "Bearer token-123"},
        )
    ]


def test_create_guest_creates_guest_when_no_match_exists() -> None:
    from iiko_api_sample.commands.create_guest import create_guest

    transport = RecordingTransport()
    transport.errors["/loyalty/iiko/customer/info"] = IikoApiError(
        status_code=404,
        error_description="Guest not found",
    )
    transport.responses["/loyalty/iiko/customer/create_or_update"] = {"id": "guest-2"}

    result = asyncio.run(
        create_guest(
            settings=build_settings(),
            organization_id="org-1",
            card_track="track-2",
            card_number="card-2",
            name="Bob",
            transport=transport,
            token_provider=fake_token_provider,
        )
    )

    assert result == {"status": "created", "guest_id": "guest-2", "name": "Bob"}
    assert transport.calls == [
        (
            "/loyalty/iiko/customer/info",
            {
                "type": "cardTrack",
                "cardTrack": "track-2",
                "organizationId": "org-1",
            },
            {"Authorization": "Bearer token-123"},
        ),
        (
            "/loyalty/iiko/customer/create_or_update",
            {
                "cardTrack": "track-2",
                "cardNumber": "card-2",
                "name": "Bob",
                "organizationId": "org-1",
            },
            {"Authorization": "Bearer token-123"},
        ),
    ]
