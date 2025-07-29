from rest_framework.routers import DefaultRouter
from .views import BehavioralSessionViewSet, BehavioralEventViewSet, BehavioralMetricViewSet, TraitProfileViewSet, MetricExtractionViewSet, ReportGenerationViewSet, TraitInferenceAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'sessions', BehavioralSessionViewSet)
router.register(r'events', BehavioralEventViewSet)
router.register(r'metrics', BehavioralMetricViewSet)
router.register(r'trait-profiles', TraitProfileViewSet)
router.register(r'metric-extraction', MetricExtractionViewSet, basename='metric-extraction')
router.register(r'report-generation', ReportGenerationViewSet, basename='report-generation')

urlpatterns = [
    path('', include(router.urls)),
    # Context-engineered trait inference endpoint
    path('traits/trait-profiles/', TraitInferenceAPIView.as_view(), name='trait-inference'),
]
