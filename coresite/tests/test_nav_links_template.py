from html.parser import HTMLParser

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase

from coresite.context_processors import NAV_LINKS


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


class NavLinkTemplateTests(TestCase):
    def render_links(self, location: str):
        request = RequestFactory().get("/")
        context = {
            "nav_links": NAV_LINKS,
            "location": location,
            "user": AnonymousUser(),
            "request": request,
        }
        html = render_to_string("coresite/partials/global/nav_links.html", context)
        parser = LinkParser()
        parser.feed(html)
        return parser.links

    def test_header_links_have_data_attributes_and_correct_values(self):
        links = self.render_links("header")
        for link in links:
            assert "data-analytics-event" in link
            assert "data-analytics-label" in link
            assert "data-analytics-url" in link

        knowledge = next(l for l in links if l["data-analytics-label"] == "Knowledge")
        assert knowledge["href"] == "/knowledge/"
        assert knowledge["data-analytics-event"] == "nav_link_click"
        assert knowledge["data-analytics-url"] == "/knowledge/"

    def test_footer_links_have_data_attributes_and_correct_values(self):
        links = self.render_links("footer")
        for link in links:
            assert "data-analytics-event" in link
            assert "data-analytics-label" in link
            assert "data-analytics-url" in link

        about = next(l for l in links if l["data-analytics-label"] == "About")
        assert about["href"] == "/about/"
        assert about["data-analytics-event"] == "nav_link_click"
        assert about["data-analytics-url"] == "/about/"
