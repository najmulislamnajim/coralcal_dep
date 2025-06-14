from django.urls import path
from dep_admin import views

urlpatterns = [
    path('', views.index, name='index'),
    path('knowledge_series/', views.knowledge_series, name='knowledge_series'),
    path('export_knowledge_series/', views.export_knowledge_series, name='export_knowledge_series'),
]
