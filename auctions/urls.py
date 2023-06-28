from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/wishlist", views.wishlist_add, name="wishlist_add"),
    path("wishlist", views.wishlist_view, name="wishlist_view"),
    path("<int:listing_id>/wishlist_delete", views.wishlist_delete, name="wishlist_delete"),
    path("<int:listing_id>/new_comment", views.new_comment, name="new_comment")
]
