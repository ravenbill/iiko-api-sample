from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from ..config import IikoSettings
from ..shared.auth import get_access_token
from ..shared.customers import get_customer_by_card_track
from ..shared.errors import IikoApiError
from ..shared.http import IikoTransport


async def check_balance_by_track(
    *,
    settings: IikoSettings,
    organization_id: str,
    card_track: str,
    transport: IikoTransport | Any,
    token_provider: Callable[[IikoSettings], Awaitable[str]] | None = None,
) -> dict[str, Any]:
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
        return {
            "status": "not_found",
            "guest_id": "",
            "card_track": card_track,
            "wallet_balances": [],
        }

    wallet_balances = customer.get("walletBalances", [])
    if not isinstance(wallet_balances, list):
        wallet_balances = []

    return {
        "status": "found",
        "guest_id": str(customer["id"]),
        "card_track": card_track,
        "wallet_balances": wallet_balances,
    }


def build_default_transport(settings: IikoSettings) -> IikoTransport:
    return IikoTransport(base_url=settings.base_url, timeout_seconds=settings.timeout_seconds)
