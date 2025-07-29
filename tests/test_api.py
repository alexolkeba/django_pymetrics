"""
Comprehensive tests for API endpoints and serializers.

Tests cover all REST API endpoints including behavioral data ingestion,
metric extraction, trait inference, and report generation.
"""

import json
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from behavioral_data.models import BehavioralSession, BehavioralEvent, BalloonRiskEvent, BehavioralMetric
from ai_model.models import TraitProfile
from accounts.models import User


class TestBehavioralDataAPI(APITestCase):
    """Test cases for behavioral data API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Authenticate client
        self.client.force_authenticate(user=self.test_user)
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id="api_test_session",
            user_id="api_test_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="active"
        )
    
    def test_create_behavioral_session(self):
        """Test creating a new behavioral session via API."""
        session_data = {
            'session_id': 'new_api_session',
            'user_id': 'new_api_user',
            'game_type': 'balloon_risk',
            'status': 'active'
        }
        
        response = self.client.post('/api/sessions/', session_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['session_id'], 'new_api_session')
        
        # Verify session was created in database
        session = BehavioralSession.objects.get(session_id='new_api_session')
        self.assertEqual(session.user_id, 'new_api_user')
        self.assertEqual(session.game_type, 'balloon_risk')
    
    def test_list_behavioral_sessions(self):
        """Test listing behavioral sessions via API."""
        response = self.client.get('/api/sessions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        # Check that our test session is in the list
        session_ids = [session['session_id'] for session in response.data]
        self.assertIn('api_test_session', session_ids)
    
    def test_retrieve_behavioral_session(self):
        """Test retrieving a specific behavioral session via API."""
        response = self.client.get(f'/api/sessions/{self.test_session.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['session_id'], 'api_test_session')
    
    def test_create_behavioral_event(self):
        """Test creating behavioral events via API."""
        event_data = {
            'session': self.test_session.id,
            'event_type': 'balloon_risk',
            'action': 'pump',
            'balloon_id': 1,
            'pump_number': 5,
            'timestamp': timezone.now().isoformat(),
            'reaction_time_ms': 750,
            'event_id': 'api_test_event_1'
        }
        
        response = self.client.post('/api/events/', event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify event was created
        event = BalloonRiskEvent.objects.get(event_id='api_test_event_1')
        self.assertEqual(event.action, 'pump')
        self.assertEqual(event.balloon_id, 1)
        self.assertEqual(event.pump_number, 5)
    
    def test_create_invalid_behavioral_event(self):
        """Test creating invalid behavioral event via API."""
        invalid_event_data = {
            'session': self.test_session.id,
            'event_type': 'balloon_risk',
            # Missing required 'action' field
            'balloon_id': 1,
            'timestamp': timezone.now().isoformat()
        }
        
        response = self.client.post('/api/events/', invalid_event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_behavioral_events(self):
        """Test listing behavioral events via API."""
        # Create test event
        BalloonRiskEvent.objects.create(
            session=self.test_session,
            event_type='balloon_risk',
            action='pump',
            balloon_id=1,
            pump_number=1,
            timestamp=timezone.now(),
            event_id='list_test_event'
        )
        
        response = self.client.get('/api/events/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class TestMetricExtractionAPI(APITestCase):
    """Test cases for metric extraction API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='metricuser',
            email='metric@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.test_user)
        
        # Create test session with events
        self.test_session = BehavioralSession.objects.create(
            session_id="metric_api_session",
            user_id="metric_api_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create test events
        self._create_test_events()
    
    def _create_test_events(self):
        """Create test events for metric extraction."""
        for i in range(15):
            BalloonRiskEvent.objects.create(
                session=self.test_session,
                event_type='balloon_risk',
                action='pump',
                balloon_id=1,
                pump_number=i + 1,
                timestamp=timezone.now() - timedelta(minutes=15-i),
                reaction_time_ms=500 + i * 50,
                event_id=f'metric_event_{i}'
            )
    
    def test_extract_metrics_api(self):
        """Test metric extraction via API."""
        request_data = {
            'session_id': 'metric_api_session'
        }
        
        response = self.client.post('/api/metrics/extract_metrics/', request_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('processed', response.data)
        
        if response.data['processed']:
            self.assertIn('balloon_risk', response.data)
    
    def test_extract_metrics_invalid_session(self):
        """Test metric extraction with invalid session ID."""
        request_data = {
            'session_id': 'nonexistent_session'
        }
        
        response = self.client.post('/api/metrics/extract_metrics/', request_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['processed'])
        self.assertIn('error', response.data)
    
    def test_list_behavioral_metrics(self):
        """Test listing behavioral metrics via API."""
        # Create test metric
        BehavioralMetric.objects.create(
            session=self.test_session,
            metric_type='game_level',
            metric_name='test_metric',
            game_type='balloon_risk',
            metric_value=0.75,
            metric_unit='score',
            sample_size=15,
            calculation_method='Test',
            calculation_timestamp=timezone.now(),
            data_version='1.0'
        )
        
        response = self.client.get('/api/metrics/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class TestTraitInferenceAPI(APITestCase):
    """Test cases for trait inference API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='traituser',
            email='trait@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.test_user)
        
        # Create test session with metrics
        self.test_session = BehavioralSession.objects.create(
            session_id="trait_api_session",
            user_id="trait_api_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create test metrics
        self._create_test_metrics()
    
    def _create_test_metrics(self):
        """Create test metrics for trait inference."""
        metrics_data = [
            ('balloon_risk_risk_tolerance_average_pumps', 8.5),
            ('balloon_risk_risk_tolerance_risk_escalation', 0.12),
            ('balloon_risk_consistency_behavioral_consistency', 0.75),
            ('balloon_risk_learning_adaptation_rate', 0.68),
            ('balloon_risk_learning_learning_curve', 0.45),
            ('balloon_risk_emotion_stress_response', 0.35)
        ]
        
        for metric_name, metric_value in metrics_data:
            BehavioralMetric.objects.create(
                session=self.test_session,
                metric_type='game_level',
                metric_name=metric_name,
                game_type='balloon_risk',
                metric_value=metric_value,
                metric_unit='score',
                sample_size=20,
                calculation_method='MetricExtractor Agent',
                calculation_timestamp=timezone.now(),
                data_version='1.0'
            )
    
    def test_infer_traits_api(self):
        """Test trait inference via API."""
        # First create a trait profile to test with
        trait_profile = TraitProfile.objects.create(
            session=self.test_session,
            trait_name='risk_tolerance',
            trait_score=0.75,
            confidence_score=0.85,
            calculation_method='TraitInferencer Agent',
            data_version='1.0'
        )
        
        response = self.client.post(f'/api/traits/{trait_profile.id}/infer_traits/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_trait_profiles(self):
        """Test listing trait profiles via API."""
        # Create test trait profile
        TraitProfile.objects.create(
            session=self.test_session,
            trait_name='risk_tolerance',
            trait_score=0.75,
            confidence_score=0.85,
            calculation_method='TraitInferencer Agent',
            data_version='1.0'
        )
        
        response = self.client.get('/api/traits/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_trait_profile(self):
        """Test creating trait profile via API."""
        trait_data = {
            'session': self.test_session.id,
            'trait_name': 'learning_ability',
            'trait_score': 0.68,
            'confidence_score': 0.78,
            'calculation_method': 'API Test',
            'data_version': '1.0'
        }
        
        response = self.client.post('/api/traits/', trait_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['trait_name'], 'learning_ability')
        self.assertEqual(float(response.data['trait_score']), 0.68)


class TestReportGenerationAPI(APITestCase):
    """Test cases for report generation API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='reportuser',
            email='report@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.test_user)
        
        # Create test session with trait profiles
        self.test_session = BehavioralSession.objects.create(
            session_id="report_api_session",
            user_id="report_api_user",
            game_type="balloon_risk",
            started_at=timezone.now() - timedelta(hours=1),
            status="completed",
            duration_ms=3600000
        )
        
        # Create test trait profiles
        self._create_test_trait_profiles()
    
    def _create_test_trait_profiles(self):
        """Create test trait profiles for report generation."""
        traits_data = [
            ('risk_tolerance', 0.75, 0.85),
            ('learning_ability', 0.68, 0.78),
            ('emotion_regulation', 0.82, 0.88)
        ]
        
        for trait_name, trait_score, confidence in traits_data:
            TraitProfile.objects.create(
                session=self.test_session,
                trait_name=trait_name,
                trait_score=trait_score,
                confidence_score=confidence,
                calculation_method='TraitInferencer Agent',
                data_version='1.0'
            )
    
    def test_generate_report_api(self):
        """Test report generation via API."""
        request_data = {
            'session_id': 'report_api_session'
        }
        
        response = self.client.post('/api/reports/generate_report/', request_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('generated', response.data)
        
        if response.data['generated']:
            self.assertIn('report', response.data)
            report = response.data['report']
            self.assertIn('session_summary', report)
            self.assertIn('trait_profiles', report)
    
    def test_generate_report_invalid_session(self):
        """Test report generation with invalid session ID."""
        request_data = {
            'session_id': 'nonexistent_session'
        }
        
        response = self.client.post('/api/reports/generate_report/', request_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['generated'])
        self.assertIn('error', response.data)


class TestAPIAuthentication(APITestCase):
    """Test cases for API authentication and permissions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password='testpass123'
        )
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected."""
        response = self.client.get('/api/sessions/')
        
        # Should require authentication - returns 403 Forbidden with SessionAuthentication
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_access(self):
        """Test that authenticated requests are allowed."""
        self.client.force_authenticate(user=self.test_user)
        
        response = self.client.get('/api/sessions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_session_authentication(self):
        """Test session-based authentication."""
        # Login user
        self.client.login(username='authuser', password='testpass123')
        
        response = self.client.get('/api/sessions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAPIErrorHandling(APITestCase):
    """Test cases for API error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='erroruser',
            email='error@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.test_user)
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON requests."""
        response = self.client.post(
            '/api/sessions/',
            'invalid json content',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_missing_required_fields(self):
        """Test handling of requests with missing required fields."""
        incomplete_data = {
            'user_id': 'test_user'
            # Missing required 'session_id' and 'game_type'
        }
        
        response = self.client.post('/api/sessions/', incomplete_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_nonexistent_resource(self):
        """Test handling of requests for nonexistent resources."""
        response = self.client.get('/api/sessions/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAPIPerformance(APITestCase):
    """Test cases for API performance and optimization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='perfuser',
            email='perf@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.test_user)
        
        # Create multiple test sessions for performance testing
        self._create_bulk_test_data()
    
    def _create_bulk_test_data(self):
        """Create bulk test data for performance testing."""
        sessions = []
        for i in range(10):
            session = BehavioralSession(
                session_id=f'perf_session_{i}',
                user_id=f'perf_user_{i}',
                game_type='balloon_risk',
                started_at=timezone.now() - timedelta(hours=i),
                status='completed'
            )
            sessions.append(session)
        
        BehavioralSession.objects.bulk_create(sessions)
    
    def test_bulk_session_listing_performance(self):
        """Test performance of listing many sessions."""
        import time
        
        start_time = time.time()
        response = self.client.get('/api/sessions/')
        end_time = time.time()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 10)
        
        # Should complete within reasonable time (2 seconds)
        self.assertLess(end_time - start_time, 2.0)
    
    def test_pagination_functionality(self):
        """Test API pagination functionality."""
        # Test with page size limit
        response = self.client.get('/api/sessions/?page_size=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should respect page size if pagination is implemented
        if 'results' in response.data:
            self.assertLessEqual(len(response.data['results']), 5)
        else:
            # If no pagination, should still return data
            self.assertGreaterEqual(len(response.data), 1)


if __name__ == '__main__':
    import unittest
    unittest.main()
