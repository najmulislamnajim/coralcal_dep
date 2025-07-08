from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.rgc_form, name='rgc_upload'),
    path('edit/<str:instance_id>', views.rgc_edit_view, name='rgc_edit'),
]
