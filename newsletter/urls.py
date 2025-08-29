from django.urls import path

from . import views

urlpatterns = [
    path("", views.newsletter_form, name="newsletter_form"),
    path("subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
]
