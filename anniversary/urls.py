from django.urls import path
from . import views

urlpatterns = [
    path('form', views.anniversary, name='anniversary_form'),
    path('edit/<int:anniversary_id>/', views.edit_anniversary, name='edit_anniversary'),
    path('del/<int:anniversary_id>/', views.delete_anniversary, name='delete_anniversary'),
    path('history', views.anniversary_history, name='anniversary_history'),
]
