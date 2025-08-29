from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.utils import timezone
from django.utils.feedgenerator import Rss201rev2Feed
from django.db.models import Q, Max
from newsletter.utils import log_newsletter_event
from django.core.cache import cache
from coresite.services.contact import contact_event
from .models import (
    SiteImage,
    BlogPost,
    KnowledgeCategory,
    KnowledgeArticle,
    Tool,
    CaseStudy,
    SITEMAP_CACHE_KEY,
)
from .forms import ContactForm
from .notifiers import ContactNotifier
from datetime import datetime
import hashlib
from .signals import get_signals_content
from .support import get_support_content
from .community import get_community_content
from .footer import get_footer_content


KNOWLEDGE_SUB_SECTIONS = [
    {"title": "Guides", "url_name": "knowledge_guides"},
    {"title": "Signals", "url_name": "knowledge_signals"},
    {"title": "Glossary", "url_name": "knowledge_glossary"},
    {"title": "Quick Wins", "url_name": "knowledge_quick_wins"},
]

# Legacy endpoints like /services/, /signup/, /community/join/, and /signals/<slug>/
# are intentionally omitted to keep retired paths out of the sitemap.
TOP_LEVEL_URLS = [
    {"loc": f"{settings.SITE_BASE_URL}/", "priority": "1.0", "changefreq": "weekly"},
    {
        "loc": f"{settings.SITE_BASE_URL}/knowledge/",
        "priority": "0.8",
        "changefreq": "weekly",
    },
    {"loc": f"{settings.SITE_BASE_URL}/blog/", "priority": "0.8", "changefreq": "weekly"},
    {
        "loc": f"{settings.SITE_BASE_URL}/resources/",
        "priority": "0.8",
        "changefreq": "weekly",
    },
    *(
        [
            {
                "loc": f"{settings.SITE_BASE_URL}/case-studies/",
                "priority": "0.7",
                "changefreq": "weekly",
            }
        ]
        if settings.CASE_STUDIES_INDEXABLE
        else []
    ),
    {
        "loc": f"{settings.SITE_BASE_URL}/community/",
        "priority": "0.8",
        "changefreq": "weekly",
    },
]


# Placeholder thread and related content data for the community hub.
THREADS = [
    {
        "title": "How do I deploy Technofatty?",
        "slug": "deploy-technofatty",
        "tags": ["deployment", "tf"],
        "replies": 3,
        "updated": datetime(2024, 1, 15),
        "answered": True,
        "author": "Priya",
    },
    {
        "title": "Scaling best practices?",
        "slug": "scaling-best-practices",
        "tags": ["scaling"],
        "replies": 0,
        "updated": datetime(2024, 2, 10),
        "answered": False,
        "author": "Liam",
    },
    {
        "title": "API authentication options",
        "slug": "api-authentication-options",
        "tags": ["api", "security"],
        "replies": 1,
        "updated": datetime(2024, 2, 5),
        "answered": False,
        "author": "Ava",
    },
]

RELATED_CONTENT_ITEMS = {
    "knowledge": [
        {"title": "Getting Started", "url": "/knowledge/getting-started/", "tags": ["deployment"]},
        {"title": "Scaling 101", "url": "/knowledge/scaling-101/", "tags": ["scaling"]},
        {"title": "API Security", "url": "/knowledge/api-security/", "tags": ["api", "security"]},
    ],
    "tools": [
        {"title": "TF CLI", "url": "/tools/tf-cli/", "tags": ["deployment"]},
    ],
    "case_studies": [
        {"title": "ACME scales with TF", "url": "/case-studies/acme/", "tags": ["scaling"]},
    ],
}


def _redirect_with_consent_flag(referer: str) -> str:
    parsed = urlparse(referer)
    query = dict(parse_qsl(parsed.query))
    query["consent"] = "updated"
    new_query = urlencode(query)
    return urlunparse(parsed._replace(query=new_query))


