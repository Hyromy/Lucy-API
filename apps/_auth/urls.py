from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    discord_login,
    discord_callback,
    auth_logout,
)

urlpatterns = [
    path("discord/login/", discord_login, name="discord_login"),
    path("discord/callback/", discord_callback, name="discord_callback"),
    path("logout/", auth_logout, name="auth_logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
