import pytest
from django.urls import reverse
from django.test import override_settings
from django.conf import settings


@pytest.mark.parametrize(
    "case_flag, tool_flag, expect_case, expect_tool",
    [
        (False, False, True, True),
        (True, False, False, True),
        (False, True, True, False),
        (True, True, False, False),
    ],
)
def test_robots_txt_respects_flags(client, case_flag, tool_flag, expect_case, expect_tool):
    with override_settings(CASE_STUDIES_INDEXABLE=case_flag, TOOLS_INDEXABLE=tool_flag):
        res = client.get(reverse("robots_txt"), HTTP_HOST="technofatty.com")
    lines = res.content.decode().splitlines()
    assert "Allow: /" in lines
    if expect_case:
        assert "Disallow: /case-studies/" in lines
    else:
        assert "Disallow: /case-studies/" not in lines
    if expect_tool:
        assert "Disallow: /tools/" in lines
    else:
        assert "Disallow: /tools/" not in lines
    assert f"Sitemap: {settings.SITE_BASE_URL}/sitemap.xml" in lines
