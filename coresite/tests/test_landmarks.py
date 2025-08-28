import re
import pytest
from django.urls import reverse, NoReverseMatch

PAGES = ["home", "about", "contact", "blog", "support", "resources", "tools"]

@pytest.mark.parametrize("urlname", PAGES)
def test_no_role_region_on_core_pages(client, urlname):
    try:
        url = reverse(urlname)
    except NoReverseMatch:
        pytest.skip(f"{urlname} not routed")
    res = client.get(url)
    html = res.content.decode()
    assert 'role="region"' not in html

def test_404_has_no_region_role(client, settings):
    settings.DEBUG = False  # force default 404 template
    res = client.get("/definitely-not-here-xyz/")
    html = res.content.decode()
    assert 'role="region"' not in html

def test_500_has_no_region_role(client, settings):
    # This simulates rendering the 500 template directly if you have a route; otherwise skip.
    try:
        url = reverse("five_hundred_test")  # if you don't have one, skip
    except NoReverseMatch:
        pytest.skip("No explicit 500 route to exercise")
    res = client.get(url)
    html = res.content.decode()
    assert 'role="region"' not in html
