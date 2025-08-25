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
from coresite.auth_views import SignupView, ActivateView


class AccountHomeView(LoginRequiredMixin, TemplateView):
    template_name = "coresite/account/account_home.html"
    login_url = reverse_lazy("account_login")


account_patterns = [
    path("", AccountHomeView.as_view(), name="account"),
    path("login/", auth_views.LoginView.as_view(), name="account_login"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coresite.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('robots.txt', core_views.robots_txt, name="robots_txt"),
    path('sitemap.xml', core_views.sitemap_xml, name="sitemap_xml"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', include(account_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
