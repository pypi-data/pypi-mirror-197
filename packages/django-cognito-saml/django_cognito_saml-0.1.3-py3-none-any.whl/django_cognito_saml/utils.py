import base64
import json
from typing import cast
from urllib.parse import parse_qsl, urlsplit
from uuid import uuid4

from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse


def generate_state(request: "HttpRequest") -> str:
    return base64.b64encode(
        json.dumps(
            {
                "redirect_uri": get_cognito_callback_url(request),
                "key": str(uuid4()),
            }
        ).encode()
    ).decode()


def generate_return_uri(request: "HttpRequest") -> str:
    """Try to use `next` url if passed through
    if not default to settings.LOGIN_REDIRECT_URL"""
    referrer = cast(str, request.META.get("HTTP_REFERER"))
    if not referrer:
        return settings.LOGIN_REDIRECT_URL

    referrer_path = urlsplit(referrer)[2]
    if referrer_path == reverse("login") or referrer_path.startswith(
        reverse("rest_framework:login")
    ):
        # If referred from login page, try to grab the ?next param.
        return (
            dict(parse_qsl(urlsplit(referrer).query)).get("next")
            or settings.LOGIN_REDIRECT_URL
        )
    elif referrer_path.startswith(reverse("logout")):
        # If referrer is logout page, don't take them back there..
        return settings.LOGIN_REDIRECT_URL
    else:
        # Else just redirect back to referrer.
        return referrer


def get_cognito_callback_url(request: HttpRequest) -> str:
    return request.build_absolute_uri(reverse("cognito_callback"))
