from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logged_in, name="login"),
    path("signout", views.sign_out, name="signout"),
    path("playlists", views.playlist_page, name="playlists")
]
