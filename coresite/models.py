from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class StatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    PUBLISHED = "published", "Published"


class PublishedManager(models.Manager):
    """Manager that returns only published items."""

    def get_queryset(self):
        return super().get_queryset().filter(status=StatusChoices.PUBLISHED)

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


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class KnowledgeCategory(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    description = models.TextField(blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title


class KnowledgeArticle(TimestampedModel):
    category = models.ForeignKey(
        KnowledgeCategory, related_name="articles", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    blurb = models.TextField(blank=True)
    content = models.TextField(blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "slug"],
                name="unique_article_slug_per_category",
            )
        ]


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    category_slug = models.SlugField(max_length=100, blank=True)
    category_title = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title


def _generate_unique_slug(title: str, queryset):
    """Return a slug unique within the given queryset."""
    base = slugify(title)
    slug = base
    counter = 1
    while queryset.filter(slug=slug).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


@receiver(pre_save, sender=BlogPost)
def set_blogpost_slug(sender, instance, **kwargs):
    if not instance.slug and instance.title:
        instance.slug = _generate_unique_slug(
            instance.title, BlogPost.objects.exclude(pk=instance.pk)
        )


@receiver(pre_save, sender=KnowledgeArticle)
def set_knowledge_article_slug(sender, instance, **kwargs):
    if not instance.slug and instance.title:
        qs = KnowledgeArticle.objects.filter(category=instance.category).exclude(
            pk=instance.pk
        )
        instance.slug = _generate_unique_slug(instance.title, qs)


class ContactEvent(models.Model):
    event_type = models.CharField(max_length=100)
    meta = models.JSONField(default=dict, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.event_type} @ {self.timestamp}"