def consent_accept(request):
    redirect_to = _redirect_with_consent_flag(request.META.get("HTTP_REFERER", "/"))
    response = HttpResponseRedirect(redirect_to)
    response.set_signed_cookie(
        settings.CONSENT_COOKIE_NAME,
        "true",
        max_age=settings.CONSENT_COOKIE_MAX_AGE,
        samesite=settings.CONSENT_COOKIE_SAMESITE,
        secure=settings.CONSENT_COOKIE_SECURE,
        httponly=settings.CONSENT_COOKIE_HTTPONLY,
    )
    return response


def consent_decline(request):
    redirect_to = _redirect_with_consent_flag(request.META.get("HTTP_REFERER", "/"))
    response = HttpResponseRedirect(redirect_to)
    response.set_signed_cookie(
        settings.CONSENT_COOKIE_NAME,
        "false",
        max_age=settings.CONSENT_COOKIE_MAX_AGE,
        samesite=settings.CONSENT_COOKIE_SAMESITE,
        secure=settings.CONSENT_COOKIE_SECURE,
        httponly=settings.CONSENT_COOKIE_HTTPONLY,
    )
    return response


def homepage(request):
    resources = [
        {
            "title": "AI for Marketing",
            "blurb": "Boost campaigns with smarter targeting and automation.",
            "url": "/resources/marketing/",
        },
        {
            "title": "AI in Operations",
            "blurb": "Cut waste and streamline workflows with predictive AI.",
            "url": "/resources/operations/",
        },
    ]
    resources_sig = hashlib.md5(
        "|".join(r["title"] + r["url"] for r in resources).encode()
    ).hexdigest()
    cs_qs = CaseStudy.objects.filter(is_published=True)
    case_studies = cs_qs[:3]
    cs_ver = cs_qs.aggregate(v=Max("updated_at"))["v"]
    cs_ver_ts = int(cs_ver.timestamp()) if cs_ver else 0
    try:
        images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
    except Exception:
        images = {}
    signals = get_signals_content()
    support = get_support_content()
    community = get_community_content()
    footer = get_footer_content()
    context = {
        "site_images": images,
        "is_homepage": True,
        "now": datetime.now(),
        "resources": resources,
        "case_studies": case_studies,
        "featured_grid_version": f"{resources_sig}:{cs_qs.count()}:{cs_ver_ts}",
        "signals": signals,
        "support": support,
        "community": community,
        "footer": footer,
        "canonical_url": "/",
    }
    log_newsletter_event(request, "newsletter_block_view")
    return render(request, "coresite/homepage.html", context)


def signal_detail(request, slug: str):
    footer = get_footer_content()
    return render(
        request,
        "coresite/signal_placeholder.html",
        {"slug": slug, "footer": footer},
    )
