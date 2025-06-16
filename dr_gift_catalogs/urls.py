from django.urls import path
from .views import gift_choice, view_gift_catalogs

urlpatterns = [
    path('choice', gift_choice, name='gift_choice'),
    path('choiced', view_gift_catalogs, name='gift_choiced')
]