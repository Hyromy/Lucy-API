from django.contrib import admin
from django.urls import path, include

from apps.api import urls as api_urls
from apps._auth import urls as auth_urls
from apps.discord import urls as discord_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("auth/", include(auth_urls)),
    path("discord/", include(discord_urls)),
]