def knowledge(request):
    page_str = request.GET.get("page")
    if page_str == "1":
        return HttpResponsePermanentRedirect(reverse("knowledge"))

    from django.core.paginator import Paginator, EmptyPage

    page_number = int(page_str or 1)

    # Base queryset for articles
    articles_qs = (
        KnowledgeArticle.published.select_related("category")
        .prefetch_related("tags")
        .order_by("-published_at")
    )

    # Optional filters
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    time_str = request.GET.get("time")
    subtype = request.GET.get("subtype")
    search = request.GET.get("q")

    if category_slug:
        articles_qs = articles_qs.filter(category__slug=category_slug)
    if tag_slug:
        articles_qs = articles_qs.filter(tags__slug=tag_slug)
    if subtype:
        articles_qs = articles_qs.filter(subtype=subtype)
    if time_str:
        try:
            minutes = int(time_str)
        except (TypeError, ValueError):
            minutes = None
        if minutes is not None:
            articles_qs = articles_qs.filter(reading_time__lte=minutes)
    if search:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search)
            | Q(blurb__icontains=search)
            | Q(tags__name__icontains=search)
        ).distinct()
    paginator = Paginator(articles_qs, 9)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        raise Http404

    page_articles = list(page_obj.object_list)
    if page_number == 1 and page_articles:
        featured_article = page_articles[0]
        remaining_articles = page_articles[1:]
    else:
        featured_article = None
        remaining_articles = page_articles

    has_content = bool(page_articles)
    if not has_content:
        remaining_articles = []

    categories_qs = KnowledgeCategory.published.all()

    base_params = request.GET.copy()
    if "page" in base_params:
        del base_params["page"]

    canonical_params = base_params.copy()
    if page_number > 1:
        canonical_params["page"] = str(page_number)
    canonical_query = canonical_params.urlencode()
    canonical_url = "/knowledge/" + (f"?{canonical_query}" if canonical_query else "")
    is_filtered = any(
        [category_slug, tag_slug, time_str, subtype, search]
    )

    def build_url(**kwargs):
        params = base_params.copy()
        for key, value in kwargs.items():
            if value is None:
                params.pop(key, None)
            else:
                params[key] = value
        query = params.urlencode()
        return reverse("knowledge") + (f"?{query}" if query else "")

    categories = [
        {"label": "All", "url": build_url(category=None), "active": not category_slug}
    ]
    for category in categories_qs:
        categories.append(
            {
                "label": category.title,
                "url": build_url(category=category.slug),
                "active": category_slug == category.slug,
            }
        )

    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge",
        "page_title": "Knowledge",
        "categories": categories,
        "featured": featured_article,
        "articles": remaining_articles,
        "page_obj": page_obj,
        "canonical_url": canonical_url,
        "has_content": has_content,
    }
    if is_filtered:
        context["meta_robots"] = "noindex,follow"
    response = render(request, "coresite/knowledge/index.html", context)
    if is_filtered:
        response["X-Robots-Tag"] = "noindex,follow"
    return response


def knowledge_category(request, category_slug: str):
    page_str = request.GET.get("page")
    if page_str == "1":
        return HttpResponsePermanentRedirect(
            reverse("knowledge_category", args=[category_slug])
        )

    from django.core.paginator import Paginator, EmptyPage

    page_number = int(page_str or 1)

    category = get_object_or_404(
        KnowledgeCategory.published, slug=category_slug
    )

    def absolute_page_url(num: int) -> str:
        return (
            f"/knowledge/{category_slug}/"
            if num == 1
            else f"/knowledge/{category_slug}/?page={num}"
        )

    articles_qs = (
        KnowledgeArticle.published.filter(category=category).order_by("-published_at")
    )
    paginator = Paginator(articles_qs, 9)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        raise Http404

    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": f"knowledge-{category_slug}",
        "page_title": category.title,
        "category": category,
        "articles": page_obj.object_list,
        "page_obj": page_obj,
        "canonical_url": absolute_page_url(page_number),
    }
    return render(request, "coresite/knowledge/category.html", context)


def knowledge_article(request, category_slug: str, article_slug: str):
    footer = get_footer_content()
    if request.GET.get("preview") == "1" and request.user.is_staff:
        category = get_object_or_404(KnowledgeCategory.objects, slug=category_slug)
        article = get_object_or_404(
            KnowledgeArticle.objects, category=category, slug=article_slug
        )
    else:
        category = get_object_or_404(
            KnowledgeCategory.published, slug=category_slug
        )
        article = get_object_or_404(
            KnowledgeArticle.published,
            category=category,
            slug=article_slug,
        )
    related_limit = 3
    related_articles = list(
        KnowledgeArticle.published.filter(category=category)
        .exclude(id=article.id)
        .order_by("-published_at")[:related_limit]
    )
    if len(related_articles) < related_limit:
        tags = article.tags.all()
        if tags:
            tag_related = (
                KnowledgeArticle.published.filter(tags__in=tags)
                .exclude(id=article.id)
                .exclude(id__in=[a.id for a in related_articles])
                .distinct()
                .order_by("-published_at")[: related_limit - len(related_articles)]
            )
            related_articles.extend(tag_related)

    context = {
        "footer": footer,
        "page_id": f"knowledge-{article_slug}",
        "page_title": article.title,
        "category": category,
        "article": article,
        "canonical_url": f"/knowledge/{category_slug}/{article_slug}/",
        "related_articles": related_articles,
    }
    return render(request, "coresite/knowledge/article.html", context)


