from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData
import json

def analytics_view(request):
    return render(request, 'analytics.html')

def get_sensor_data(request):
    # Get latest sensor data or create mock data
    try:
        latest = SensorData.objects.latest('timestamp')
        data = {
            'temperature': {'value': latest.temperature, 'condition': latest.temperature_status},
            'humidity': {'value': latest.humidity, 'condition': latest.humidity_status},
            'moisture': {'value': latest.moisture, 'condition': latest.moisture_status},
            'ph_level': {'value': latest.ph_level, 'condition': latest.ph_status}
        }
    except SensorData.DoesNotExist:
        data = {
            'temperature': {'value': "-", 'condition': "OFF"},
            'humidity': {'value': "-", 'condition': "OFF"},
            'moisture': {'value': "-", 'condition': "OFF"},
            'ph_level': {'value': "-", 'condition': "OFF"}
        }
    return JsonResponse(data)

def save_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            SensorData.objects.create(
                temperature=data.get('temperature'),
                humidity=data.get('humidity'),
                moisture=data.get('moisture'),
                ph_level=data.get('ph_level'),
                temperature_status=data.get('temperature_status'),
                humidity_status=data.get('humidity_status'),
                moisture_status=data.get('moisture_status'),
                ph_status=data.get('ph_status')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})