from django.urls import path

from wishlists.views import WishListView

urlpatterns = [
    path('', WishListView.as_view()),
    path('/<int:planet_id>', WishListView.as_view()),
]