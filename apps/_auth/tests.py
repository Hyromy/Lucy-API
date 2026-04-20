import pytest
from unittest.mock import (
    patch,
    MagicMock,
)

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from apps.discord.models import Member


@pytest.mark.django_db
class TestDiscordAuth:
    class TestLogin:
        def test_discord_login(self):
            """Test the discord login view."""

            client = Client()
            url = reverse("discord_login")
            response = client.get(url)

            assert response.status_code == 302
            assert "discord.com/api/oauth2/authorize" in response.url

        def test_discord_login_url_params(self):
            """Test that the discord login URL contains the correct parameters."""

            client = Client()
            response = client.get(reverse("discord_login"))

            redirect_url = response.url

            assert "client_id=" in redirect_url
            assert "redirect_uri=" in redirect_url
            assert "response_type=code" in redirect_url
            assert "scope=identify" in redirect_url
            assert "guilds" in redirect_url

    class TestCallback:
        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback(self, mock_get: MagicMock, mock_post: MagicMock):
            """Test the discord callback view with a successful flow."""

            mock_post.return_value.json.return_value = {
                "access_token": "fake_token",
                "refresh_token": "fake_refresh_token",
            }

            mock_get.return_value.json.return_value = {
                "id": "123456789",
                "username": "testUser",
            }

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 302
            assert "/auth/callback" in response.url

            assert User.objects.filter(username="testUser").exists()
            member = Member.objects.get(id="123456789")
            assert member.access_token == "fake_token"
            assert member.refresh_token == "fake_refresh_token"

        @patch("apps._auth.views.post")
        def test_discord_callback_invalid_code(self, mock_post: MagicMock):
            """Test the discord callback view with an invalid code."""

            from requests import RequestException

            mock_post.side_effect = RequestException("Token exchange failed")

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "wrong_code"})

            assert response.status_code == 302
            assert "error=token_exchange_failed" in response.url

        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback_existing_user(self, mock_get: MagicMock, mock_post: MagicMock):
            """Test the discord callback view with an existing user."""

            User.objects.create(username="testUser")

            mock_post.return_value.json.return_value = {
                "access_token": "fake_token",
                "refresh_token": "fake_refresh_token",
            }

            mock_get.return_value.json.return_value = {
                "id": "123456789",
                "username": "testUser",
            }

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 302
            assert "/auth/callback" in response.url

            assert User.objects.filter(username="testUser").count() == 1

        @patch("apps._auth.views.post")
        def test_discord_callback_no_access_token(self, mock_post: MagicMock):
            """Test callback when Discord response has no access token."""

            mock_post.return_value.json.return_value = {}

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 302
            assert "error=no_access_token" in response.url

        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback_user_fetch_failed(
            self, mock_get: MagicMock, mock_post: MagicMock
        ):
            """Test callback when user fetch from Discord fails."""

            mock_post.return_value.json.return_value = {"access_token": "fake_token"}
            mock_get.return_value.json.return_value = {}

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 302
            assert "error=user_fetch_failed" in response.url

        @patch("apps._auth.views.User.objects.get_or_create")
        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback_transaction_failed(
            self,
            mock_get: MagicMock,
            mock_post: MagicMock,
            mock_get_or_create: MagicMock,
        ):
            """Test callback when database transaction fails."""

            mock_post.return_value.json.return_value = {
                "access_token": "fake_token",
                "refresh_token": "fake_refresh_token",
            }
            mock_get.return_value.json.return_value = {
                "id": "123456789",
                "username": "testUser",
            }
            mock_get_or_create.side_effect = Exception("db failure")

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 302
            assert "error=transaction_failed" in response.url

        def test_discord_callback_no_code(self):
            """Test the discord callback view with no code provided."""

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url)

            assert response.status_code == 302
            assert "error=missing_code" in response.url

    class TestSession:
        def test_auth_logout(self):
            """Test the logout view."""

            user = User.objects.create_user(username="testuser")
            client = Client()
            client.force_login(user)

            assert "_auth_user_id" in client.session

            url = reverse("auth_logout")
            response = client.post(url)

            assert response.status_code == 200
            assert response.json() == {"ok": True, "was_authenticated": True}
            assert "_auth_user_id" not in client.session
