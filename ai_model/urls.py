from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TraitProfileViewSet,
    SuccessModelViewSet,
    TraitAssessmentViewSet,
    AssessmentValidationViewSet,
    trait_inference_view
)

router = DefaultRouter()
router.register(r'trait-profiles', TraitProfileViewSet, basename='traitprofile')
router.register(r'success-models', SuccessModelViewSet)
router.register(r'trait-assessments', TraitAssessmentViewSet)
router.register(r'assessment-validations', AssessmentValidationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('infer/', trait_inference_view, name='trait_inference'),
]
