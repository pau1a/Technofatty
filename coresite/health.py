from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import connections
from django.core.cache import cache


def _json_ok():
    resp = JsonResponse({"status": "ok"})
    resp["Cache-Control"] = "no-store"
    return resp


@require_GET
def db_health(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as exc:
        payload = {"status": "error"}
        if settings.DEBUG:
            payload["detail"] = str(exc)
        resp = JsonResponse(payload, status=500)
        resp["Cache-Control"] = "no-store"
        return resp
    return _json_ok()


@require_GET
def cache_health(request):
    try:
        cache.set("__healthcheck__", "ok", 1)
        if cache.get("__healthcheck__") != "ok":
            raise ValueError("cache read/write failed")
        cache.delete("__healthcheck__")
    except Exception as exc:
        payload = {"status": "error"}
        if settings.DEBUG:
            payload["detail"] = str(exc)
        resp = JsonResponse(payload, status=500)
        resp["Cache-Control"] = "no-store"
        return resp
    return _json_ok()


@require_GET
def live_health(request):
    return _json_ok()
