from django.urls import path
from . import views

app_name = 'coresite'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
]