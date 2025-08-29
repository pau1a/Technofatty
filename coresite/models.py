from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
import math


class StatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class SubtypeChoices(models.TextChoices):
    GUIDE = "guide", "Guide"
    GLOSSARY = "glossary", "Glossary"
    SIGNAL = "signal", "Signal"
    QUICK_WIN = "quick_win", "Quick Win"


class PublishedManager(models.Manager):
    """Manager that returns only published items."""

    def get_queryset(self):
        qs = super().get_queryset().filter(status=StatusChoices.PUBLISHED)
        model_fields = {f.name for f in self.model._meta.get_fields()}
        if "published_at" in model_fields:
            now = timezone.now()
            qs = qs.filter(published_at__isnull=False, published_at__lte=now)
        return qs


class ToolQuerySet(models.QuerySet):
    """Custom queryset for Tool with publication helpers."""

    def published(self):
        return self.filter(is_published=True)

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


class KnowledgeTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class KnowledgeArticle(TimestampedModel):
    category = models.ForeignKey(
        KnowledgeCategory, related_name="articles", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        blank=True,
        unique=True,
        help_text="Unique across all knowledge articles for future routing flexibility",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
        db_index=True,
    )
    subtype = models.CharField(
        max_length=20, choices=SubtypeChoices.choices, blank=True
    )
    blurb = models.TextField(blank=True)
    content = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="knowledge_articles",
    )
    reading_time = models.PositiveIntegerField(blank=True, null=True)
    attribution = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(KnowledgeTag, blank=True, related_name="articles")
    image = models.ImageField(upload_to="knowledge/", blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    motif = models.CharField(max_length=100, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image_url = models.URLField(blank=True)
    twitter_title = models.CharField(max_length=255, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image_url = models.URLField(blank=True)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "knowledge_article",
            kwargs={"category_slug": self.category.slug, "article_slug": self.slug},
        )

    def clean(self):
        super().clean()
        if self.image and not self.image_alt:
            raise ValidationError({"image_alt": "Alt text is required when an image is set."})
        if self.status == StatusChoices.PUBLISHED:
            if not self.published_at:
                raise ValidationError({"published_at": "Published articles must have a publish date."})
            if timezone.is_naive(self.published_at):
                raise ValidationError({"published_at": "published_at must be timezone-aware."})

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            qs = self.__class__.objects.exclude(pk=self.pk)
            self.slug = _generate_unique_slug(self.title, qs, fallback="article")
        if not self.blurb and self.content:
            snippet = self.content.strip().split("\n\n", 1)[0]
            self.blurb = snippet
        if self.content:
            words = len(self.content.split())
            self.reading_time = max(1, math.ceil(words / 200)) if words else None
        if self.status == StatusChoices.PUBLISHED:
            original = None
            if self.pk:
                original = self.__class__.objects.filter(pk=self.pk).values("status", "published_at").first()
            if original and original["status"] == StatusChoices.PUBLISHED and original["published_at"]:
                self.published_at = original["published_at"]
            elif self.published_at is None:
                self.published_at = timezone.now()
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["status", "published_at"], name="knart_status_pub_idx"),
            models.Index(fields=["category", "status", "published_at"], name="knart_cat_status_pub_idx"),
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


class Tool(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="tools/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    schema_kind = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    objects = ToolQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = _generate_unique_slug(
                self.title, Tool.objects.exclude(pk=self.pk), fallback="tool"
            )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tool_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("display_order", "title")
        indexes = [
            models.Index(
                fields=["is_published", "display_order"],
                name="tool_pub_order_idx",
            ),
            models.Index(
                fields=["schema_kind"],
                name="tool_schema_idx",
            ),
        ]


class CaseStudy(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="case_studies/", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("case_study_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = _generate_unique_slug(
                self.title, CaseStudy.objects.exclude(pk=self.pk), fallback="case-study"
            )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("display_order", "title")
        indexes = [
            models.Index(
                fields=["is_published", "display_order"],
                name="casestudy_pub_order_idx",
            ),
        ]


def _generate_unique_slug(title: str, queryset, fallback: str = "item"):
    """Return a slug unique within the given queryset."""
    base = slugify(title) or slugify(fallback) or "item"
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
            instance.title, BlogPost.objects.exclude(pk=instance.pk), fallback="blog-post"
        )


SITEMAP_CACHE_KEY = "sitemap_xml"


@receiver(post_save, sender=BlogPost)
@receiver(post_save, sender=CaseStudy)
def clear_sitemap_cache(**kwargs):
    cache.delete(SITEMAP_CACHE_KEY)


class ContactEvent(models.Model):
    """Record a contact-related event.

    This minimal model provides an audit trail for contact interactions
    while keeping the data model simple so that persisting events to an
    external provider in the future would be straightforward.
    """

    event_type = models.CharField(max_length=100)
    meta = models.JSONField(default=dict, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.event_type} @ {self.timestamp}"
