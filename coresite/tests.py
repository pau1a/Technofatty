from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.conf import settings


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


class LegacyRoutesTests(TestCase):
    def test_services_redirects(self):
        response = self.client.get("/SERVICES/?utm=test")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"], "https://technofatty.com/about/?utm=test"
        )

    def test_signup_redirects(self):
        response = self.client.get("/SIGNUP")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"], "https://technofatty.com/#signup"
        )

    def test_community_join_redirects(self):
        response = self.client.get("/Community/Join")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"], "https://technofatty.com/community/"
        )

    def test_signal_redirects(self):
        response = self.client.get("/Signals/MODEL-Tuning/?ref=1")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "https://technofatty.com/knowledge/signals/?ref=1#signal-model-tuning",
        )

    def test_account_archived(self):
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("noindex,nofollow,noarchive", response.content.decode())


class UrlResolutionTests(SimpleTestCase):
    def test_core_urls_reverse(self):
        names = [
            "home",
            "knowledge",
            "tools",
            "case_studies_landing",
            "community",
            "blog",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertIsInstance(reverse(name), str)


class RobotsTxtTests(SimpleTestCase):
    def test_non_production_disallows(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertContains(response, "Disallow: /")

    @override_settings(IS_PRODUCTION=True)
    def test_production_allows(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertContains(response, "Allow: /")


class SettingsSanityTests(SimpleTestCase):
    def test_no_empty_allowed_hosts(self):
        self.assertTrue(settings.ALLOWED_HOSTS)
        self.assertNotIn("", settings.ALLOWED_HOSTS)
