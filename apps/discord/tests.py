import pytest
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client
from django.urls import reverse

from .models import Member


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def auth_user(db) -> User:
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def member(db, auth_user: User) -> Member:
    return Member.objects.create(
        id=123456789,
        user=auth_user,
        access_token="fake_access_token",
        refresh_token="fake_refresh_token",
    )


@pytest.fixture(autouse=True)
def clear_django_cache():
    cache.clear()


@pytest.mark.django_db
class TestDiscordViews:
    def test_me_anonymous_user(self, client: Client):
        """Should return authenticated=False for anonymous users."""

        response = client.get(reverse("discord_me"))

        assert response.status_code == 200
        assert response.json() == {"authenticated": False}

    @patch("apps.discord.views._ask_to_discord")
    def test_me_authenticated_user_filtered_fields(
        self,
        mock_ask: MagicMock,
        client: Client,
        auth_user: User,
        member: Member,
    ):
        """Should include only allowed Discord fields."""

        mock_ask.return_value = {
            "id": "123456789",
            "username": "discord_name",
            "global_name": "Discord Global",
            "avatar": "avatar_hash",
            "email": "hidden@example.com",
        }

        client.force_login(auth_user)
        response = client.get(reverse("discord_me"))
        payload = response.json()

        assert response.status_code == 200
        assert payload["authenticated"] is True
        assert payload["id"] == "123456789"
        assert payload["username"] == "discord_name"
        assert payload["global_name"] == "Discord Global"
        assert payload["avatar"] == "avatar_hash"
        assert "email" not in payload

    @patch("apps.discord.views._ask_to_discord")
    def test_me_ignores_none_values(
        self,
        mock_ask: MagicMock,
        client: Client,
        auth_user: User,
        member: Member,
    ):
        """Should omit keys with None values."""

        mock_ask.return_value = {
            "id": "123456789",
            "username": None,
            "global_name": None,
            "avatar": "avatar_hash",
        }

        client.force_login(auth_user)
        response = client.get(reverse("discord_me"))
        payload = response.json()

        assert response.status_code == 200
        assert payload["authenticated"] is True
        assert payload["id"] == "123456789"
        assert payload["avatar"] == "avatar_hash"
        assert "username" not in payload
        assert "global_name" not in payload

    def test_guilds_anonymous_user(self, client: Client):
        """Should redirect anonymous users to login."""

        response = client.get(reverse("discord_guilds"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    @patch("apps.discord.views._ask_to_discord")
    def test_guilds_filters_owner_or_admin(
        self,
        mock_ask: MagicMock,
        client: Client,
        auth_user: User,
        member: Member,
    ):
        """Should keep guilds where user is owner or has admin permission."""

        mock_ask.return_value = [
            {"id": "1", "name": "owner-guild", "owner": True, "permissions": "0"},
            {"id": "2", "name": "admin-guild", "owner": False, "permissions": "32"},
            {"id": "3", "name": "normal-guild", "owner": False, "permissions": "8"},
        ]

        client.force_login(auth_user)
        response = client.get(reverse("discord_guilds"))
        payload = response.json()

        assert response.status_code == 200
        assert len(payload) == 2
        assert {g["id"] for g in payload} == {"1", "2"}

    @patch("apps.discord.views._ask_to_discord")
    def test_guilds_uses_cache(
        self,
        mock_ask: MagicMock,
        client: Client,
        auth_user: User,
        member: Member,
    ):
        """Should call Discord only once while cache is warm."""

        mock_ask.return_value = [
            {"id": "2", "name": "admin-guild", "owner": False, "permissions": "32"},
        ]

        client.force_login(auth_user)

        first = client.get(reverse("discord_guilds"))
        second = client.get(reverse("discord_guilds"))

        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json() == second.json()
        assert mock_ask.call_count == 1