def knowledge_guides(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-guides",
        "page_title": "Guides",
        "canonical_url": "/knowledge/guides/",
    }
    return render(request, "coresite/knowledge/guides.html", context)


def knowledge_signals(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-signals",
        "page_title": "Signals",
        "canonical_url": "/knowledge/signals/",
    }
    return render(request, "coresite/knowledge/signals.html", context)


def knowledge_glossary(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-glossary",
        "page_title": "Glossary",
        "canonical_url": "/knowledge/glossary/",
    }
    return render(request, "coresite/knowledge/glossary.html", context)


def knowledge_quick_wins(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-quick-wins",
        "page_title": "Quick Wins",
        "canonical_url": "/knowledge/quick-wins/",
    }
    return render(request, "coresite/knowledge/quick_wins.html", context)


_CASE_STUDY_ROBOTS = (
    "index,follow" if settings.CASE_STUDIES_INDEXABLE else "noindex,nofollow"
)


def case_studies(request):
    footer = get_footer_content()
    studies = CaseStudy.objects.filter(is_published=True)
    context = {
        "footer": footer,
        "page_id": "case-studies",
        "page_title": "Case Studies",
        "canonical_url": "/case-studies/",
        "case_studies": studies,
        "meta_robots": _CASE_STUDY_ROBOTS,
    }
    response = render(request, "coresite/case_studies/index.html", context)
    response["X-Robots-Tag"] = _CASE_STUDY_ROBOTS
    return response


case_studies.context_object_name = "case_studies"
case_studies.meta_robots = _CASE_STUDY_ROBOTS


def case_study_detail(request, slug: str):
    preview = request.GET.get("preview") == "1" and request.user.is_staff
    lookup = {"slug": slug}
    if not preview:
        lookup["is_published"] = True
    footer = get_footer_content()
    study = get_object_or_404(CaseStudy, **lookup)
    context = {
        "footer": footer,
        "page_id": "case-study-detail",
        "page_title": study.title,
        "canonical_url": f"/case-studies/{study.slug}/",
        "case_study": study,
        "meta_robots": _CASE_STUDY_ROBOTS,
    }
    response = render(request, "coresite/case_studies/detail.html", context)
    response["X-Robots-Tag"] = _CASE_STUDY_ROBOTS
    return response


case_study_detail.context_object_name = "case_study"
case_study_detail.meta_robots = _CASE_STUDY_ROBOTS


def resources(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/resources.html",
        {
            "footer": footer,
            "page_id": "resources",
            "page_title": "Resources",
            "canonical_url": "/resources/",
        },
    )


def tools(request):
    footer = get_footer_content()
    robots = "index,follow" if settings.TOOLS_INDEXABLE else "noindex,nofollow"
    tools_list = [
        {
            "title": "ROI Calculator",
            "description": "Estimate returns from your AI marketing spend.",
            "url": "/tools/roi-calculator/",
            "slug": "roi-calculator",
        },
        {
            "title": "Content Ideator",
            "description": "Generate growth ideas powered by machine intelligence.",
            "url": "/tools/content-ideator/",
            "slug": "content-ideator",
        },
    ]
    learn_items = [
        {
            "title": "What is AI marketing?",
            "url": "/knowledge/ai-marketing/",
        },
        {
            "title": "How to measure AI ROI",
            "url": "/knowledge/ai-roi/",
        },
    ]
    blog_items = [
        {
            "title": "Launching our ROI tool",
            "url": "/blog/roi-tool/",
        },
        {
            "title": "3 AI tips for Q4",
            "url": "/blog/ai-tips-q4/",
        },
    ]
    context = {
        "footer": footer,
        "page_id": "tools",
        "page_title": "Tools",
        "page_intro": "Short utilities to explore AI for growth.",
        "canonical_url": "/tools/",
        "meta_robots": robots,
        "tools": tools_list,
        "knowledge_items": learn_items,
        "blog_posts": blog_items,
    }
    response = render(
        request,
        "coresite/tools.html",
        context,
    )
    response["X-Robots-Tag"] = robots
    return response


