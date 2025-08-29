from django.contrib import admin
from django import forms
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    SiteSettings,
    SiteImage,
    DevImage,
    KnowledgeCategory,
    KnowledgeArticle,
    KnowledgeTag,
    BlogPost,
    Tool,
    ContactEvent,
    StatusChoices,
)
from django_ckeditor_5.widgets import CKEditor5Widget


class KnowledgeArticleAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name="default"), required=False
    )

    class Meta:
        model = KnowledgeArticle
        fields = "__all__"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hero_image')
    # Optional: add search/filter if SiteSettings grows
    search_fields = ('__str__',)
    list_per_page = 20


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    list_per_page = 20


@admin.register(DevImage)
class DevImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'uploaded_at')
    search_fields = ('title',)
    list_per_page = 20
    ordering = ('-uploaded_at',)
    # This lets you preview uploaded images right in the list view
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 60px;" />'
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Preview'


@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "status")
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    form = KnowledgeArticleAdminForm
    list_display = ("title", "category", "status", "published_at", "preview_link")
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview_link",)
    filter_horizontal = ("tags",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "status",
                    "published_at",
                    "subtype",
                    "blurb",
                    "content",
                )
            },
        ),
        ("Media", {"fields": ("image", "image_alt", "motif")}),
        ("Tags", {"fields": ("tags",)}),
        (
            "Metadata",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "canonical_url",
                    "og_title",
                    "og_description",
                    "og_image_url",
                    "twitter_title",
                    "twitter_description",
                    "twitter_image_url",
                )
            },
        ),
    )
    actions = ["make_published", "make_archived"]

    def preview_link(self, obj):
        if not obj.pk:
            return ""
        url = obj.get_absolute_url()
        return format_html('<a href="{}?preview=1" target="_blank">Preview</a>', url)

    preview_link.short_description = "Preview"

    def make_published(self, request, queryset):
        for obj in queryset:
            obj.status = StatusChoices.PUBLISHED
            if not obj.published_at:
                obj.published_at = timezone.now()
            obj.save()
        self.message_user(request, "Selected articles published.")

    make_published.short_description = "Mark selected articles as published"

    def make_archived(self, request, queryset):
        updated = queryset.update(status=StatusChoices.ARCHIVED)
        self.message_user(request, f"{updated} articles archived.")

    make_archived.short_description = "Archive selected articles"


@admin.register(KnowledgeTag)
class KnowledgeTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at")
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    def thumb(self, obj):
        return (
            format_html('<img src="{}" style="height:32px;">', obj.image.url)
            if obj.image
            else ""
        )

    thumb.short_description = "Image"

    list_display = (
        "title",
        "thumb",
        "schema_kind",
        "is_published",
        "is_premium",
        "display_order",
    )
    list_editable = ("display_order", "is_published", "is_premium")
    list_filter = ("is_published", "is_premium", "schema_kind")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactEvent)
class ContactEventAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "event_type", "ip_hash")
    list_filter = ("event_type",)
    search_fields = ("event_type", "ip_hash")
    readonly_fields = ("timestamp", "event_type", "meta", "ip_hash")
    ordering = ("-timestamp",)
