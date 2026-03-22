from __future__ import annotations

from typing import Any, Protocol


class JsonTransport(Protocol):
    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]: ...


async def get_customer_by_card_track(
    *,
    transport: JsonTransport,
    token: str,
    organization_id: str,
    card_track: str,
) -> dict[str, Any]:
    return await transport.post_json(
        "/loyalty/iiko/customer/info",
        {
            "type": "cardTrack",
            "cardTrack": card_track,
            "organizationId": organization_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


async def create_customer_with_card_track(
    *,
    transport: JsonTransport,
    token: str,
    organization_id: str,
    card_track: str,
    card_number: str,
    name: str,
) -> dict[str, Any]:
    return await transport.post_json(
        "/loyalty/iiko/customer/create_or_update",
        {
            "cardTrack": card_track,
            "cardNumber": card_number,
            "name": name,
            "organizationId": organization_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
