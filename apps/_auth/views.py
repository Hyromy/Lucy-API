from os import getenv
from django.shortcuts import redirect
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from requests import get, post
from django.contrib.auth.models import User

def discord_login(request) -> HttpResponseRedirect:
    auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={getenv("DISCORD_CLIENT_ID")}"
        f"&redirect_uri={getenv("DISCORD_REDIRECT_URI")}"
        f"&response_type=code"
        f"&scope=identify"
    )

    return redirect(auth_url)

def discord_callback(request: HttpRequest) -> JsonResponse:
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code provided"}, status = 400)

    data = {
        "client_id": getenv("DISCORD_CLIENT_ID"),
        "client_secret": getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": getenv("DISCORD_REDIRECT_URI"),
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = post("https://discord.com/api/oauth2/token",
        data = data,
        headers = headers
    )
    token_json = response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return JsonResponse(token_json, status = 400)

    return _process_token_from_discord(access_token)

def _process_token_from_discord(access_token: str) -> JsonResponse:
    user_response = get("https://discord.com/api/users/@me",
        headers = {"Authorization": f"Bearer {access_token}"}
    )
    user_json = user_response.json()

    if "username" not in user_json:
        return JsonResponse(user_json, status = 400)

    User.objects.get_or_create(
        username = user_json["username"],
        defaults = {
            "first_name": user_json["username"]
        }
    )

    return JsonResponse(user_json)
