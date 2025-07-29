"""
Professional Example: Behavioral Event Logging for Django Pymetrics

This example demonstrates best practices for event logging models, serializers, and API endpoints in a neuroscience-based Django application. Use this as a reference for implementing granular behavioral data collection and analysis.
"""

from django.db import models
from django.contrib.auth import get_user_model

class GameSession(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session_id = models.CharField(max_length=64, unique=True)
    device_info = models.JSONField()
    session_start_time = models.DateTimeField()
    session_end_time = models.DateTimeField(null=True, blank=True)

class BalloonEvent(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    balloon_id = models.CharField(max_length=64)
    balloon_index = models.IntegerField()
    color = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    outcome = models.CharField(max_length=16)

class PumpEvent(models.Model):
    balloon = models.ForeignKey(BalloonEvent, on_delete=models.CASCADE)
    pump_number = models.IntegerField()
    timestamp = models.DateTimeField()
    time_since_prev_pump = models.FloatField()
    balloon_size = models.FloatField()
    current_earnings = models.FloatField()
    total_earnings = models.FloatField()

from rest_framework import serializers

class PumpEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PumpEvent
        fields = '__all__'

from rest_framework import viewsets

class PumpEventViewSet(viewsets.ModelViewSet):
    queryset = PumpEvent.objects.all()
    serializer_class = PumpEventSerializer

# Documentation
# - Django documentation: https://docs.djangoproject.com/
# - Django REST Framework: https://www.django-rest-framework.org/
# - See django_pymetrics/Pymetrics Application Research.md for scientific context
