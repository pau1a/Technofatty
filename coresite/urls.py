from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('signals/<slug:slug>/', views.signal_detail, name='signal_detail'),
    path('community/join/', views.community_join, name='community_join'),
]
