from __future__ import annotations

import asyncio

import httpx
import pytest

from iiko_api_sample.config import IikoSettings


class RecordingTransport:
    def __init__(self, response: dict[str, str]) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, str], dict[str, str] | None]] = []

    async def post_json(
        self,
        path: str,
        payload: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> dict[str, str]:
        self.calls.append((path, payload, headers))
        return self.response


def test_get_access_token_posts_api_login() -> None:
    from iiko_api_sample.shared.auth import get_access_token

    settings = IikoSettings(
        slug="client_one",
        name="Client One",
        base_url="https://api-ru.iiko.services",
        api_login="login-one",
        timeout_seconds=10.0,
    )
    transport = RecordingTransport(
        response={
            "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
            "token": "token-123",
        }
    )

    token = asyncio.run(get_access_token(settings, transport=transport))

    assert token == "token-123"
    assert transport.calls == [
        (
            "/access_token",
            {"apiLogin": "login-one"},
            None,
        )
    ]


def test_iiko_transport_maps_iiko_error_response() -> None:
    from iiko_api_sample.shared.errors import IikoApiError
    from iiko_api_sample.shared.http import IikoTransport

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/access_token"
        return httpx.Response(
            401,
            json={
                "correlationId": "48fb4cd3-2ef6-4479-bea1-7c92721b988c",
                "errorDescription": "Authentication failed",
                "error": "Unauthorized",
            },
        )

    transport = IikoTransport(
        base_url="https://api-ru.iiko.services",
        timeout_seconds=10.0,
        http_transport=httpx.MockTransport(handler),
    )

    with pytest.raises(IikoApiError) as exc_info:
        asyncio.run(transport.post_json("/access_token", {"apiLogin": "bad-login"}))

    assert exc_info.value.status_code == 401
    assert exc_info.value.correlation_id == "48fb4cd3-2ef6-4479-bea1-7c92721b988c"
    assert exc_info.value.error_description == "Authentication failed"
