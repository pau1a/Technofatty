import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.core import signing
from django.urls import reverse

from coresite.context_processors import analytics_flags
from coresite.middleware import ConsentMiddleware


def _apply_middleware(request):
    middleware = ConsentMiddleware(lambda req: HttpResponse("OK"))
    middleware(request)


def test_consent_not_granted_without_cookie():
    rf = RequestFactory()
    request = rf.get('/')
    _apply_middleware(request)
    context = analytics_flags(request)
    assert request.CONSENT_GRANTED is False
    assert context['CONSENT_GRANTED'] is False


def test_consent_granted_with_valid_cookie(settings):
    rf = RequestFactory()
    request = rf.get('/')
    request.COOKIES[settings.CONSENT_COOKIE_NAME] = signing.dumps('true')
    _apply_middleware(request)
    context = analytics_flags(request)
    assert request.CONSENT_GRANTED is True
    assert context['CONSENT_GRANTED'] is True


def test_consent_not_granted_with_invalid_cookie(settings):
    rf = RequestFactory()
    request = rf.get('/')
    request.COOKIES[settings.CONSENT_COOKIE_NAME] = 'true'  # unsigned value
    _apply_middleware(request)
    context = analytics_flags(request)
    assert request.CONSENT_GRANTED is False
    assert context['CONSENT_GRANTED'] is False


def test_accept_sets_signed_cookie(client, settings):
    response = client.get(reverse('consent_accept'), HTTP_REFERER='/prev/')
    assert response.status_code == 302
    assert response['Location'] == '/prev/'
    assert (
        signing.loads(
            response.cookies[settings.CONSENT_COOKIE_NAME].value
        )
        == 'true'
    )


def test_decline_sets_signed_cookie(client, settings):
    response = client.get(reverse('consent_decline'), HTTP_REFERER='/prev/')
    assert response.status_code == 302
    assert response['Location'] == '/prev/'
    assert (
        signing.loads(
            response.cookies[settings.CONSENT_COOKIE_NAME].value
        )
        == 'false'
    )


def test_cookie_settings_exposed(settings):
    rf = RequestFactory()
    request = rf.get('/')
    context = analytics_flags(request)
    assert context['CONSENT_COOKIE_NAME'] == settings.CONSENT_COOKIE_NAME
    assert context['CONSENT_COOKIE_MAX_AGE'] == settings.CONSENT_COOKIE_MAX_AGE
    assert context['CONSENT_COOKIE_SAMESITE'] == settings.CONSENT_COOKIE_SAMESITE
    assert context['CONSENT_COOKIE_SECURE'] == settings.CONSENT_COOKIE_SECURE
    assert context['CONSENT_COOKIE_HTTPONLY'] == settings.CONSENT_COOKIE_HTTPONLY
