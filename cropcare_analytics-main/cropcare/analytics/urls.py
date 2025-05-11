from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_view, name='analytics'),
    path('get-sensor-data/', views.get_sensor_data, name='get_sensor_data'),
    path('save-sensor-data/', views.save_sensor_data, name='save_sensor_data'),
    path('get-moisture/', views.get_moisture, name='get_moisture'),
    path('get-temperature/', views.get_temperature, name='get_temperature'),
    path('get-humidity/', views.get_humidity, name='get_humidity'),
    path('get-ph/', views.get_ph, name='get_ph'),
]