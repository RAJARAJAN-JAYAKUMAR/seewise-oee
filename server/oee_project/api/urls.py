from django.urls import path
from .views.machine_views import machine_list_create
from .views.productionlog_views import productionlog_list_create
from .views.oee_views import machine_oee

urlpatterns = [
    path('machines/', machine_list_create, name='machine-list-create'),
    path('logs/', productionlog_list_create, name='log-list-create'),
    path('oee/', machine_oee, name='machine_oee'),
    path('oee/<int:machine_id>/', machine_oee, name='machine_oee_detail'),
    path('oee/<int:machine_id>/<str:start_date>/<str:end_date>/', machine_oee, name='machine_oee_filter'),
]
