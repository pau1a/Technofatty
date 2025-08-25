import re

from django.urls import path, re_path
from . import views
from .feeds import (
    BlogAtomFeed,
    BlogRSSFeed,
    KnowledgeAtomFeed,
    KnowledgeRSSFeed,
    blog_json_feed,
    knowledge_json_feed,
)

urlpatterns = [
    path("", views.homepage, name="home"),
    path("consent/accept/", views.consent_accept, name="consent_accept"),
    path("consent/decline/", views.consent_decline, name="consent_decline"),
    path("knowledge/", views.knowledge, name="knowledge"),
    path("knowledge/rss/", KnowledgeRSSFeed(), name="knowledge_rss"),
    path("knowledge/atom/", KnowledgeAtomFeed(), name="knowledge_atom"),
    path("knowledge/json/", knowledge_json_feed, name="knowledge_json"),
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
    path("blog/rss/", BlogRSSFeed(), name="blog_rss"),
    path("blog/atom/", BlogAtomFeed(), name="blog_atom"),
    path("blog/json/", blog_json_feed, name="blog_json"),
    path("blog/category/<slug:category_slug>/", views.blog_category, name="blog_category"),
    path("blog/tag/<slug:tag_slug>/", views.blog_tag, name="blog_tag"),
    path("blog/<slug:post_slug>/", views.blog_post, name="blog_post"),
    path("join/", views.join, name="join"),
    re_path(
        re.compile(r"^signup/?$", re.IGNORECASE),
        views.legacy_signup,
        name="legacy_signup",
    ),
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
