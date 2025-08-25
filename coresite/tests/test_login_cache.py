import time

import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse


@pytest.mark.django_db
def test_failed_login_uses_cache_and_delay(client, monkeypatch):
    User.objects.create_user(username="tester", password="secret")
    login_url = reverse("account_login")
    calls = []

    def fake_sleep(seconds):
        calls.append(seconds)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    client.post(login_url, {"username": "tester", "password": "wrong"})
    assert cache.get("failed_login_tester") == 1
    assert calls[-1] == 1

    client.post(login_url, {"username": "tester", "password": "wrong"})
    assert cache.get("failed_login_tester") == 2
    assert calls[-1] == 2

    client.post(login_url, {"username": "tester", "password": "secret"})
    assert cache.get("failed_login_tester") is None
