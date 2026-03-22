"""iiko API sample package."""

from .config import IikoSettings, get_client_settings, get_client_settings_many

__all__ = ["IikoApiClient", "IikoSettings", "get_client_settings", "get_client_settings_many"]


def __getattr__(name: str) -> object:
    if name == "IikoApiClient":
        from .client import IikoApiClient

        return IikoApiClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
