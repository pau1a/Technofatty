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


class BlogPaginationTests(TestCase):
    def test_page_one_redirects(self):
        response = self.client.get(reverse("blog") + "?page=1")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], reverse("blog"))

    def test_page_two_meta_tags(self):
        response = self.client.get(reverse("blog") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<link rel="canonical" href="https://technofatty.com/blog/?page=2">',
            html=True,
        )
        self.assertContains(
            response,
            '<link rel="prev" href="https://technofatty.com/blog/">',
            html=True,
        )
        self.assertNotContains(response, 'rel="next"')
        self.assertContains(
            response,
            '<title>Blog — Page 2 | Technofatty</title>',
            html=True,
        )
        self.assertContains(
            response,
            '<span class="pager__current">Page 2 of 2</span>',
            html=True,
        )
