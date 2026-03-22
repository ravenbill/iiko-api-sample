from __future__ import annotations

import asyncio
from typing import Any

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


def test_check_balance_returns_balance_for_track_number() -> None:
    from iiko_api_sample.commands.check_balance import check_balance_by_track

    transport = RecordingTransport()
    transport.responses["/loyalty/iiko/customer/info"] = {
        "id": "guest-1",
        "walletBalances": [
            {"id": "wallet-1", "name": "Bonus", "type": 0, "balance": 120.5},
            {"id": "wallet-2", "name": "Gift", "type": 0, "balance": 15},
        ],
    }

    result = asyncio.run(
        check_balance_by_track(
            settings=build_settings(),
            organization_id="org-1",
            card_track="track-1",
            transport=transport,
            token_provider=fake_token_provider,
        )
    )

    assert result == {
        "status": "found",
        "guest_id": "guest-1",
        "card_track": "track-1",
        "wallet_balances": [
            {"id": "wallet-1", "name": "Bonus", "type": 0, "balance": 120.5},
            {"id": "wallet-2", "name": "Gift", "type": 0, "balance": 15},
        ],
    }
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


def test_check_balance_returns_not_found_for_unknown_track() -> None:
    from iiko_api_sample.commands.check_balance import check_balance_by_track

    transport = RecordingTransport()
    transport.errors["/loyalty/iiko/customer/info"] = IikoApiError(
        status_code=404,
        error_description="Guest not found",
    )

    result = asyncio.run(
        check_balance_by_track(
            settings=build_settings(),
            organization_id="org-1",
            card_track="track-2",
            transport=transport,
            token_provider=fake_token_provider,
        )
    )

    assert result == {
        "status": "not_found",
        "guest_id": "",
        "card_track": "track-2",
        "wallet_balances": [],
    }
