
from rest_framework import viewsets
from django.shortcuts import render

def trait_inference_view(request):
    return render(request, 'traits/trait_inference.html')
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import TraitProfile
from .serializers import TraitProfileSerializer
import numpy as np

class TraitProfileViewSet(viewsets.ModelViewSet):
    queryset = TraitProfile.objects.all()
    serializer_class = TraitProfileSerializer

    @action(detail=False, methods=['post'], url_path='infer', url_name='infer-traits')
    def infer_traits(self, request):
        """
        Context-engineered trait inference endpoint.
        Input: { "session_id": "session_123" }
        Output: trait profile or validation error
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({
                "error": "Missing required field: session_id.",
                "required_fields": ["session_id"],
                "suggestion": "Provide a valid session_id."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Example: Fetch metrics for session (replace with real logic)
        from behavioral_data.models import BehavioralMetric
        metrics = BehavioralMetric.objects.filter(session_id=session_id)
        if not metrics.exists() or metrics.count() < 10:
            return Response({
                "error": "Insufficient data completeness (required: 10 valid events).",
                "required_fields": ["session_id", "event_data"],
                "suggestion": "Ensure session contains at least 10 valid events."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Example trait calculation (replace with scientific logic)
        trait_scores = {
            "risk_tolerance": float(np.random.uniform(0.7, 0.95)),
            "consistency": float(np.random.uniform(0.7, 0.95)),
            "learning": float(np.random.uniform(0.7, 0.95)),
            "decision_speed": float(np.random.uniform(0.6, 0.9)),
            "emotional_regulation": float(np.random.uniform(0.7, 0.95)),
            "confidence_interval": 0.95
        }
        return Response(trait_scores, status=status.HTTP_200_OK)
from rest_framework import viewsets
from .models import TraitProfile, SuccessModel, TraitAssessment, AssessmentValidation
from .serializers import (
    TraitProfileSerializer,
    SuccessModelSerializer,
    TraitAssessmentSerializer,
    AssessmentValidationSerializer
)

class TraitProfileViewSet(viewsets.ModelViewSet):
    queryset = TraitProfile.objects.all()
    serializer_class = TraitProfileSerializer

class SuccessModelViewSet(viewsets.ModelViewSet):
    queryset = SuccessModel.objects.all()
    serializer_class = SuccessModelSerializer

class TraitAssessmentViewSet(viewsets.ModelViewSet):
    queryset = TraitAssessment.objects.all()
    serializer_class = TraitAssessmentSerializer

class AssessmentValidationViewSet(viewsets.ModelViewSet):
    queryset = AssessmentValidation.objects.all()
    serializer_class = AssessmentValidationSerializer
from django.shortcuts import render

# Create your views here.
