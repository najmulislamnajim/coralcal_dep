from django.urls import path
from .views import gift_choice, view_gift_catalogs, delete_gift_catalog, edit_gift_catalog

urlpatterns = [
    path('choice', gift_choice, name='gift_choice'),
    path('choiced', view_gift_catalogs, name='gift_choiced'),
    path('delete_gift/<int:id>/', delete_gift_catalog, name='delete_gift_catalog'),
    path('edit_gift/<int:id>', edit_gift_catalog, name='edit_gift_catalog'),
]