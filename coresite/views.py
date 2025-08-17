from django.shortcuts import render
from .models import SiteImage
from datetime import datetime


def homepage(request):
    images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
    context = {"site_images": images, "is_homepage": True, "now": datetime.now()}
    return render(request, "coresite/homepage.html", context)
