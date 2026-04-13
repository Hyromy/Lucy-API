from django.urls import path

from .views import (
    me,
    guilds,
)

urlpatterns = [
    path("me/", me, name="discord_me"),
    path("guilds/", guilds, name="discord_guilds"),
]
