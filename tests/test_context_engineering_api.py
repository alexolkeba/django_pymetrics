"""
Test Context Engineering API Implementation

This module tests the context-engineered trait inference API endpoint
to ensure it provides multi-dimensional psychometric trait profiles
with proper scientific validation and error handling.
"""

import pytest
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile

User = get_user_model()


class TestContextEngineeringAPI(TestCase):
    """Test cases for context-engineered trait inference API."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test session
        self.session = BehavioralSession.objects.create(
            user=self.user,
            session_id='test_session_123',
            game_type='balloon_risk',
            status='completed',
            session_start_time=timezone.now() - timedelta(minutes=5),
            session_end_time=timezone.now(),
            is_completed=True,
            total_duration=300000,  # 5 minutes
            total_games_played=1
        )
        
        # Create test events
        self._create_test_events()
        
        # Create test metrics
        self._create_test_metrics()
    
    def _create_test_events(self):
        """Create test behavioral events."""
        events_data = [
            {
                'event_type': 'balloon_risk',
                'event_name': 'pump',
                'timestamp_milliseconds': 1000,
                'event_data': {
                    'balloon_id': 'balloon_1',
                    'pump_number': 3,
                    'balloon_size': 1.2,
                    'current_earnings': 0.15,
                    'time_since_prev_pump': 1500
                }
            },
            {
                'event_type': 'balloon_risk',
                'event_name': 'pump',
                'timestamp_milliseconds': 2500,
                'event_data': {
                    'balloon_id': 'balloon_1',
                    'pump_number': 4,
                    'balloon_size': 1.4,
                    'current_earnings': 0.20,
                    'time_since_prev_pump': 1200
                }
            },
            {
                'event_type': 'balloon_risk',
                'event_name': 'cash_out',
                'timestamp_milliseconds': 4000,
                'event_data': {
                    'balloon_id': 'balloon_1',
                    'pump_number': 4,
                    'earnings_collected': 0.20
                }
            }
        ]
        
        for event_data in events_data:
            BehavioralEvent.objects.create(
                session=self.session,
                **event_data
            )
    
    def _create_test_metrics(self):
        """Create test behavioral metrics."""
        metrics_data = [
            {
                'metric_name': 'balloon_risk_risk_tolerance_avg_pumps_per_balloon',
                'metric_value': 4.0,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            },
            {
                'metric_name': 'balloon_risk_risk_tolerance_risk_escalation_rate',
                'metric_value': 0.2,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            },
            {
                'metric_name': 'balloon_risk_consistency_behavioral_consistency_score',
                'metric_value': 0.8,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            },
            {
                'metric_name': 'balloon_risk_learning_patterns_adaptation_rate',
                'metric_value': 0.6,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            },
            {
                'metric_name': 'balloon_risk_decision_speed_avg_decision_time',
                'metric_value': 2000.0,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            },
            {
                'metric_name': 'balloon_risk_emotional_regulation_stress_response',
                'metric_value': 0.3,
                'metric_type': 'game_level',
                'game_type': 'balloon_risk'
            }
        ]
        
        for metric_data in metrics_data:
            BehavioralMetric.objects.create(
                session=self.session,
                **metric_data
            )
    
    def test_successful_trait_inference(self):
        """Test successful trait inference with valid data."""
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        response_data = response.data
        self.assertIn('session_id', response_data)
        self.assertIn('risk_tolerance', response_data)
        self.assertIn('consistency', response_data)
        self.assertIn('learning', response_data)
        self.assertIn('decision_speed', response_data)
        self.assertIn('emotional_regulation', response_data)
        self.assertIn('confidence_interval', response_data)
        self.assertIn('data_completeness', response_data)
        self.assertIn('quality_score', response_data)
        self.assertIn('reliability_score', response_data)
        self.assertIn('scientific_validation', response_data)
        
        # Check trait score ranges
        for trait in ['risk_tolerance', 'consistency', 'learning', 'decision_speed', 'emotional_regulation']:
            self.assertGreaterEqual(response_data[trait], 0.0)
            self.assertLessEqual(response_data[trait], 1.0)
        
        # Check validation scores
        self.assertGreaterEqual(response_data['confidence_interval'], 0.0)
        self.assertLessEqual(response_data['confidence_interval'], 1.0)
        self.assertGreaterEqual(response_data['data_completeness'], 0.0)
        self.assertLessEqual(response_data['data_completeness'], 100.0)
        self.assertGreaterEqual(response_data['quality_score'], 0.0)
        self.assertLessEqual(response_data['quality_score'], 100.0)
        
        # Check scientific validation
        scientific_validation = response_data['scientific_validation']
        self.assertIn('meets_thresholds', scientific_validation)
        self.assertIn('validation_method', scientific_validation)
        self.assertIn('data_schema_version', scientific_validation)
        self.assertIn('assessment_version', scientific_validation)
        
        self.assertTrue(scientific_validation['meets_thresholds'])
        self.assertEqual(scientific_validation['validation_method'], 'Context-engineered trait inference')
    
    def test_missing_session_id(self):
        """Test error handling for missing session_id."""
        url = reverse('trait-inference')
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Missing required field: session_id.', response.data['error'])
        self.assertIn('required_fields', response.data)
        self.assertIn('suggestion', response.data)
    
    def test_nonexistent_session(self):
        """Test error handling for nonexistent session."""
        url = reverse('trait-inference')
        data = {'session_id': 'nonexistent_session'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Session nonexistent_session not found', response.data['error'])
        self.assertIn('suggestion', response.data)
    
    def test_incomplete_session(self):
        """Test error handling for incomplete session."""
        # Create incomplete session
        incomplete_session = BehavioralSession.objects.create(
            user=self.user,
            session_id='incomplete_session',
            game_type='balloon_risk',
            status='in_progress',
            session_start_time=timezone.now() - timedelta(minutes=1),
            is_completed=False
        )
        
        url = reverse('trait-inference')
        data = {'session_id': 'incomplete_session'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Session is not completed', response.data['error'])
    
    def test_insufficient_events(self):
        """Test error handling for session with insufficient events."""
        # Create session with minimal events
        minimal_session = BehavioralSession.objects.create(
            user=self.user,
            session_id='minimal_session',
            game_type='balloon_risk',
            status='completed',
            session_start_time=timezone.now() - timedelta(minutes=5),
            session_end_time=timezone.now(),
            is_completed=True,
            total_duration=300000
        )
        
        # Add only 2 events (below minimum threshold)
        for i in range(2):
            BehavioralEvent.objects.create(
                session=minimal_session,
                event_type='balloon_risk',
                event_name='pump',
                timestamp_milliseconds=i * 1000,
                event_data={'pump_number': i + 1}
            )
        
        url = reverse('trait-inference')
        data = {'session_id': 'minimal_session'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Insufficient data completeness', response.data['error'])
    
    def test_short_session_duration(self):
        """Test error handling for very short session duration."""
        # Create session with short duration
        short_session = BehavioralSession.objects.create(
            user=self.user,
            session_id='short_session',
            game_type='balloon_risk',
            status='completed',
            session_start_time=timezone.now() - timedelta(seconds=10),
            session_end_time=timezone.now(),
            is_completed=True,
            total_duration=10000  # 10 seconds
        )
        
        # Add sufficient events
        for i in range(15):
            BehavioralEvent.objects.create(
                session=short_session,
                event_type='balloon_risk',
                event_name='pump',
                timestamp_milliseconds=i * 500,
                event_data={'pump_number': i + 1}
            )
        
        url = reverse('trait-inference')
        data = {'session_id': 'short_session'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Session duration too short', response.data['error'])
    
    def test_api_response_format(self):
        """Test that API response follows the documented format."""
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify exact response format as documented in README
        expected_keys = {
            'session_id', 'risk_tolerance', 'consistency', 'learning',
            'decision_speed', 'emotional_regulation', 'confidence_interval',
            'data_completeness', 'quality_score', 'reliability_score',
            'assessment_timestamp', 'scientific_validation'
        }
        
        response_keys = set(response.data.keys())
        self.assertTrue(expected_keys.issubset(response_keys))
        
        # Verify scientific validation structure
        scientific_validation = response.data['scientific_validation']
        expected_validation_keys = {
            'meets_thresholds', 'validation_method', 'data_schema_version', 'assessment_version'
        }
        validation_keys = set(scientific_validation.keys())
        self.assertTrue(expected_validation_keys.issubset(validation_keys))
    
    def test_error_response_format(self):
        """Test that error responses follow the documented format."""
        url = reverse('trait-inference')
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify error response format
        self.assertIn('error', response.data)
        self.assertIn('required_fields', response.data)
        self.assertIn('suggestion', response.data)
        
        # Verify error message is actionable
        error_message = response.data['error']
        self.assertIn('Missing required field', error_message)
        
        # Verify suggestion is helpful
        suggestion = response.data['suggestion']
        self.assertIn('Provide a valid session identifier', suggestion)
    
    def test_authentication_required(self):
        """Test that authentication is required for the API."""
        # Create unauthenticated client
        unauthenticated_client = APIClient()
        
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = unauthenticated_client.post(url, data, format='json')
        
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_trait_score_interpretation(self):
        """Test that trait scores are within reasonable ranges and interpretable."""
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that trait scores are normalized between 0 and 1
        trait_scores = {
            'risk_tolerance': response.data['risk_tolerance'],
            'consistency': response.data['consistency'],
            'learning': response.data['learning'],
            'decision_speed': response.data['decision_speed'],
            'emotional_regulation': response.data['emotional_regulation']
        }
        
        for trait_name, score in trait_scores.items():
            self.assertGreaterEqual(score, 0.0, f"{trait_name} score too low")
            self.assertLessEqual(score, 1.0, f"{trait_name} score too high")
            
            # Scores should not all be identical (indicating proper calculation)
            if trait_name == 'risk_tolerance':
                # Risk tolerance should be reasonable based on our test data
                self.assertGreater(score, 0.0, "Risk tolerance should be calculated")
    
    def test_confidence_calculation(self):
        """Test that confidence intervals are calculated correctly."""
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        confidence_interval = response.data['confidence_interval']
        
        # Confidence should be between 0 and 1
        self.assertGreaterEqual(confidence_interval, 0.0)
        self.assertLessEqual(confidence_interval, 1.0)
        
        # With our test data, confidence should be reasonable
        self.assertGreater(confidence_interval, 0.5, "Confidence should be reasonable with good data")
    
    def test_data_quality_metrics(self):
        """Test that data quality metrics are calculated correctly."""
        url = reverse('trait-inference')
        data = {'session_id': 'test_session_123'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data_completeness = response.data['data_completeness']
        quality_score = response.data['quality_score']
        reliability_score = response.data['reliability_score']
        
        # All quality metrics should be percentages (0-100)
        for metric_name, metric_value in [
            ('data_completeness', data_completeness),
            ('quality_score', quality_score),
            ('reliability_score', reliability_score)
        ]:
            self.assertGreaterEqual(metric_value, 0.0, f"{metric_name} too low")
            self.assertLessEqual(metric_value, 100.0, f"{metric_name} too high")
        
        # With our test data, quality should be good
        self.assertGreater(quality_score, 50.0, "Quality score should be reasonable with test data") 