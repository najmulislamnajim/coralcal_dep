from django.urls import path
from .views import gift_choice

urlpatterns = [
    path('choice', gift_choice, name='gift_choice'),
]