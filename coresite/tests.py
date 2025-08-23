from django.test import TestCase
from django.urls import reverse


class BlogRssTests(TestCase):
    def test_rss_feed_endpoint(self):
        response = self.client.get(reverse("blog_rss"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "application/rss+xml; charset=utf-8"
        )
        self.assertIn(b"<rss", response.content)
        self.assertIn(b"<channel>", response.content)
