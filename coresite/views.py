from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.feedgenerator import Rss201rev2Feed
from django.db.models import Q
from newsletter.utils import log_newsletter_event
from django.core.cache import cache
from coresite.services.contact import contact_event
from .models import SiteImage, BlogPost, KnowledgeCategory, KnowledgeArticle
from .forms import ContactForm
from .notifiers import ContactNotifier
from datetime import datetime
from .signals import get_signals_content
from .support import get_support_content
from .community import get_community_content
from .footer import get_footer_content


BASE_CANONICAL = "https://technofatty.com"


KNOWLEDGE_SUB_SECTIONS = [
    {"title": "Guides", "url_name": "knowledge_guides"},
    {"title": "Signals", "url_name": "knowledge_signals"},
    {"title": "Glossary", "url_name": "knowledge_glossary"},
    {"title": "Quick Wins", "url_name": "knowledge_quick_wins"},
]

# Legacy endpoints like /services/, /signup/, /community/join/, and /signals/<slug>/
# are intentionally omitted to keep retired paths out of the sitemap.
TOP_LEVEL_URLS = [
    {"loc": f"{BASE_CANONICAL}/", "priority": "1.0", "changefreq": "weekly"},
    {"loc": f"{BASE_CANONICAL}/knowledge/", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{BASE_CANONICAL}/blog/", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{BASE_CANONICAL}/resources/", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{BASE_CANONICAL}/case-studies/", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{BASE_CANONICAL}/community/", "priority": "0.8", "changefreq": "weekly"},
]


def consent_accept(request):
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
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
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
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
        {
            "title": "AI Case Studies",
            "blurb": "See how real businesses turned AI into growth.",
            "url": "/case-studies/",
        },
    ]
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
        "signals": signals,
        "support": support,
        "community": community,
        "footer": footer,
        "canonical_url": f"{BASE_CANONICAL}/",
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
    canonical_url = f"{BASE_CANONICAL}/knowledge/" + (
        f"?{canonical_query}" if canonical_query else ""
    )
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
        "show_cta_strip": has_content,
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
            f"{BASE_CANONICAL}/knowledge/{category_slug}/"
            if num == 1
            else f"{BASE_CANONICAL}/knowledge/{category_slug}/?page={num}"
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
    context = {
        "footer": footer,
        "page_id": f"knowledge-{article_slug}",
        "page_title": article.title,
        "category": category,
        "article": article,
        "canonical_url": f"{BASE_CANONICAL}/knowledge/{category_slug}/{article_slug}/",
        "base_canonical": BASE_CANONICAL,
    }
    return render(request, "coresite/knowledge/article.html", context)


def knowledge_guides(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-guides",
        "page_title": "Guides",
        "canonical_url": f"{BASE_CANONICAL}/knowledge/guides/",
    }
    return render(request, "coresite/knowledge/guides.html", context)


def knowledge_signals(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-signals",
        "page_title": "Signals",
        "canonical_url": f"{BASE_CANONICAL}/knowledge/signals/",
    }
    return render(request, "coresite/knowledge/signals.html", context)


def knowledge_glossary(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-glossary",
        "page_title": "Glossary",
        "canonical_url": f"{BASE_CANONICAL}/knowledge/glossary/",
    }
    return render(request, "coresite/knowledge/glossary.html", context)


def knowledge_quick_wins(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge-quick-wins",
        "page_title": "Quick Wins",
        "canonical_url": f"{BASE_CANONICAL}/knowledge/quick-wins/",
    }
    return render(request, "coresite/knowledge/quick_wins.html", context)


def case_studies_landing(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/case_studies/landing.html",
        {
            "footer": footer,
            "page_id": "case-studies",
            "page_title": "Case Studies",
            "canonical_url": f"{BASE_CANONICAL}/case-studies/",
        },
    )


def case_study_detail(request, slug: str):
    footer = get_footer_content()
    return render(
        request,
        "coresite/case_studies/detail.html",
        {
            "footer": footer,
            "page_id": "case-study-detail",
            "page_title": "Case Study Title",
            "canonical_url": f"{BASE_CANONICAL}/case-studies/{slug}/",
        },
    )


def resources(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/resources.html",
        {
            "footer": footer,
            "page_id": "resources",
            "page_title": "Resources",
            "canonical_url": f"{BASE_CANONICAL}/resources/",
        },
    )


def tools(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/tools.html",
        {
            "footer": footer,
            "page_id": "tools",
            "page_title": "Tools",
            "canonical_url": f"{BASE_CANONICAL}/tools/",
        },
    )


def community(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/community.html",
        {
            "footer": footer,
            "page_id": "community",
            "page_title": "Community",
            "canonical_url": f"{BASE_CANONICAL}/community/",
        },
    )


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
        return f"{BASE_CANONICAL}/blog/" if num == 1 else f"{BASE_CANONICAL}/blog/?page={num}"

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
        "canonical_url": f"{BASE_CANONICAL}/blog/{post_slug}/",
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
        "canonical_url": f"{BASE_CANONICAL}/blog/category/{category_slug}/",
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
        "canonical_url": f"{BASE_CANONICAL}/blog/tag/{tag_slug}/",
    }
    return render(request, "coresite/blog_tag.html", context)


def blog_rss(request):
    """Return an RSS 2.0 feed of recent blog posts."""
    feed = Rss201rev2Feed(
        title="Technofatty Blog",
        link=f"{BASE_CANONICAL}/blog/",
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
            link=f"{BASE_CANONICAL}/blog/{post.slug}/",
            description=post.excerpt,
            unique_id=f"{BASE_CANONICAL}/blog/{post.slug}/",
            pubdate=pubdate,
        )

    if feed.latest_post_date is None:
        feed.latest_post_date = timezone.now()

    rss_content = feed.writeString("utf-8")
    return HttpResponse(
        rss_content, content_type="application/rss+xml; charset=utf-8"
    )


def sitemap_xml(request):
    urls = list(TOP_LEVEL_URLS)
    posts = BlogPost.published.order_by("-published_at")[:10]
    for post in posts:
        urls.append(
            {
                "loc": f"{BASE_CANONICAL}/blog/{post.slug}/",
                "priority": "0.5",
                "changefreq": "monthly",
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
        xml_parts.append(f"    <priority>{url['priority']}</priority>")
        xml_parts.append("  </url>")
    xml_parts.append("</urlset>")
    xml_content = "\n".join(xml_parts)
    return HttpResponse(
        xml_content, content_type="application/xml; charset=utf-8"
    )


def robots_txt(request):
    host = request.get_host().split(":")[0].lower()
    production_hosts = {"technofatty.com", "www.technofatty.com"}
    if host in production_hosts:
        lines = [
            "User-agent: *",
            "Allow: /",
            "Sitemap: https://technofatty.com/sitemap.xml",
        ]
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
            "canonical_url": f"{BASE_CANONICAL}/join/",
        },
    )


def about(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/about.html",
        {"footer": footer, "canonical_url": f"{BASE_CANONICAL}/about/"},
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
            "canonical_url": f"{BASE_CANONICAL}/contact/",
            "form": form,
            "sent": sent,
        },
    )

def support(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/support.html",
        {"footer": footer, "canonical_url": f"{BASE_CANONICAL}/support/"},
    )

def legal(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/legal.html",
        {"footer": footer, "canonical_url": f"{BASE_CANONICAL}/legal/"},
    )
