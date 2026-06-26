from app.core.openai_settings import OpenAISettings
from app.services.openai_client_service import OpenAIClientService


def test_openai_settings_have_safe_defaults():
    settings = OpenAISettings()

    assert settings.model == "gpt-5.5"
    assert settings.timeout_seconds == 1000.0
    assert settings.max_retries == 1000


def test_openai_client_service_reports_configuration_status():
    service = OpenAIClientService()

    assert isinstance(service.is_configured(), bool)
    assert service.get_model() == "gpt-5.5"
