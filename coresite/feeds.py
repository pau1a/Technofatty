from django.contrib.syndication.views import Feed
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.feedgenerator import Atom1Feed

from .models import BlogPost, KnowledgeArticle


class BlogRSSFeed(Feed):
    title = "Technofatty Blog"
    link = "/blog/"
    description = "Latest news and insights from Technofatty."

    def items(self):
        return BlogPost.published.order_by("-published_at")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        return reverse("blog_post", args=[item.slug])

    def item_pubdate(self, item):
        pubdate = item.published_at or timezone.now()
        if timezone.is_naive(pubdate):
            pubdate = timezone.make_aware(pubdate, timezone.utc)
        return pubdate


class BlogAtomFeed(BlogRSSFeed):
    feed_type = Atom1Feed
    subtitle = BlogRSSFeed.description


class KnowledgeRSSFeed(Feed):
    title = "Technofatty Knowledge"
    link = "/knowledge/"
    description = "Latest knowledge articles from Technofatty."

    def items(self):
        return (
            KnowledgeArticle.published.select_related("category").order_by("-published_at")[:10]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.blurb

    def item_link(self, item):
        return reverse("knowledge_article", args=[item.category.slug, item.slug])

    def item_pubdate(self, item):
        pubdate = item.published_at or timezone.now()
        if timezone.is_naive(pubdate):
            pubdate = timezone.make_aware(pubdate, timezone.utc)
        return pubdate


class KnowledgeAtomFeed(KnowledgeRSSFeed):
    feed_type = Atom1Feed
    subtitle = KnowledgeRSSFeed.description


def blog_json_feed(request):
    posts = BlogPost.published.order_by("-published_at")[:10]
    items = [
        {
            "title": p.title,
            "link": request.build_absolute_uri(reverse("blog_post", args=[p.slug])),
            "excerpt": p.excerpt,
        }
        for p in posts
    ]
    return JsonResponse({"items": items})


def knowledge_json_feed(request):
    articles = (
        KnowledgeArticle.published.select_related("category").order_by("-published_at")[:10]
    )
    items = [
        {
            "title": a.title,
            "link": request.build_absolute_uri(
                reverse("knowledge_article", args=[a.category.slug, a.slug])
            ),
            "blurb": a.blurb,
        }
        for a in articles
    ]
    return JsonResponse({"items": items})
