from django.urls import path

from .views import (
    me,
    guilds,
    guilds_get_one,
)

urlpatterns = [
    path("me/", me, name="discord_me"),
    path("guilds/", guilds, name="discord_guilds"),
    path("guilds/<str:id>/", guilds_get_one, name="discord_guilds_get_one"),
]
