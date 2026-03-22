from __future__ import annotations

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class IikoSettings:
    base_url: str
    api_login: str
    timeout_seconds: float = 10.0

    @classmethod
    def from_env(cls) -> "IikoSettings":
        return cls(
            base_url=getenv("IIKO_BASE_URL", "https://api-ry.iiko.services/api/1"),
            api_login=getenv("IIKO_API_LOGIN", ""),
            timeout_seconds=float(getenv("IIKO_TIMEOUT_SECONDS", "10")),
        )