def tool_detail(request, slug: str):
    footer = get_footer_content()
    tool = get_object_or_404(Tool.objects.published(), slug=slug)
    robots = "index,follow" if settings.TOOLS_INDEXABLE else "noindex,nofollow"
    context = {
        "footer": footer,
        "page_id": "tool-detail",
        "page_title": tool.title,
        "tool": tool,
        "tool_slug": tool.slug,
        "canonical_url": f"/tools/{tool.slug}/",
        "meta_robots": robots,
    }
    response = render(request, "coresite/tool_detail.html", context)
    response["X-Robots-Tag"] = robots
    return response


def community(request):
    """Render the community hub with basic filtering and pagination."""
    footer = get_footer_content()
    filter_param = request.GET.get("filter", "latest")
    tag = request.GET.get("tag")
    page_number = int(request.GET.get("page", 1))
    robots = "index,follow"

    error = False
    from django.core.paginator import Paginator, EmptyPage
    try:
        threads = list(THREADS)
        if filter_param == "unanswered":
            threads = [t for t in threads if not t["answered"]]
        if tag:
            threads = [t for t in threads if tag in t["tags"]]
        threads.sort(key=lambda t: t["updated"], reverse=True)
        paginator = Paginator(threads, 10)
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except Exception:
        threads = []
        paginator = Paginator([], 1)
        page_obj = paginator.page(1)
        error = True

    selected_tags = set([tag]) if tag else set()
    if not selected_tags:
        for t in page_obj.object_list:
            selected_tags.update(t["tags"])

    related = {}
    for key, items in RELATED_CONTENT_ITEMS.items():
        filtered = [i for i in items if selected_tags.intersection(i["tags"])]
        if key == "knowledge":
            related[key] = filtered[:2]
        else:
            related[key] = filtered[:1]

    def absolute_page_url(num: int) -> str:
        params = {}
        if num != 1:
            params["page"] = num
        if filter_param != "latest":
            params["filter"] = filter_param
        if tag:
            params["tag"] = tag
        query = f"?{urlencode(params)}" if params else ""
        return f"/community/{query}"

    prev_page = absolute_page_url(page_number - 1) if page_obj.has_previous() else None
    next_page = absolute_page_url(page_number + 1) if page_obj.has_next() else None

    context = {
        "footer": footer,
        "page_id": "community",
        "page_title": "Technofatty Community",
        "meta_title": "Technofatty Community — Questions & Discussions",
        "canonical_url": absolute_page_url(page_number),
        "threads": page_obj.object_list,
        "page_obj": page_obj,
        "filter": filter_param,
        "tag": tag,
        "related_content": related,
        "error": error,
        "meta_robots": robots,
        "prev_page_url": prev_page,
        "next_page_url": next_page,
        "site_base_url": settings.SITE_BASE_URL,
    }
    response = render(request, "coresite/community.html", context)
    response["X-Robots-Tag"] = robots
    return response


