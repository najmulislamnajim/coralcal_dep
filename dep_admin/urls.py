from django.urls import path
from dep_admin import views

urlpatterns = [
    path('', views.index, name='index'),
    path('knowledge_series/', views.knowledge_series, name='knowledge_series'),
    path('export_knowledge_series/', views.export_knowledge_series, name='export_knowledge_series'),
    path('delete_knowledge_series/<int:id>/', views.delete_knowledge_series_data, name='delete_knowledge_series'),
    path('download_gift_catalogs', views.download_gift_catalogs, name='download_gift_catalogs'),
    path('export_gift_catalogs', views.export_gift_catalogs, name='export_gift_catalogs'),
    path('gift_catalogs/', views.gift_catalogs, name='gift_catalogs'),
    path('anniversary', views.anniversary, name='anniversary'),
]
