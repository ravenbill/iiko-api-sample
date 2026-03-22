from __future__ import annotations

from typing import Any

from .shared.http import IikoTransport


class IikoApiClient:
    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        self._transport = IikoTransport(base_url=base_url, timeout_seconds=timeout_seconds)

    def build_url(self, path: str) -> str:
        return self._transport.build_url(path)

    async def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._transport.post_json(path, payload)
