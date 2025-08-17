from django.shortcuts import render
from .models import SiteImage


def homepage(request):
    images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
    context = {"site_images": images}
    return render(request, "coresite/homepage.html", context)
