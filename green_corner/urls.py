from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.rgc_form, name='rgc_upload'),
]
