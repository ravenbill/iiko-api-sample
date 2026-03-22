from __future__ import annotations

from typing import Any

import httpx

from .errors import IikoApiError


class IikoTransport:
    def __init__(
        self,
        *,
        base_url: str,
        timeout_seconds: float = 10.0,
        http_transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._http_transport = http_transport

    def build_url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(
            timeout=self._timeout_seconds,
            transport=self._http_transport,
        ) as client:
            response = await client.post(self.build_url(path), json=payload, headers=headers)

        response_payload = _read_response_payload(response)
        if response.is_error:
            raise IikoApiError(
                status_code=response.status_code,
                correlation_id=_get_optional_string(response_payload, "correlationId"),
                error=_get_optional_string(response_payload, "error"),
                error_description=_get_optional_string(response_payload, "errorDescription"),
                error_field=_get_optional_string(response_payload, "errorField"),
            )

        return response_payload


def _read_response_payload(response: httpx.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def _get_optional_string(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return value if isinstance(value, str) else None
