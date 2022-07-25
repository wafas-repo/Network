
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like_post"),
    path("<str:username>", views.profile, name="profile"),
    path("<int:user_id>/followers/add", views.add_follower, name="add_follower"),
    path("<int:user_id>/followers/remove", views.remove_follower, name="remove_follower")
]
