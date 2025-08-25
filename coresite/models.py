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


STATUS_CHOICES = [
    ("draft", "Draft"),
    ("published", "Published"),
]


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class KnowledgeCategory(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class KnowledgeArticle(TimestampedModel):
    category = models.ForeignKey(
        KnowledgeCategory, related_name="articles", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    blurb = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    category_slug = models.SlugField(max_length=100, blank=True)
    category_title = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
