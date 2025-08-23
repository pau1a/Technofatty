"""
URL configuration for technofatty_com project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from coresite import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coresite.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('robots.txt', core_views.robots_txt, name="robots_txt"),
    path('sitemap.xml', core_views.sitemap_xml, name="sitemap_xml"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
