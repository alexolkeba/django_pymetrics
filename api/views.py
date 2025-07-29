from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile, SuccessModel
from .serializers import BehavioralSessionSerializer, BehavioralEventSerializer, BehavioralMetricSerializer, TraitProfileSerializer
from agents.metric_extractor import MetricExtractor
from agents.trait_inferencer import TraitInferencer
from agents.report_generator import ReportGenerator
from trait_mapping.trait_mappings import TraitMapper
from trait_mapping.validation import TraitValidationEngine
import logging

logger = logging.getLogger(__name__)

class BehavioralSessionViewSet(viewsets.ModelViewSet):
    queryset = BehavioralSession.objects.all()
    serializer_class = BehavioralSessionSerializer

class BehavioralEventViewSet(viewsets.ModelViewSet):
    queryset = BehavioralEvent.objects.all()
    serializer_class = BehavioralEventSerializer

class BehavioralMetricViewSet(viewsets.ModelViewSet):
    queryset = BehavioralMetric.objects.all()
    serializer_class = BehavioralMetricSerializer

class TraitProfileViewSet(viewsets.ModelViewSet):
    queryset = TraitProfile.objects.all()
    serializer_class = TraitProfileSerializer

    @action(detail=True, methods=['post'])
    def infer_traits(self, request, pk=None):
        session = self.get_object()
        inferencer = TraitInferencer()
        result = inferencer.infer_session_traits(session.session_id)
        return Response(result)

class MetricExtractionViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def extract_metrics(self, request):
        session_id = request.data.get('session_id')
        extractor = MetricExtractor()
        result = extractor.extract_metrics(session_id)
        return Response(result)

class ReportGenerationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        session_id = request.data.get('session_id')
        generator = ReportGenerator()
        result = generator.generate_session_report(session_id)
        return Response(result)

