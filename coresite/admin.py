from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, SiteImage, DevImage, Subscriber

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
    list_display = ('id', 'title', 'image_tag', 'uploaded_at')
    search_fields = ('title',)
    list_per_page = 20
    ordering = ('-uploaded_at',)

    @admin.display(description='Preview')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.image.url)
        return ""


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'mailchimp_status', 'consent', 'created_at', 'ip_address')
    list_filter = ('mailchimp_status', 'consent', 'created_at')
    search_fields = ('email', 'name', 'company', 'ip_address')
    ordering = ('-created_at',)
