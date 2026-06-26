from app.core.openai_settings import OpenAISettings
from app.services.openai_client_service import OpenAIClientService


def test_openai_settings_have_safe_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OPENAI_MAX_RETRIES", raising=False)

    settings = OpenAISettings(_env_file=None)  # type: ignore[call-arg]

    assert settings.api_key is None
    assert settings.model == "gpt-5.5"
    assert settings.timeout_seconds == 30.0
    assert settings.max_retries == 2


def test_openai_client_service_reports_configuration_status():
    service = OpenAIClientService()

    assert isinstance(service.is_configured(), bool)
    assert service.get_model() == "gpt-5.5"
