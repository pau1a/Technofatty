from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("support/", views.support, name="support"),
    path("signals/<slug:slug>/", views.signal_detail, name="signal_detail"),
    path("community/join/", views.community_join, name="community_join"),
]
