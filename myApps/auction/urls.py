from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="auction_home"), 
    path("items/<category>", views.items, name="items"), 
    path("item/<item_title>", views.item_page, name="itempage"), 
    path('item/<str:item_title>/end-auction', views.end_auction, name='end_auction'),
    path("login", views.login_page, name="login"),
    path("", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("post-Item", views.post_item, name="postitem"),
    path("api-item", views.api_item, name="apiitem"),
    path("MyItems", views.user_items, name="useritems"),
    path("about", views.about_page, name="about"),
]
