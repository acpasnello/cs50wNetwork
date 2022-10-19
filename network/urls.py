
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<int:userid>", views.profile, name="profile"),
    path("like/<int:postid>", views.like, name="like"),
    path("unlike/<int:postid>", views.unlike, name="unlike"),
    path("userlist/<str:desiredlist>", views.userlist, name="userlist")
]
