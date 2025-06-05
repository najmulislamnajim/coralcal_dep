from django.urls import path
from core.views import home, login_view, user_logout, territory_home

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', territory_home, name='territory_home'),
]