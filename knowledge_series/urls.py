from django.urls import path
from knowledge_series.views import book_choice, admin, export_wishlist

urlpatterns = [
    path('book', book_choice, name='book_choice'),
    path('admin',admin, name='admin'),
    path('export_wishlist', export_wishlist, name='export_wishlist'),
]