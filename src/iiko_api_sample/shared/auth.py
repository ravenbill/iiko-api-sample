from __future__ import annotations

from ..config import IikoSettings
from .http import IikoTransport


async def get_access_token(
    settings: IikoSettings,
    *,
    transport: IikoTransport | None = None,
) -> str:
    transport = transport or IikoTransport(
        base_url=settings.base_url,
        timeout_seconds=settings.timeout_seconds,
    )
    response = await transport.post_json("/access_token", {"apiLogin": settings.api_login})
    return str(response["token"])
