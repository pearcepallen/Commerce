from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.item, name="item"),
    path("watchlist", views.watching, name="watching"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"), 
    path("close/<int:id>", views.close, name="close"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category")
]
