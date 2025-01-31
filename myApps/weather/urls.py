from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="weather_home"),
]
