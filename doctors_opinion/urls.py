from django.urls import path
from . import views

urlpatterns = [
    path('form',views.do_form_view, name='do_form_view'),
]
