import pytest
from django.test import RequestFactory
from django.core import signing

from coresite.context_processors import analytics_flags


def test_consent_not_granted_without_cookie():
    rf = RequestFactory()
    request = rf.get('/')
    context = analytics_flags(request)
    assert context['CONSENT_GRANTED'] is False


def test_consent_granted_with_valid_cookie(settings):
    rf = RequestFactory()
    request = rf.get('/')
    request.COOKIES['tf_consent'] = signing.dumps('true')
    context = analytics_flags(request)
    assert context['CONSENT_GRANTED'] is True


def test_consent_not_granted_with_invalid_cookie(settings):
    rf = RequestFactory()
    request = rf.get('/')
    request.COOKIES['tf_consent'] = 'true'  # unsigned value
    context = analytics_flags(request)
    assert context['CONSENT_GRANTED'] is False
