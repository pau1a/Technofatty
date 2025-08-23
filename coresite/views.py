from django.http import Http404
from django.shortcuts import render
from newsletter.utils import log_newsletter_event
from .models import SiteImage
from datetime import datetime
from .signals import get_signals_content
from .support import get_support_content
from .community import get_community_content
from .footer import get_footer_content


BASE_CANONICAL = "https://technofatty.com"


KNOWLEDGE_CATEGORIES = [
    {"title": "AI Basics", "slug": "ai-basics"},
    {"title": "Data Strategy", "slug": "data-strategy"},
    {"title": "Automation", "slug": "automation"},
]

KNOWLEDGE_ARTICLES = {
    "ai-basics": [
        {
            "title": "What Is AI?",
            "slug": "what-is-ai",
            "blurb": "A quick introduction to artificial intelligence.",
        },
        {
            "title": "History of AI",
            "slug": "history-of-ai",
            "blurb": "From early concepts to modern breakthroughs.",
        },
        {
            "title": "Future of AI",
            "slug": "future-of-ai",
            "blurb": "Where the technology may be heading next.",
        },
    ]
}


KNOWLEDGE_SUB_SECTIONS = [
    {"title": "Guides", "url_name": "knowledge_guides"},
    {"title": "Signals", "url_name": "knowledge_signals"},
    {"title": "Glossary", "url_name": "knowledge_glossary"},
    {"title": "Quick Wins", "url_name": "knowledge_quick_wins"},
]


BLOG_POSTS = [
    {
        "title": "Getting Started with Our Blog",
        "slug": "getting-started",
        "date": datetime(2024, 1, 1),
        "category": {"title": "News", "slug": "news"},
        "tags": [
            {"title": "intro", "slug": "intro"},
            {"title": "welcome", "slug": "welcome"},
        ],
        "excerpt": "A brief welcome to the Technofatty blog.",
    },
    {
        "title": "AI Trends in 2024",
        "slug": "ai-trends-2024",
        "date": datetime(2024, 2, 15),
        "category": {"title": "Insights", "slug": "insights"},
        "tags": [
            {"title": "ai", "slug": "ai"},
            {"title": "trends", "slug": "trends"},
        ],
        "excerpt": "A snapshot of the AI developments we're watching this year.",
    },
    {
        "title": "Behind the Scenes: Data Tips",
        "slug": "data-tips",
        "date": datetime(2024, 3, 10),
        "category": {"title": "Guides", "slug": "guides"},
        "tags": [
            {"title": "data", "slug": "data"},
            {"title": "tips", "slug": "tips"},
        ],
        "excerpt": "Practical data pointers from our team.",
    },
    {
        "title": "Automation Stories",
        "slug": "automation-stories",
        "date": datetime(2024, 4, 5),
        "category": {"title": "Stories", "slug": "stories"},
        "tags": [
            {"title": "automation", "slug": "automation"},
            {"title": "cases", "slug": "cases"},
        ],
        "excerpt": "How small automations make a big impact.",
    },
    {
        "title": "Community Highlights",
        "slug": "community-highlights",
        "date": datetime(2024, 5, 20),
        "category": {"title": "Community", "slug": "community"},
        "tags": [
            {"title": "community", "slug": "community"},
            {"title": "update", "slug": "update"},
        ],
        "excerpt": "Recent happenings around the Technofatty community.",
    },
]


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


def community_join(request):
    """
    Lightweight landing stub for the Community primary CTA.
    Keeps everything server-rendered and accessible. No JS dependence.
    """
    footer = get_footer_content()
    return render(request, "coresite/community_join.html", {"footer": footer})


def knowledge(request):
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "knowledge",
        "page_title": "Knowledge",
        "categories": KNOWLEDGE_CATEGORIES,
        "sub_sections": KNOWLEDGE_SUB_SECTIONS,
        "canonical_url": f"{BASE_CANONICAL}/knowledge/",
    }
    return render(request, "coresite/knowledge/hub.html", context)


def knowledge_category(request, category_slug: str):
    footer = get_footer_content()
    category = next(
        (c for c in KNOWLEDGE_CATEGORIES if c["slug"] == category_slug), None
    )
    if not category:
        raise Http404
    articles = KNOWLEDGE_ARTICLES.get(category_slug, [])
    context = {
        "footer": footer,
        "page_id": f"knowledge-{category_slug}",
        "page_title": category["title"],
        "category": category,
        "articles": articles,
        "canonical_url": f"{BASE_CANONICAL}/knowledge/{category_slug}/",
    }
    return render(request, "coresite/knowledge/category.html", context)


def knowledge_article(request, category_slug: str, article_slug: str):
    footer = get_footer_content()
    category = next(
        (c for c in KNOWLEDGE_CATEGORIES if c["slug"] == category_slug), None
    )
    if not category:
        raise Http404
    article = next(
        (
            a
            for a in KNOWLEDGE_ARTICLES.get(category_slug, [])
            if a["slug"] == article_slug
        ),
        None,
    )
    if not article:
        raise Http404
    context = {
        "footer": footer,
        "page_id": f"knowledge-{article_slug}",
        "page_title": article["title"],
        "category": category,
        "article": article,
        "canonical_url": f"{BASE_CANONICAL}/knowledge/{category_slug}/{article_slug}/",
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
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "blog",
        "page_title": "Blog",
        "posts": BLOG_POSTS,
        "next_page_url": "#",
        "prev_page_url": "#",
        "canonical_url": f"{BASE_CANONICAL}/blog/",
    }
    return render(request, "coresite/blog.html", context)


def blog_post(request, post_slug: str):
    footer = get_footer_content()
    post = next((p for p in BLOG_POSTS if p["slug"] == post_slug), None)
    if not post:
        raise Http404
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
    posts = [p for p in BLOG_POSTS if p["category"]["slug"] == category_slug]
    category_title = next(
        (p["category"]["title"] for p in BLOG_POSTS if p["category"]["slug"] == category_slug),
        category_slug.replace("-", " ").title(),
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
    posts = [p for p in BLOG_POSTS if any(t["slug"] == tag_slug for t in p["tags"])]
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
    footer = get_footer_content()
    context = {
        "footer": footer,
        "page_id": "blog-rss",
        "page_title": "Blog RSS",
        "canonical_url": f"{BASE_CANONICAL}/blog/rss/",
    }
    return render(request, "coresite/blog_rss.html", context)


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


def signup(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/signup.html",
        {
            "footer": footer,
            "page_id": "signup",
            "page_title": "Sign Up",
            "canonical_url": f"{BASE_CANONICAL}/signup/",
        },
    )


def account(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/account.html",
        {
            "footer": footer,
            "page_id": "account",
            "page_title": "Account",
            "canonical_url": f"{BASE_CANONICAL}/account/",
        },
    )


def about(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/about.html",
        {"footer": footer, "canonical_url": f"{BASE_CANONICAL}/about/"},
    )


def services(request):
    footer = get_footer_content()
    return render(request, "coresite/services.html", {"footer": footer})


def contact(request):
    footer = get_footer_content()
    return render(
        request,
        "coresite/contact.html",
        {"footer": footer, "canonical_url": f"{BASE_CANONICAL}/contact/"},
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
