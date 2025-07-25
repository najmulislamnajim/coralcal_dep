from django.urls import path
from . import views

urlpatterns = [
    path('form',views.do_form_view, name='do_form'),
    path('history', views.do_history, name='do_history'),
    path('edit/<int:pk>/', views.do_edit_view, name='do_edit'),
    path('delete/<int:pk>/', views.do_delete_view, name='do_delete'),
]
