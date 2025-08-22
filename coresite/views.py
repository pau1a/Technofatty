from django.shortcuts import render
from newsletter.utils import log_newsletter_event
from .models import SiteImage
from datetime import datetime
from .signals import get_signals_content
from .support import get_support_content
from .community import get_community_content
from .footer import get_footer_content


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
    images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
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


def about(request):
    footer = get_footer_content()
    return render(request, "coresite/about.html", {"footer": footer})


def services(request):
    footer = get_footer_content()
    return render(request, "coresite/services.html", {"footer": footer})


def contact(request):
    footer = get_footer_content()
    return render(request, "coresite/contact.html", {"footer": footer})

def legal(request):
    footer = get_footer_content()
    return render(request, "coresite/legal.html", {"footer": footer})
