from django.urls import path
from . import views

urlpatterns = [
    path('', views.dd_form, name='dd_form'),
    path('delete/<int:doctor_id>', views.delete_doctors_data, name='delete_doctors_data'),
    path('edit/<int:doctor_id>', views.edit_doctors_data, name='edit_doctors_data'),
]
