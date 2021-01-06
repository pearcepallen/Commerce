from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:id>", views.item, name="item"), #add listing
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"), #check if we can do without this path
    path("close/<int:id>", views.close, name="close")
]
