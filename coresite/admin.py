from django.contrib import admin
from .models import SiteSettings, SiteImage, DevImage

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
