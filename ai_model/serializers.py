from rest_framework import serializers
from .models import TraitProfile, SuccessModel, TraitAssessment, AssessmentValidation

class TraitProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraitProfile
        fields = '__all__'

class SuccessModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessModel
        fields = '__all__'

class TraitAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraitAssessment
        fields = '__all__'

class AssessmentValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentValidation
        fields = '__all__'
