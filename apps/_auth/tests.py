import pytest
from unittest.mock import (
    patch,
    MagicMock,
)

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestDiscordAuth:
    class TestLogin:
        def test_discord_login(self):
            """ Test the discord login view. """

            client = Client()
            url = reverse("discord_login")
            response = client.get(url)

            assert response.status_code == 302
            assert "discord.com/api/oauth2/authorize" in response.url

        def test_discord_login_url_params(self):
            """ Test that the discord login URL contains the correct parameters. """

            client = Client()
            response = client.get(reverse("discord_login"))

            redirect_url = response.url

            assert "client_id=" in redirect_url
            assert "redirect_uri=" in redirect_url
            assert "response_type=code" in redirect_url
            assert "scope=identify" in redirect_url

    class TestCallback:
        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback(self, mock_get: MagicMock, mock_post: MagicMock):
            """ Test the discord callback view with a successful flow. """

            mock_post.return_value.json.return_value = {
                "access_token": "fake_token"
            }

            mock_get.return_value.json.return_value = {
                "id": "123456789",
                "username": "testUser",
            }

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 200
            assert response.json()["username"] == "testUser"

            assert User.objects.filter(username = "testUser").exists()

        @patch("apps._auth.views.post")
        def test_discord_callback_invalid_code(self, mock_post: MagicMock):
            """ Test the discord callback view with an invalid code. """

            mock_post.return_value.json.return_value = {"error": "invalid_grant"}

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "wrong_code"})

            assert response.status_code == 400
            assert response.json()["error"] == "invalid_grant"

        @patch("apps._auth.views.post")
        @patch("apps._auth.views.get")
        def test_discord_callback_existing_user(self, mock_get: MagicMock, mock_post: MagicMock):
            """ Test the discord callback view with an existing user. """

            User.objects.create(username = "testUser")

            mock_post.return_value.json.return_value = {
                "access_token": "fake_token"
            }

            mock_get.return_value.json.return_value = {
                "id": "123456789",
                "username": "testUser",
            }

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url, {"code": "fake_code"})

            assert response.status_code == 200
            assert response.json()["username"] == "testUser"

            assert User.objects.filter(username = "testUser").count() == 1

        def test_discord_callback_no_code(self):
            """ Test the discord callback view with no code provided. """

            client = Client()
            url = reverse("discord_callback")
            response = client.get(url)

            assert response.status_code == 400

