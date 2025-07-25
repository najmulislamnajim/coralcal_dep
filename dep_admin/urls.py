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
    path('export_anniversary', views.export_anniversary, name='export_anniversary'),
    path('download_anniversary', views.download_anniverysary, name='download_anniversary'),
    path('rgc', views.green_corner, name='rgc'),
    path('export_rgc', views.export_rgc, name='export_rgc'),
    path('access_control', views.access_control_view, name='access_control'),
    path('dop', views.doctors_opinion_view, name='dop'),
    path('dop_export', views.dop_export, name='dop_export'),
    path('doctors_data', views.doctors_data, name='doctors_data'),
    path('doctors_data_export', views.doctors_data_export, name='doctors_data_export'),
]
