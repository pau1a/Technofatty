from django.urls import reverse
from django.db import connections


def test_db_health(client):
    resp = client.get(reverse('health_db'))
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}
    assert resp['Cache-Control'] == 'no-store'


def test_cache_health(client):
    resp = client.get(reverse('health_cache'))
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}
    assert resp['Cache-Control'] == 'no-store'


def test_live_health(client):
    resp = client.get(reverse('health_live'))
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}
    assert resp['Cache-Control'] == 'no-store'


def test_db_health_error_hides_detail(client, monkeypatch, settings):
    class BadCursor:
        def __enter__(self):
            raise Exception('boom')

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(connections['default'], 'cursor', lambda *a, **kw: BadCursor())
    settings.DEBUG = False
    resp = client.get(reverse('health_db'))
    assert resp.status_code == 500
    assert resp.json() == {'status': 'error'}


def test_db_health_error_shows_detail_when_debug(client, monkeypatch, settings):
    class BadCursor:
        def __enter__(self):
            raise Exception('boom')

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(connections['default'], 'cursor', lambda *a, **kw: BadCursor())
    settings.DEBUG = True
    resp = client.get(reverse('health_db'))
    assert resp.status_code == 500
    assert resp.json() == {'status': 'error', 'detail': 'boom'}
