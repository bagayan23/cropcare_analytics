from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_view, name='analytics'),
    path('get-sensor-data/', views.get_sensor_data, name='get_sensor_data'),
    path('save-sensor-data/', views.save_sensor_data, name='save_sensor_data'),
]