def blog(request):
    page_str = request.GET.get("page")
    if page_str == "1":
        return HttpResponsePermanentRedirect(reverse("blog"))

    footer = get_footer_content()
    posts_qs = BlogPost.published.order_by("-published_at")
    posts = list(posts_qs)

    # Basic pagination over in-memory posts to enable proper SEO signals.
    from django.core.paginator import Paginator, EmptyPage

    page_number = int(page_str or 1)
    paginator = Paginator(posts, 4)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        raise Http404

    page_posts = list(page_obj.object_list)
    featured_post = page_posts[0] if page_number == 1 and page_posts else None
    remaining_posts = page_posts[1:] if page_number == 1 else page_posts

    categories = {
        (p.category_slug, p.category_title)
        for p in posts
        if p.category_slug
    }
    tags = {
        (t["slug"], t["title"]) for p in posts for t in p.tags
    }

    def absolute_page_url(num: int) -> str:
        return "/blog/" if num == 1 else f"/blog/?page={num}"

    prev_page = absolute_page_url(page_number - 1) if page_obj.has_previous() else None
    next_page = absolute_page_url(page_number + 1) if page_obj.has_next() else None

    context = {
        "footer": footer,
        "page_id": "blog",
        "page_title": "Blog",
        "featured_post": featured_post,
        "posts": remaining_posts,
        "page_posts": page_posts,
        "categories": [
            {"slug": slug, "title": title} for slug, title in sorted(categories)
        ],
        "tags": [
            {"slug": slug, "title": title} for slug, title in sorted(tags)
        ],
        "next_page_url": next_page,
        "prev_page_url": prev_page,
        "canonical_url": absolute_page_url(page_number),
        "page_number": page_number,
        "total_pages": paginator.num_pages,
    }
    return render(request, "coresite/blog.html", context)


def blog_post(request, post_slug: str):
    footer = get_footer_content()
    post = get_object_or_404(BlogPost.published, slug=post_slug)
    context = {
        "footer": footer,
        "page_id": "post",
        "page_title": post["title"],
        "post": post,
        "canonical_url": f"/blog/{post_slug}/",
    }
    return render(request, "coresite/blog_detail.html", context)


def blog_category(request, category_slug: str):
    footer = get_footer_content()
    posts_qs = BlogPost.published.filter(
        category_slug=category_slug
    ).order_by("-published_at")
    posts = list(posts_qs)
    category_title = (
        posts[0].category_title
        if posts
        else category_slug.replace("-", " ").title()
    )
    context = {
        "footer": footer,
        "page_id": "blog-category",
        "page_title": category_title,
        "posts": posts,
        "next_page_url": "#",
        "prev_page_url": "#",
        "canonical_url": f"/blog/category/{category_slug}/",
    }
    return render(request, "coresite/blog_category.html", context)


def blog_tag(request, tag_slug: str):
    footer = get_footer_content()
    posts = [
        p
        for p in BlogPost.published.all()
        if any(t.get("slug") == tag_slug for t in p.tags)
    ]
    tag_title = tag_slug.replace("-", " ").title()
    context = {
        "footer": footer,
        "page_id": "blog-tag",
        "page_title": tag_title,
        "posts": posts,
        "next_page_url": "#",
        "prev_page_url": "#",
        "canonical_url": f"/blog/tag/{tag_slug}/",
    }
    return render(request, "coresite/blog_tag.html", context)


def blog_rss(request):
    """Return an RSS 2.0 feed of recent blog posts."""
    feed = Rss201rev2Feed(
        title="Technofatty Blog",
        link=f"{settings.SITE_BASE_URL}/blog/",
        description="Latest news and insights from Technofatty.",
    )

    posts = BlogPost.published.order_by("-published_at")[:10]
    for post in posts:
        pubdate = post.published_at
        if pubdate is None:
            pubdate = timezone.now()
        elif timezone.is_naive(pubdate):
            pubdate = timezone.make_aware(pubdate, timezone.utc)
        feed.add_item(
            title=post.title,
            link=f"{settings.SITE_BASE_URL}/blog/{post.slug}/",
            description=post.excerpt,
            unique_id=f"{settings.SITE_BASE_URL}/blog/{post.slug}/",
            pubdate=pubdate,
        )

    if feed.latest_post_date is None:
        feed.latest_post_date = timezone.now()

    rss_content = feed.writeString("utf-8")
    return HttpResponse(
        rss_content, content_type="application/rss+xml; charset=utf-8"
    )

