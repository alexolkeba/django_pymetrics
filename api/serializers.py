from rest_framework import serializers
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile

class BehavioralSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralSession
        fields = '__all__'

class BehavioralEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralEvent
        fields = '__all__'

class BehavioralMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralMetric
        fields = '__all__'

class TraitProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraitProfile
        fields = '__all__'
