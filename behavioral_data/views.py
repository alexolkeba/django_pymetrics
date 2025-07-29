from rest_framework import viewsets
from .models import BehavioralSession, BehavioralEvent, BalloonRiskEvent, MemoryCardsEvent, ReactionTimerEvent, BehavioralMetric
from .serializers import (
    BehavioralSessionSerializer,
    BehavioralEventSerializer,
    BalloonRiskEventSerializer,
    MemoryCardsEventSerializer,
    ReactionTimerEventSerializer,
    BehavioralMetricSerializer
)

class BehavioralSessionViewSet(viewsets.ModelViewSet):
    queryset = BehavioralSession.objects.all()
    serializer_class = BehavioralSessionSerializer

class BehavioralEventViewSet(viewsets.ModelViewSet):
    queryset = BehavioralEvent.objects.all()
    serializer_class = BehavioralEventSerializer

class BalloonRiskEventViewSet(viewsets.ModelViewSet):
    queryset = BalloonRiskEvent.objects.all()
    serializer_class = BalloonRiskEventSerializer

class MemoryCardsEventViewSet(viewsets.ModelViewSet):
    queryset = MemoryCardsEvent.objects.all()
    serializer_class = MemoryCardsEventSerializer

class ReactionTimerEventViewSet(viewsets.ModelViewSet):
    queryset = ReactionTimerEvent.objects.all()
    serializer_class = ReactionTimerEventSerializer

class BehavioralMetricViewSet(viewsets.ModelViewSet):
    queryset = BehavioralMetric.objects.all()
    serializer_class = BehavioralMetricSerializer