def sitemap_xml(request):
    cache_key = SITEMAP_CACHE_KEY
    xml_content = cache.get(cache_key)
    if xml_content is None:
        urls = list(TOP_LEVEL_URLS)
        posts = BlogPost.published.order_by("-published_at")[:10]
        for post in posts:
            urls.append(
                {
                    "loc": f"{settings.SITE_BASE_URL}/blog/{post.slug}/",
                    "priority": "0.5",
                    "changefreq": "monthly",
                }
            )
        if settings.CASE_STUDIES_INDEXABLE:
            studies = CaseStudy.objects.filter(is_published=True).only("slug", "updated_at")
            for study in studies:
                urls.append(
                    {
                        "loc": f"{settings.SITE_BASE_URL}{study.get_absolute_url()}",
                        "priority": "0.5",
                        "changefreq": "monthly",
                        "lastmod": (study.updated_at or timezone.now()).date().isoformat(),
                    }
                )
        xml_parts = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        for url in urls:
            xml_parts.append("  <url>")
            xml_parts.append(f"    <loc>{url['loc']}</loc>")
            xml_parts.append(f"    <changefreq>{url['changefreq']}</changefreq>")
            if 'lastmod' in url:
                xml_parts.append(f"    <lastmod>{url['lastmod']}</lastmod>")
            xml_parts.append(f"    <priority>{url['priority']}</priority>")
            xml_parts.append("  </url>")
        xml_parts.append("</urlset>")
        xml_content = "\n".join(xml_parts)
        cache.set(cache_key, xml_content, 60 * 60)
    return HttpResponse(
        xml_content, content_type="application/xml; charset=utf-8"
    )


def robots_txt(request):
    host = request.get_host().split(":")[0].lower()
    production_hosts = {"technofatty.com", "www.technofatty.com"}
    if host in production_hosts:
        lines = ["User-agent: *", "Allow: /"]
        if not settings.CASE_STUDIES_INDEXABLE:
            lines.append("Disallow: /case-studies/")
        if not settings.TOOLS_INDEXABLE:
            lines.append("Disallow: /tools/")
        lines.append(f"Sitemap: {settings.SITE_BASE_URL}/sitemap.xml")
    else:
        lines = [
            "User-agent: *",
            "Disallow: /",
        ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def join(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/join.html",
        {
            "footer": footer,
            "page_id": "join",
            "page_title": "Join Free",
            "canonical_url": "/join/",
        },
    )


def about(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/about.html",
        {"footer": footer, "canonical_url": "/about/"},
    )


def contact(request):
    footer = get_footer_content()
    sent = request.GET.get("sent") == "1"
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = {k: v for k, v in form.cleaned_data.items() if k != "website"}
            ip = request.META.get("REMOTE_ADDR", "")
            email = data.get("email", "")
            cache_key = f"contact:{ip}:{email}"
            if cache.get(cache_key):
                contact_event("throttle_hit", {"ip": ip, "email": email})
            else:
                ContactNotifier().send(**data)
                contact_event("submitted_success", {"ip": ip})
                cache.set(cache_key, True, timeout=60)
            return redirect("/contact/?sent=1")
        first_error = next(iter(form.errors))
        form.fields[first_error].widget.attrs["autofocus"] = "autofocus"
    else:
        form = ContactForm()
    return render(
        request,
        "coresite/contact.html",
        {
            "footer": footer,
            "canonical_url": "/contact/",
            "form": form,
            "sent": sent,
        },
    )

def support(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/support.html",
        {"footer": footer, "canonical_url": "/support/"},
    )

def legal(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/legal.html",
        {"footer": footer, "canonical_url": "/legal/"},
    )
