import os
import time  # Import time for timestamp comparison
from django.http import JsonResponse
from django.shortcuts import render
from .models import SensorData
import json
import requests

def analytics_view(request):
    return render(request, 'analytics.html')

def get_sensor_data(request):
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


def analytics_view(request):
    return render(request, 'analytics.html')

# Function to fetch moisture data from the PHP file
def get_moisture(request):
    return fetch_data_from_php('http://127.0.0.1:8000/static/php/getMoisture.php')

# Function to fetch temperature data from the PHP file
def get_temperature(request):
    return fetch_data_from_php('http://127.0.0.1:8000/static/php/getTemp.php')

# Function to fetch humidity data from the PHP file
def get_humidity(request):
    return fetch_data_from_php('http://127.0.0.1:8000/static/php/getHumidity.php')

# Function to fetch pH data from the PHP file
def get_ph(request):
    return fetch_data_from_php('http://127.0.0.1:8000/static/php/getPh.php')

# Helper function to fetch data from a PHP file
def fetch_data_from_php(php_url):
    try:
        response = requests.get(php_url)
        if response.status_code == 200:
            return JsonResponse({'value': response.text.strip()})
        else:
            return JsonResponse({'value': '-', 'error': f'Failed to fetch data from {php_url}'}, status=500)
    except requests.RequestException as e:
        return JsonResponse({'value': '-', 'error': str(e)}, status=500)