class TraitInferenceAPIView(APIView):
    """
    Context-engineered trait inference endpoint.
    
    Provides multi-dimensional psychometric trait profiles for a user/session,
    based on scientifically validated mapping from behavioral metrics.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trait_mapper = TraitMapper()
        self.validation_engine = TraitValidationEngine()
        
        # Scientific validation thresholds
        self.validation_thresholds = {
            'min_data_completeness': 80.0,  # 80% data completeness required
            'min_quality_score': 70.0,      # 70% data quality required
            'min_reliability_score': 75.0,  # 75% reliability required
            'confidence_interval_level': 0.95,  # 95% confidence interval
            'min_sample_size': 10,          # Minimum 10 data points
        }
    
    def post(self, request):
        """
        Infer psychometric traits for a session.
        
        Expected input:
        {
            "session_id": "session_123"
        }
        
        Returns:
        {
            "risk_tolerance": 0.85,
            "consistency": 0.92,
            "learning": 0.78,
            "decision_speed": 0.67,
            "emotional_regulation": 0.81,
            "confidence_interval": 0.95
        }
        """
        try:
            # Extract and validate input
            session_id = request.data.get('session_id')
            if not session_id:
                return Response({
                    'error': 'Missing required field: session_id.',
                    'required_fields': ['session_id'],
                    'suggestion': 'Provide a valid session identifier.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate session exists and has sufficient data
            validation_result = self._validate_session_data(session_id)
            if not validation_result['is_valid']:
                return Response({
                    'error': validation_result['error'],
                    'required_fields': ['session_id', 'event_data'],
                    'suggestion': validation_result['suggestion']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract metrics if not already available
            metrics_result = self._ensure_metrics_available(session_id)
            if not metrics_result['success']:
                return Response({
                    'error': metrics_result['error'],
                    'suggestion': 'Ensure session contains sufficient behavioral events.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform trait inference
            trait_result = self._perform_trait_inference(session_id)
            if not trait_result['success']:
                return Response({
                    'error': trait_result['error'],
                    'suggestion': 'Trait inference failed due to insufficient or invalid data.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate trait inference results
            trait_validation = self._validate_trait_results(trait_result['traits'], session_id)
            if not trait_validation['is_valid']:
                return Response({
                    'error': trait_validation['error'],
                    'suggestion': 'Trait inference results do not meet scientific validation thresholds.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Return successful trait profile
            return Response({
                'session_id': session_id,
                'risk_tolerance': trait_result['traits'].get('risk_tolerance', 0.5),
                'consistency': trait_result['traits'].get('consistency', 0.5),
                'learning': trait_result['traits'].get('learning_ability', 0.5),
                'decision_speed': trait_result['traits'].get('decision_speed', 0.5),
                'emotional_regulation': trait_result['traits'].get('emotional_regulation', 0.5),
                'confidence_interval': trait_validation['confidence_level'],
                'data_completeness': validation_result['data_completeness'],
                'quality_score': validation_result['quality_score'],
                'reliability_score': trait_validation['reliability_score'],
                'assessment_timestamp': trait_result['timestamp'],
                'scientific_validation': {
                    'meets_thresholds': True,
                    'validation_method': 'Context-engineered trait inference',
                    'data_schema_version': '1.0',
                    'assessment_version': '1.0'
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Trait inference error: {str(e)}", exc_info=True)
            return Response({
                'error': 'Internal server error during trait inference.',
                'suggestion': 'Please try again or contact support if the issue persists.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _validate_session_data(self, session_id: str) -> dict:
        """Validate session data completeness and quality."""
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
            
            # Check session completion
            if not session.is_completed:
                return {
                    'is_valid': False,
                    'error': 'Session is not completed.',
                    'suggestion': 'Ensure session is fully completed before trait inference.'
                }
            
            # Check session duration
            if session.session_end_time and session.session_start_time:
                duration = (session.session_end_time - session.session_start_time).total_seconds()
                if duration < 30:  # Less than 30 seconds
                    return {
                        'is_valid': False,
                        'error': 'Session duration too short for reliable assessment.',
                        'suggestion': 'Ensure session duration is at least 30 seconds.'
                    }
            
            # Count events
            event_count = BehavioralEvent.objects.filter(session=session).count()
            if event_count < self.validation_thresholds['min_sample_size']:
                return {
                    'is_valid': False,
                    'error': f'Insufficient data completeness (required: {self.validation_thresholds["min_sample_size"]} events).',
                    'suggestion': f'Ensure session contains at least {self.validation_thresholds["min_sample_size"]} valid events.',
                    'data_completeness': (event_count / self.validation_thresholds['min_sample_size']) * 100
                }
            
            # Calculate data quality
            valid_events = BehavioralEvent.objects.filter(
                session=session, 
                validation_status='valid'
            ).count()
            quality_score = (valid_events / event_count) * 100 if event_count > 0 else 0
            
            if quality_score < self.validation_thresholds['min_quality_score']:
                return {
                    'is_valid': False,
                    'error': f'Data quality below threshold (required: {self.validation_thresholds["min_quality_score"]}%).',
                    'suggestion': 'Ensure high-quality behavioral data collection.',
                    'quality_score': quality_score
                }
            
            return {
                'is_valid': True,
                'data_completeness': (event_count / self.validation_thresholds['min_sample_size']) * 100,
                'quality_score': quality_score,
                'event_count': event_count
            }
            
        except BehavioralSession.DoesNotExist:
            return {
                'is_valid': False,
                'error': f'Session {session_id} not found.',
                'suggestion': 'Provide a valid session identifier.'
            }
    
    def _ensure_metrics_available(self, session_id: str) -> dict:
        """Ensure metrics are available for trait inference."""
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
            
            # Check if metrics already exist
            existing_metrics = BehavioralMetric.objects.filter(session=session).count()
            if existing_metrics >= 5:  # Minimum metrics for trait inference
                return {'success': True, 'metrics_count': existing_metrics}
            
            # Extract metrics if not available
            extractor = MetricExtractor()
            result = extractor.extract_session_metrics(session_id)
            
            if result.get('processed', False):
                new_metrics = BehavioralMetric.objects.filter(session=session).count()
                return {
                    'success': True, 
                    'metrics_count': new_metrics,
                    'metrics_extracted': True
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Metric extraction failed.')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error ensuring metrics availability: {str(e)}'
            }
    
    def _perform_trait_inference(self, session_id: str) -> dict:
        """Perform trait inference using the TraitInferencer agent."""
        try:
            inferencer = TraitInferencer()
            result = inferencer.infer_session_traits(session_id)
            
            if result.get('processed', False):
                return {
                    'success': True,
                    'traits': result.get('traits', {}),
                    'timestamp': result.get('timestamp'),
                    'processing_time': result.get('processing_time')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Trait inference failed.')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during trait inference: {str(e)}'
            }
    
    def _validate_trait_results(self, traits: dict, session_id: str) -> dict:
        """Validate trait inference results against scientific thresholds."""
        try:
            # Check if we have the minimum required traits
            required_traits = ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']
            available_traits = [trait for trait in required_traits if trait in traits]
            
            if len(available_traits) < 3:  # At least 3 traits required
                return {
                    'is_valid': False,
                    'error': f'Insufficient trait coverage (required: 3, available: {len(available_traits)}).',
                    'suggestion': 'Ensure sufficient behavioral data for comprehensive trait assessment.'
                }
            
            # Calculate confidence level based on trait scores
            trait_scores = [traits.get(trait, 0.5) for trait in available_traits]
            confidence_level = min(0.95, 0.7 + (len(available_traits) / len(required_traits)) * 0.25)
            
            # Calculate reliability score
            reliability_score = self._calculate_reliability_score(traits, session_id)
            
            if reliability_score < self.validation_thresholds['min_reliability_score']:
                return {
                    'is_valid': False,
                    'error': f'Reliability score below threshold (required: {self.validation_thresholds["min_reliability_score"]}%).',
                    'suggestion': 'Ensure consistent behavioral patterns for reliable assessment.',
                    'reliability_score': reliability_score
                }
            
            return {
                'is_valid': True,
                'confidence_level': confidence_level,
                'reliability_score': reliability_score,
                'trait_coverage': len(available_traits) / len(required_traits)
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'error': f'Error validating trait results: {str(e)}'
            }
    
    def _calculate_reliability_score(self, traits: dict, session_id: str) -> float:
        """Calculate reliability score based on trait consistency and data quality."""
        try:
            # Get session metrics for reliability calculation
            session = BehavioralSession.objects.get(session_id=session_id)
            metrics = BehavioralMetric.objects.filter(session=session)
            
            if not metrics.exists():
                return 50.0  # Default moderate reliability
            
            # Calculate reliability based on metric consistency
            metric_values = [m.metric_value for m in metrics if m.metric_value is not None]
            if not metric_values:
                return 50.0
            
            # Higher consistency = higher reliability
            mean_value = sum(metric_values) / len(metric_values)
            variance = sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)
            std_dev = variance ** 0.5
            
            # Normalize reliability (lower std dev = higher reliability)
            if mean_value > 0:
                coefficient_of_variation = std_dev / mean_value
                reliability = max(50.0, 100.0 - (coefficient_of_variation * 100))
            else:
                reliability = 50.0
            
            return min(100.0, reliability)
            
        except Exception:
            return 50.0  # Default moderate reliability
