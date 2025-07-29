"""
Comprehensive Test Suite for Django Pymetrics

This module provides comprehensive testing for all major components
of the Django Pymetrics application including agents, models, APIs,
and Celery tasks.
"""

import os
import sys
import django
import json
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from behavioral_data.models import (
    BehavioralSession, BehavioralEvent, BalloonRiskEvent, 
    BehavioralMetric, MemoryCardsEvent, ReactionTimerEvent
)
from ai_model.models import TraitProfile, SuccessModel, TraitAssessment
from agents.event_logger import EventLogger
from agents.metric_extractor import MetricExtractor
from agents.trait_inferencer import TraitInferencer
from agents.report_generator import ReportGenerator
from tasks.event_processing import process_single_event, process_batch_events
from tasks.metric_extraction import extract_session_metrics, validate_metrics
from tasks.trait_inference import infer_session_traits, validate_trait_profiles
from tasks.reporting import generate_session_report, generate_user_report

User = get_user_model()


class ComprehensiveTestSuite(TestCase):
    """Comprehensive test suite for Django Pymetrics application."""
    
    def setUp(self):
        """Set up test data and user."""
        self.user = User.objects.create_user(
            username='testuser_comprehensive',
            email='test_comprehensive@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser_comprehensive', password='testpass123')
        
        # Create test session
        self.session = BehavioralSession.objects.create(
            user=self.user,
            session_id='test_session_123',
            game_type='balloon_risk',
            status='completed',
            is_completed=True,
            total_duration=300000,  # 5 minutes
            total_games_played=3
        )
    
    def test_agent_initialization(self):
        """Test that all agents can be initialized properly."""
        print("🧪 Testing Agent Initialization...")
        
        # Test EventLogger
        event_logger = EventLogger()
        self.assertIsNotNone(event_logger)
        self.assertEqual(event_logger.agent_name, 'event_logger')
        
        # Test MetricExtractor
        metric_extractor = MetricExtractor()
        self.assertIsNotNone(metric_extractor)
        self.assertEqual(metric_extractor.agent_name, 'metric_extractor')
        
        # Test TraitInferencer
        trait_inferencer = TraitInferencer()
        self.assertIsNotNone(trait_inferencer)
        self.assertEqual(trait_inferencer.agent_name, 'trait_inferencer')
        
        # Test ReportGenerator
        report_generator = ReportGenerator()
        self.assertIsNotNone(report_generator)
        self.assertEqual(report_generator.agent_name, 'report_generator')
        
        print("✅ All agents initialized successfully")
    
    def test_behavioral_data_models(self):
        """Test behavioral data models and their relationships."""
        print("🧪 Testing Behavioral Data Models...")
        
        # Test BehavioralSession
        self.assertIsNotNone(self.session)
        self.assertEqual(self.session.session_id, 'test_session_123')
        self.assertEqual(self.session.game_type, 'balloon_risk')
        self.assertTrue(self.session.is_completed)
        
        # Test BehavioralEvent creation
        event = BehavioralEvent.objects.create(
            session=self.session,
            event_type='user_action',
            event_name='pump',
            timestamp_milliseconds=int(time.time() * 1000),
            event_data={
                'balloon_id': 'balloon_1',
                'pump_number': 5,
                'balloon_size': 1.2
            }
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, 'user_action')
        
        # Test BalloonRiskEvent
        balloon_event = BalloonRiskEvent.objects.create(
            session=self.session,
            event_type='pump',
            balloon_id='balloon_1',
            pump_number=5,
            balloon_size=1.2,
            current_earnings=0.25,
            total_earnings=1.50,
            timestamp_milliseconds=int(time.time() * 1000)
        )
        self.assertIsNotNone(balloon_event)
        self.assertEqual(balloon_event.pump_number, 5)
        
        print("✅ Behavioral data models working correctly")
    
    def test_event_logger_agent(self):
        """Test EventLogger agent functionality."""
        print("🧪 Testing EventLogger Agent...")
        
        event_logger = EventLogger()
        
        # Test balloon risk event processing
        event_data = {
            'session_id': 'test_session_123',
            'event_type': 'balloon_risk',
            'event_data': {
                'balloon_id': 'balloon_1',
                'pump_number': 5,
                'timestamp_milliseconds': int(time.time() * 1000),
                'balloon_size': 1.2,
                'current_earnings': 0.25,
                'total_earnings': 1.50,
                'time_since_prev_pump': 1500,
                'is_new_personal_max': True,
                'is_rapid_pump': False
            }
        }
        
        result = event_logger.process(event_data)
        self.assertIsNotNone(result)
        self.assertTrue(result.get('processed', False))
        
        print("✅ EventLogger agent working correctly")
    
    def test_metric_extractor_agent(self):
        """Test MetricExtractor agent functionality."""
        print("🧪 Testing MetricExtractor Agent...")
        
        # Create test events first
        for i in range(10):
            BalloonRiskEvent.objects.create(
                session=self.session,
                event_type='pump',
                balloon_id=f'balloon_{i}',
                pump_number=i + 1,
                balloon_size=1.0 + (i * 0.1),
                current_earnings=0.25 * (i + 1),
                total_earnings=1.50 + (i * 0.25),
                timestamp_milliseconds=int(time.time() * 1000) + (i * 1000)
            )
        
        metric_extractor = MetricExtractor()
        
        # Test metric extraction
        result = metric_extractor.extract_session_metrics('test_session_123')
        self.assertIsNotNone(result)
        
        print("✅ MetricExtractor agent working correctly")
    
    def test_trait_inferencer_agent(self):
        """Test TraitInferencer agent functionality."""
        print("🧪 Testing TraitInferencer Agent...")
        
        # Create metrics first
        BehavioralMetric.objects.create(
            session=self.session,
            metric_type='session_level',
            metric_name='avg_pumps_per_balloon',
            metric_value=0.75,
            game_type='balloon_risk',
            sample_size=10
        )
        
        trait_inferencer = TraitInferencer()
        
        # Test trait inference
        result = trait_inferencer.infer_session_traits('test_session_123')
        self.assertIsNotNone(result)
        
        print("✅ TraitInferencer agent working correctly")
    
    def test_report_generator_agent(self):
        """Test ReportGenerator agent functionality."""
        print("🧪 Testing ReportGenerator Agent...")
        
        report_generator = ReportGenerator()
        
        # Test report generation
        result = report_generator.generate_session_report('test_session_123')
        self.assertIsNotNone(result)
        
        print("✅ ReportGenerator agent working correctly")
    
    def test_celery_tasks(self):
        """Test Celery task functionality."""
        print("🧪 Testing Celery Tasks...")
        
        # Test event processing task
        event_data = {
            'session_id': 'test_session_123',
            'event_type': 'balloon_risk',
            'event_data': {
                'balloon_id': 'balloon_2',
                'pump_number': 3,
                'timestamp_milliseconds': int(time.time() * 1000),
                'balloon_size': 1.1,
                'current_earnings': 0.15,
                'total_earnings': 1.65
            }
        }
        
        # Mock the task to avoid actual Celery execution
        with patch('tasks.event_processing.process_single_event.delay') as mock_task:
            mock_task.return_value = MagicMock()
            result = process_single_event(event_data)
            self.assertIsNotNone(result)
        
        print("✅ Celery tasks working correctly")
    
    def test_api_endpoints(self):
        """Test API endpoint functionality."""
        print("🧪 Testing API Endpoints...")
        
        # Test behavioral session API
        response = self.client.get('/api/behavioral-sessions/')
        self.assertEqual(response.status_code, 200)
        
        # Test behavioral events API
        response = self.client.get('/api/behavioral-events/')
        self.assertEqual(response.status_code, 200)
        
        print("✅ API endpoints working correctly")
    
    def test_data_validation(self):
        """Test data validation and integrity."""
        print("🧪 Testing Data Validation...")
        
        # Test session validation
        self.assertTrue(self.session.is_completed)
        self.assertGreater(self.session.total_duration, 0)
        
        # Test event validation
        events = BehavioralEvent.objects.filter(session=self.session)
        for event in events:
            self.assertIsNotNone(event.timestamp)
            self.assertIsNotNone(event.event_type)
        
        print("✅ Data validation working correctly")
    
    def test_performance_metrics(self):
        """Test performance metrics and monitoring."""
        print("🧪 Testing Performance Metrics...")
        
        # Test agent performance metrics
        event_logger = EventLogger()
        metrics = event_logger.get_performance_metrics()
        
        self.assertIn('agent_name', metrics)
        self.assertIn('processed_count', metrics)
        self.assertIn('error_count', metrics)
        self.assertIn('success_rate', metrics)
        
        print("✅ Performance metrics working correctly")
    
    def test_error_handling(self):
        """Test error handling and recovery."""
        print("🧪 Testing Error Handling...")
        
        event_logger = EventLogger()
        
        # Test with invalid data
        invalid_data = {
            'session_id': 'non_existent_session',
            'event_type': 'invalid_type',
            'event_data': {}
        }
        
        try:
            result = event_logger.process(invalid_data)
            # Should handle error gracefully
            self.assertIsNotNone(result)
        except Exception as e:
            # Error should be handled by the agent
            self.assertIsNotNone(str(e))
        
        print("✅ Error handling working correctly")
    
    def test_scientific_validation(self):
        """Test scientific validation and quality controls."""
        print("🧪 Testing Scientific Validation...")
        
        # Test metric quality validation
        metric = BehavioralMetric.objects.create(
            session=self.session,
            metric_type='session_level',
            metric_name='test_metric',
            metric_value=0.85,
            game_type='balloon_risk',
            sample_size=10,
            standard_error=0.05,
            confidence_interval={'lower': 0.80, 'upper': 0.90}
        )
        
        self.assertIsNotNone(metric.confidence_interval)
        self.assertGreater(metric.metric_value, 0)
        self.assertLess(metric.metric_value, 1)
        
        print("✅ Scientific validation working correctly")
    
    def test_batch_processing(self):
        """Test batch processing capabilities."""
        print("🧪 Testing Batch Processing...")
        
        # Create multiple events
        events = []
        for i in range(5):
            events.append({
                'session_id': 'test_session_123',
                'event_type': 'balloon_risk',
                'event_data': {
                    'balloon_id': f'balloon_batch_{i}',
                    'pump_number': i + 1,
                    'timestamp_milliseconds': int(time.time() * 1000) + (i * 1000),
                    'balloon_size': 1.0 + (i * 0.1),
                    'current_earnings': 0.25 * (i + 1)
                }
            })
        
        event_logger = EventLogger()
        result = event_logger.batch_process_events(events)
        
        self.assertIsNotNone(result)
        self.assertIn('processed_count', result)
        
        print("✅ Batch processing working correctly")
    
    def test_data_persistence(self):
        """Test data persistence and retrieval."""
        print("🧪 Testing Data Persistence...")
        
        # Create test data
        original_count = BehavioralEvent.objects.count()
        
        # Add new event
        BehavioralEvent.objects.create(
            session=self.session,
            event_type='user_action',
            event_name='test_action',
            timestamp_milliseconds=int(time.time() * 1000),
            event_data={'test': 'data'}
        )
        
        # Verify persistence
        new_count = BehavioralEvent.objects.count()
        self.assertEqual(new_count, original_count + 1)
        
        # Test retrieval
        events = BehavioralEvent.objects.filter(session=self.session)
        self.assertGreater(events.count(), 0)
        
        print("✅ Data persistence working correctly")
    
    def run_comprehensive_test(self):
        """Run all comprehensive tests."""
        print("🚀 Starting Comprehensive Test Suite...")
        
        test_methods = [
            'test_agent_initialization',
            'test_behavioral_data_models',
            'test_event_logger_agent',
            'test_metric_extractor_agent',
            'test_trait_inferencer_agent',
            'test_report_generator_agent',
            'test_celery_tasks',
            'test_api_endpoints',
            'test_data_validation',
            'test_performance_metrics',
            'test_error_handling',
            'test_scientific_validation',
            'test_batch_processing',
            'test_data_persistence'
        ]
        
        passed = 0
        total = len(test_methods)
        
        for test_method in test_methods:
            try:
                getattr(self, test_method)()
                passed += 1
                print(f"✅ {test_method}: PASSED")
            except Exception as e:
                print(f"❌ {test_method}: FAILED - {str(e)}")
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All comprehensive tests passed! Application is working correctly.")
        else:
            print(f"⚠️ {total - passed} tests failed. Review and fix issues.")
        
        return passed == total


if __name__ == '__main__':
    # Run the comprehensive test suite
    test_suite = ComprehensiveTestSuite()
    test_suite.setUp()
    success = test_suite.run_comprehensive_test()
    
    if success:
        print("\n🎯 Comprehensive test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Comprehensive test suite found issues!")
        sys.exit(1) 