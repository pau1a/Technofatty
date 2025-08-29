from types import SimpleNamespace

from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from coresite.middleware import PENDING_POST_QUEUE, PostRateLimitMiddleware


def dummy_view(request):
    return HttpResponse("ok")


class PostRateLimitMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        PENDING_POST_QUEUE.clear()
        self.factory = RequestFactory()
        self.middleware = PostRateLimitMiddleware(dummy_view)

    def test_rate_limit(self):
        user = SimpleNamespace(is_authenticated=True, id=1, approved_posts=3, is_verified=True)
        req1 = self.factory.post("/community/post/", {"body": "hi"})
        req1.user = user
        self.assertEqual(self.middleware(req1).status_code, 200)
        req2 = self.factory.post("/community/post/", {"body": "hi"})
        req2.user = user
        self.assertEqual(self.middleware(req2).status_code, 429)

    def test_link_throttle(self):
        user = SimpleNamespace(is_authenticated=True, id=2, approved_posts=0, is_verified=True)
        req = self.factory.post(
            "/community/post/",
            {"body": "http://a.com http://b.com"},
        )
        req.user = user
        self.assertEqual(self.middleware(req).status_code, 400)

    def test_queue_unverified_first_post(self):
        user = SimpleNamespace(is_authenticated=True, id=3, approved_posts=0, is_verified=False)
        req = self.factory.post("/community/post/", {"body": "hi", "title": "t"})
        req.user = user
        resp = self.middleware(req)
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(len(PENDING_POST_QUEUE), 1)
