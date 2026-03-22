from iiko_api_sample.config import IikoSettings


def test_default_base_url() -> None:
    settings = IikoSettings.from_env()
    assert settings.base_url == "https://api-ry.iiko.services/api/1"
