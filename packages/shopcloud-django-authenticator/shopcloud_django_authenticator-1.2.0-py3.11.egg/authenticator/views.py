from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def _encode_jwt(request) -> Optional[dict]:
    token = request.GET.get('token')
    if token is None:
        return None

    if settings.AUTHENTICATOR_KEY is None:
        return None

    data = jwt.decode(
        token,
        settings.AUTHENTICATOR_KEY,
        algorithms="HS256",
        options={
            "require": [
                "exp",
                "iss",
                "nbf"
            ]
        }
    )
    if data.get('iss') not in ['shopcloud-secrethub', 'shopcloud-tower']:
        return None

    return data


def login_view(request):
    try:
        data = _encode_jwt(request)
    except Exception:
        return HttpResponseUnauthorized()

    if data is None:
        return HttpResponseUnauthorized()

    user = User.objects.filter(username=data.get('username')).first()
    password = User.objects.make_random_password()
    if user is None:
        user = User.objects.create(
            username=data.get('username'),
            password=password,
        )

    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True if "admin" in data.get('scopes', []) else False
    user.save()

    login(request, user)

    return redirect('/', permanent=False)


def login_credential_rotation(request):
    try:
        data = _encode_jwt(request)
    except Exception:
        return HttpResponseUnauthorized()

    if data is None:
        return HttpResponseUnauthorized()

    user = User.objects.filter(username=data.get('username')).first()
    if user is None:
        return JsonResponse({
            'status': 'not-found',
        }, status=200)

    password = User.objects.make_random_password()
    user.set_password(password)
    user.save()

    return JsonResponse({
        'status': 'ok',
    }, status=201)
