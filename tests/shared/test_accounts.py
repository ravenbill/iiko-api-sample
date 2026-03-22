import pytest

from iiko_api_sample.config import IikoSettings, get_client_settings, get_client_settings_many


def test_get_client_settings_returns_named_client_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IIKO_BASE_URL", "https://api-ry.iiko.services/api/1")
    monkeypatch.setenv("IIKO_TIMEOUT_SECONDS", "12")
    monkeypatch.setenv("IIKO_CLIENTS", "client_one,client_two")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_ONE_NAME", "Client One")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_ONE_API_LOGIN", "login-one")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_TWO_NAME", "Client Two")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_TWO_API_LOGIN", "login-two")

    settings = get_client_settings("client_one")

    assert settings == IikoSettings(
        slug="client_one",
        name="Client One",
        base_url="https://api-ry.iiko.services/api/1",
        api_login="login-one",
        timeout_seconds=12.0,
    )


def test_get_client_settings_many_rejects_unknown_client_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IIKO_CLIENTS", "client_one")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_ONE_NAME", "Client One")
    monkeypatch.setenv("IIKO_CLIENT_CLIENT_ONE_API_LOGIN", "login-one")

    with pytest.raises(ValueError, match="Unknown client"):
        get_client_settings_many(["client_one", "missing"])
