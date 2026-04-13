from django.urls import path

from .views import (
    discord_login,
    discord_callback,
    auth_logout,
)

urlpatterns = [
    path("discord/login/", discord_login, name="discord_login"),
    path("discord/callback/", discord_callback, name="discord_callback"),
    path("logout/", auth_logout, name="auth_logout"),
]
