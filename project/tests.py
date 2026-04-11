import pytest
from pydantic import ValidationError
from .config import Settings


class TestConfig:
    @pytest.fixture(autouse=True)
    def disable_env_file(self, monkeypatch):
        """Disable loading from .env file during tests to ensure test isolation."""

        monkeypatch.setitem(Settings.model_config, "env_file", None)

    def test_development_defaults(self):
        """Test that development defaults are set correctly."""

        config = Settings(PRODUCTION=False)
        assert config.is_debug is True
        assert config.DJANGO_SECRET_KEY == "insecure-secret"
        assert "*" in config.HOSTS

    def test_production_fail_fast_secret_key(self):
        """Test that missing or default secret key in production raises an error."""

        with pytest.raises(ValidationError) as excinfo:
            Settings(PRODUCTION=True, DJANGO_SECRET_KEY="insecure-secret")
        assert "DJANGO_SECRET_KEY must be set in production" in str(excinfo.value)

    def test_production_fail_fast_db_creds(self):
        """Test that missing database credentials in production raise an error."""

        with pytest.raises(ValidationError) as excinfo:
            Settings(PRODUCTION=True, PG_DB=None)

        assert "PG_DB must be set in production" in str(excinfo.value)

    def test_list_parsing_from_env_string(self):
        """Test that strings with commas are converted to actual lists."""

        config = Settings(CORS_ALLOWED="https://lucy.io, http://localhost:3000")
        assert isinstance(config.CORS_ALLOWED, list)
        assert len(config.CORS_ALLOWED) == 2
        assert "https://lucy.io" in config.CORS_ALLOWED

    def test_empty_env_string_to_empty_list(self):
        """Test that an empty environment string becomes an empty list and doesn't cause an error."""

        config = Settings(CSRF_TRUSTED="")
        assert config.CSRF_TRUSTED == []
