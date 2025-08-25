"""
URL configuration for technofatty_com project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from coresite import views as core_views


class AccountHomeView(LoginRequiredMixin, TemplateView):
    template_name = "coresite/account/account_home.html"
    login_url = reverse_lazy("account_login")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coresite.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('robots.txt', core_views.robots_txt, name="robots_txt"),
    path('sitemap.xml', core_views.sitemap_xml, name="sitemap_xml"),
    path('account/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='account_logout'),
    path('account/', AccountHomeView.as_view(), name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
