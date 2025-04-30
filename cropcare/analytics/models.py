from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    moisture = models.FloatField(null=True, blank=True)
    ph_level = models.FloatField(null=True, blank=True)
    temperature_status = models.CharField(max_length=20, blank=True)
    humidity_status = models.CharField(max_length=20, blank=True)
    moisture_status = models.CharField(max_length=20, blank=True)
    ph_status = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-timestamp']