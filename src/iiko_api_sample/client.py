from __future__ import annotations

from typing import Any

import httpx


class IikoApiClient:
    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def build_url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    async def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            response = await client.post(self.build_url(path), json=payload)
            response.raise_for_status()
            return response.json()
