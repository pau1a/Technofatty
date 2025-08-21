from django.shortcuts import render
from newsletter.utils import log_newsletter_event
from .models import SiteImage
from datetime import datetime


def homepage(request):
    resources = [
        {"title": "AI for Marketing", "blurb": "Boost campaigns with smarter targeting and automation.", "url": "/resources/marketing/"},
        {"title": "AI in Operations", "blurb": "Cut waste and streamline workflows with predictive AI.", "url": "/resources/operations/"},
        {"title": "AI Case Studies", "blurb": "See how real businesses turned AI into growth.", "url": "/case-studies/"},
    ]
    images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
    context = {"site_images": images, "is_homepage": True, "now": datetime.now(), "resources": resources}
    log_newsletter_event(request, "newsletter_block_view")
    return render(request, "coresite/homepage.html", context)
