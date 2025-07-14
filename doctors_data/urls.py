from django.urls import path
from . import views

urlpatterns = [
    path('', views.dd_form, name='dd_form'),
]
