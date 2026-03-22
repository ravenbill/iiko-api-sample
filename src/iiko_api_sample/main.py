from __future__ import annotations

from dotenv import load_dotenv

from .config import IikoSettings


def main() -> None:
    load_dotenv()
    settings = IikoSettings.from_env()
    print(f"iiko base URL: {settings.base_url}")
    if not settings.api_login:
        print("IIKO_API_LOGIN is not set yet.")
