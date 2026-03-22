"""iiko API sample package."""

from .config import IikoSettings

__all__ = ["IikoApiClient", "IikoSettings"]


def __getattr__(name: str) -> object:
    if name == "IikoApiClient":
        from .client import IikoApiClient

        return IikoApiClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
