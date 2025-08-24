import re

from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("knowledge/", views.knowledge, name="knowledge"),
    path("knowledge/guides/", views.knowledge_guides, name="knowledge_guides"),
    path("knowledge/signals/", views.knowledge_signals, name="knowledge_signals"),
    path("knowledge/glossary/", views.knowledge_glossary, name="knowledge_glossary"),
    path("knowledge/quick-wins/", views.knowledge_quick_wins, name="knowledge_quick_wins"),
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
    path("case-studies/", views.case_studies_landing, name="case_studies_landing"),
    path(
        "case-studies/<slug:slug>/",
        views.case_study_detail,
        name="case_study_detail",
    ),
    path("resources/", views.resources, name="resources"),
    path("tools/", views.tools, name="tools"),
    path("community/", views.community, name="community"),
    path("blog/", views.blog, name="blog"),
    path("blog/rss/", views.blog_rss, name="blog_rss"),
    path("blog/category/<slug:category_slug>/", views.blog_category, name="blog_category"),
    path("blog/tag/<slug:tag_slug>/", views.blog_tag, name="blog_tag"),
    path("blog/<slug:post_slug>/", views.blog_post, name="blog_post"),
    path("join/", views.join, name="join"),
    re_path(
        re.compile(r"^signup/?$", re.IGNORECASE),
        views.legacy_signup,
        name="legacy_signup",
    ),
    path("account/", views.account, name="account"),
    path("about/", views.about, name="about"),
    re_path(
        re.compile(r"^services/?$", re.IGNORECASE),
        views.legacy_services,
        name="legacy_services",
    ),
    path("contact/", views.contact, name="contact"),
    path("support/", views.support, name="support"),
    path("legal/", views.legal, name="legal"),
    re_path(
        re.compile(r"^signals/(?P<slug>[^/]+)/?$", re.IGNORECASE),
        views.legacy_signal,
        name="legacy_signal",
    ),
    re_path(
        re.compile(r"^community/join/?$", re.IGNORECASE),
        views.legacy_community_join,
        name="legacy_community_join",
    ),
]
