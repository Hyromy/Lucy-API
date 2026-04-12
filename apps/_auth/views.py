import logging

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie, get_token
from requests import RequestException, get, post

from project.config import config

logger = logging.getLogger(__name__)


def discord_login(request) -> HttpResponseRedirect:
    auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={config.DISCORD_CLIENT_ID}"
        f"&redirect_uri={config.DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )
    return redirect(auth_url)


def discord_callback(request: HttpRequest) -> HttpResponseRedirect:
    def append_redirect(error_code: str | None = None) -> str:
        base_url = config.FRONTEND_URL.rstrip("/")
        path = config.FRONTEND_AUTH_CALLBACK_URL.lstrip("/")

        err = f"?error={error_code}" if error_code else ""
        return f"{base_url}/{path}{err}"

    code = request.GET.get("code")
    if not code:
        return redirect(append_redirect("missing_code"))

    data = {
        "client_id": config.DISCORD_CLIENT_ID,
        "client_secret": config.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.DISCORD_REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = post(
            "https://discord.com/api/oauth2/token",
            data=data,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    except RequestException:
        logger.exception("Discord OAuth token exchange failed")
        return redirect(append_redirect("token_exchange_failed"))

    token_json = response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return redirect(append_redirect("no_access_token"))

    user_json = _fetch_discord_user(access_token)
    if not user_json or "username" not in user_json:
        return redirect(append_redirect("user_fetch_failed"))

    user, _ = User.objects.get_or_create(
        username=user_json["username"],
    )

    login(request, user)
    get_token(request)

    return redirect(append_redirect())


def _fetch_discord_user(access_token: str) -> dict | None:
    try:
        user_response = get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        user_response.raise_for_status()
        return user_response.json()

    except RequestException:
        logger.exception("Discord OAuth user data fetch failed")
        return None


@ensure_csrf_cookie
def auth_me(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False}, status=200)

    return JsonResponse(
        {
            "authenticated": True,
            "id": request.user.id,
            "username": request.user.username,
            "first_name": request.user.first_name,
        }
    )


def auth_logout(request: HttpRequest) -> JsonResponse:
    was_authenticated = request.user.is_authenticated
    logout(request)
    return JsonResponse({"ok": True, "was_authenticated": was_authenticated}, status=200)
