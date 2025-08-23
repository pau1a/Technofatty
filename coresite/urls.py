from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("knowledge/", views.knowledge, name="knowledge"),
    path(
        "knowledge/<slug:category_slug>/<slug:article_slug>/",
        views.knowledge_article,
        name="knowledge_article",
    ),
    path(
        "knowledge/<slug:category_slug>/",
        views.knowledge_category,
        name="knowledge_category",
    ),
    path("case-studies/", views.case_studies, name="case_studies"),
    path("resources/", views.resources, name="resources"),
    path("tools/", views.tools, name="tools"),
    path("community/", views.community, name="community"),
    path("blog/", views.blog, name="blog"),
    path("join/", views.join, name="join"),
    path("signup/", views.signup, name="signup"),
    path("account/", views.account, name="account"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("support/", views.support, name="support"),
    path("legal/", views.legal, name="legal"),
    path("signals/<slug:slug>/", views.signal_detail, name="signal_detail"),
    path("community/join/", views.community_join, name="community_join"),
]
