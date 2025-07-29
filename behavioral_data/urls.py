from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BehavioralSessionViewSet,
    BehavioralEventViewSet,
    BalloonRiskEventViewSet,
    MemoryCardsEventViewSet,
    ReactionTimerEventViewSet,
    BehavioralMetricViewSet
)

router = DefaultRouter()
router.register(r'sessions', BehavioralSessionViewSet)
router.register(r'events', BehavioralEventViewSet)
router.register(r'balloon-risk-events', BalloonRiskEventViewSet)
router.register(r'memory-cards-events', MemoryCardsEventViewSet)
router.register(r'reaction-timer-events', ReactionTimerEventViewSet)
router.register(r'metrics', BehavioralMetricViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
