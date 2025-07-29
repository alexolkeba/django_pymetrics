from rest_framework import serializers
from .models import BehavioralSession, BehavioralEvent, BalloonRiskEvent, MemoryCardsEvent, ReactionTimerEvent, BehavioralMetric

class BehavioralSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralSession
        fields = '__all__'

class BehavioralEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralEvent
        fields = '__all__'

class BalloonRiskEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalloonRiskEvent
        fields = '__all__'

class MemoryCardsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryCardsEvent
        fields = '__all__'

class ReactionTimerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionTimerEvent
        fields = '__all__'

class BehavioralMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralMetric
        fields = '__all__'
