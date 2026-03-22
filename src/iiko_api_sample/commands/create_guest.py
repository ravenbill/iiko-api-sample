from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from ..config import IikoSettings
from ..shared.auth import get_access_token
from ..shared.customers import create_customer_with_card_track, get_customer_by_card_track
from ..shared.errors import IikoApiError
from ..shared.http import IikoTransport


async def create_guest(
    *,
    settings: IikoSettings,
    organization_id: str,
    card_track: str,
    card_number: str,
    name: str,
    transport: IikoTransport | Any,
    token_provider: Callable[[IikoSettings], Awaitable[str]] | None = None,
) -> dict[str, str]:
    token_provider = token_provider or get_access_token
    token = await token_provider(settings)

    try:
        customer = await get_customer_by_card_track(
            transport=transport,
            token=token,
            organization_id=organization_id,
            card_track=card_track,
        )
    except IikoApiError as error:
        if error.status_code != 404:
            raise
    else:
        return {
            "status": "existing",
            "guest_id": str(customer["id"]),
            "name": str(customer.get("name") or name),
        }

    created_customer = await create_customer_with_card_track(
        transport=transport,
        token=token,
        organization_id=organization_id,
        card_track=card_track,
        card_number=card_number,
        name=name,
    )
    return {
        "status": "created",
        "guest_id": str(created_customer["id"]),
        "name": name,
    }


def build_default_transport(settings: IikoSettings) -> IikoTransport:
    return IikoTransport(base_url=settings.base_url, timeout_seconds=settings.timeout_seconds)
