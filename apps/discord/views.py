import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from requests import RequestException, get

from .models import Member

logger = logging.getLogger(__name__)


def _ask_to_discord(endpoint: str, access_token: str) -> dict | None:
    """Request data from Discord API using the provided access token."""

    endpoint = endpoint.strip("/")
    url = f"https://discord.com/api/v10/{endpoint}"
    try:
        response = get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
        response.raise_for_status()
        return response.json()

    except RequestException as e:
        logging.exception(f"Discord API request to {url} failed", exc_info=e)
        return None


@ensure_csrf_cookie
def me(request: HttpRequest) -> JsonResponse:
    def purge_discord_user_data(data: dict) -> dict:
        if not data:
            return {}

        allowed_fields = {
            "avatar",
            "global_name",
            "id",
            "username",
        }
        return {
            key: value for key, value in data.items() if key in allowed_fields and value is not None
        }

    user: User = request.user
    data = {"authenticated": user.is_authenticated}
    if data["authenticated"]:
        member = Member.objects.filter(user=user).first()
        data.update(
            purge_discord_user_data(
                _ask_to_discord("users/@me", member.access_token) if member else None
            )
        )

    return JsonResponse(data, status=200)


@login_required
def guilds(request: HttpRequest) -> JsonResponse:
    def filter_by_owner_or_admin(guilds: list[dict]) -> list[dict]:
        return [
            guild
            for guild in guilds
            if guild.get("owner") or (int(guild.get("permissions", 0)) & 0x20)
        ]

    user: User = request.user
    member = Member.objects.filter(user=user).first()

    if not member:
        return JsonResponse([], safe=False)

    cache_key = f"discord_guilds_{member.id}"
    data = cache.get(cache_key)

    if data is None:
        raw_guilds = _ask_to_discord("users/@me/guilds", member.access_token) or []
        data = filter_by_owner_or_admin(raw_guilds)
        cache.set(cache_key, data, timeout=300)

    return JsonResponse(data, status=200, safe=False)
