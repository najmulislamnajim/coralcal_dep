from django.urls import path
from core.views import home, login_view, user_logout

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
]