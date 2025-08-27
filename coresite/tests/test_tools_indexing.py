import re
import pytest
from django.urls import reverse
from django.test import override_settings


def test_tools_view_not_indexable(client):
    res = client.get(reverse("tools"))
    assert res["X-Robots-Tag"] == "noindex,nofollow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="noindex,nofollow"\s*/?>',
        res.content.decode(),
        re.I,
    )


@override_settings(TOOLS_INDEXABLE=True)
def test_tools_view_indexable(client):
    res = client.get(reverse("tools"))
    assert res["X-Robots-Tag"] == "index,follow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="index,follow"\s*/?>',
        res.content.decode(),
        re.I,
    )


def test_tools_has_canonical(client):
    res = client.get(reverse("tools"))
    assert '<link rel="canonical"' in res.content.decode()
