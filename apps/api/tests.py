import pytest
from unittest.mock import patch, MagicMock

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import (
    Guild,
    Language,
)
from .gossiper import event_name, redis_payload


@pytest.fixture
def sample_guilds(db):
    en, _ = Language.objects.get_or_create(code="en", defaults={"name": "English"})
    es, _ = Language.objects.get_or_create(code="es", defaults={"name": "Spanish"})
    return [
        Guild.objects.create(id=123456789, lang=en),
        Guild.objects.create(id=987654321, lang=en),
        Guild.objects.create(id=555555555, lang=es),
    ]


@pytest.mark.django_db
class TestEventsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = "/api/events/"

        self.patch_redis_client = patch("apps.api.views.redis_client")
        self.mock_redis = self.patch_redis_client.start()

    def teardown_method(self):
        self.patch_redis_client.stop()

    def test_events_endpoint_headers(self):
        """Test that the events endpoint returns the correct headers for SSE."""

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "text/event-stream"
        assert response["Cache-Control"] == "no-cache"
        assert response["X-Accel-Buffering"] == "no"

    def test_events_stream_initial_message(self):
        """Test that the events stream yields the initial connection message."""

        mock_pubsub = MagicMock()
        self.mock_redis.pubsub.return_value = mock_pubsub
        mock_pubsub.listen.return_value = []

        response = self.client.get(self.url)

        content = b"".join(response.streaming_content).decode()
        assert "status" in content
        assert "connected" in content


@pytest.mark.django_db
class TestGuildAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = "/api/guilds/"
        self.user = User.objects.create_user(username="testuser", password="password")

        self.patch_redis_client = patch("apps.api.views.redis_client")
        self.patch_publish = patch("apps.api.views.publish_on_redis")

        self.mock_redis = self.patch_redis_client.start()
        self.mock_publish = self.patch_publish.start()

    def teardown_method(self):
        self.patch_redis_client.stop()
        self.patch_publish.stop()

    def test_list_guilds(self, sample_guilds):
        """Test that the API returns a list of guilds."""

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(sample_guilds)

    def test_get_guild(self, sample_guilds):
        """Test that the API returns a single guild by ID."""

        guild = sample_guilds[0]
        response = self.client.get(f"{self.url}{guild.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(guild.id)
        assert response.data["lang"]["code"] == guild.lang.code
        assert response.data["joined_at"] == guild.joined_at.isoformat().replace("+00:00", "Z")

    def test_get_nonexistent_guild(self):
        """Test that the API returns a 404 for a non-existent guild."""

        response = self.client.get(f"{self.url}999999999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_guild(self):
        """Test that the API can create a new guild."""

        Language.objects.get_or_create(code="en", defaults={"name": "English"})
        self.client.force_authenticate(user=self.user)

        data = {
            "id": "111111111",
            "lang": "en",
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] == data["id"]
        assert response.data["lang"]["code"] == "en"

    def test_create_guild_without_authentication(self):
        """Test that the API requires authentication to create a guild."""

        response = self.client.post(self.url, {"id": "222222222", "lang": "en"}, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_duplicate_guild(self, sample_guilds):
        """Test that the API returns a 400 when trying to create a guild with an ID that already exists."""

        self.client.force_authenticate(user=self.user)

        existing_guild = sample_guilds[0]
        response = self.client.post(
            self.url, {"id": str(existing_guild.id), "lang": "en"}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_guild(self, sample_guilds):
        """Test that the API can update an existing guild."""

        self.client.force_authenticate(user=self.user)

        guild = sample_guilds[0]
        data = {
            "lang": "es",
        }
        response = self.client.patch(f"{self.url}{guild.id}/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(guild.id)
        assert response.data["lang"]["code"] == data["lang"]

        # Verify that an event was published to Redis
        assert self.mock_publish.called

    def test_delete_guild(self, sample_guilds):
        """Test that the API can delete a guild."""

        self.client.force_authenticate(user=self.user)

        guild = sample_guilds[0]
        response = self.client.delete(f"{self.url}{guild.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Guild.objects.filter(id=guild.id).exists()

    def test_update_version_increment(self, sample_guilds):
        """Test that the version field increments on update."""

        self.client.force_authenticate(user=self.user)

        guild = sample_guilds[0]
        original_version = guild.version

        data = {
            "lang": "es",
        }
        response = self.client.patch(f"{self.url}{guild.id}/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["version"] == original_version + 1

    def test_update_at_field(self, sample_guilds):
        """Test that the updated_at field updates on update."""

        self.client.force_authenticate(user=self.user)

        guild = sample_guilds[0]
        original_updated_at = guild.updated_at

        data = {
            "lang": "es",
        }
        response = self.client.patch(f"{self.url}{guild.id}/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["updated_at"] != original_updated_at.isoformat().replace("+00:00", "Z")


class TestGossiper:
    def test_event_name_valid(self):
        """Test that event_name returns the correct string for valid inputs."""

        assert event_name("guild", "created") == "lucy.guild.created"
        assert event_name("language", "updated") == "lucy.language.updated"
        assert event_name("guild", "deleted") == "lucy.guild.deleted"

    def test_event_name_invalid_model(self):
        """Test that event_name raises ValueError for an invalid model."""

        with pytest.raises(ValueError, match="Invalid value: invalid_model"):
            event_name("invalid_model", "created")

    def test_event_name_invalid_event(self):
        """Test that event_name raises ValueError for an invalid event."""

        with pytest.raises(ValueError, match="Invalid value: invalid_event"):
            event_name("guild", "invalid_event")

    def test_redis_payload(self):
        """Test that redis_payload returns a dictionary with the correct structure."""

        data = {
            "event": "guild.created",
            "version": 1,
            "updated_at": "2024-01-01T00:00:00Z",
            "source": "api",
        }
        payload = redis_payload(**data)
        assert payload == data
