from django.db import models

class SiteSettings(models.Model):
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)  # <-- New field
    hero_alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class SiteImage(models.Model):
    key = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Unique identifier, e.g. 'hero-bg', 'footer-logo', 'team-photo-1'."
    )
    alt_text = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="site_images/", blank=True, null=True)
    video = models.FileField(upload_to="site_videos/", blank=True, null=True)  # <-- New field

    def __str__(self):
        return self.key


class DevImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='dev_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"
# ----- Subscriber model (added to match migration 0004_subscriber.py) -----
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=200, blank=True)
    consent = models.BooleanField(default=False)
    mailchimp_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.email
# -------------------------------------------------------------------------
