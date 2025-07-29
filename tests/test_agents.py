"""
Comprehensive tests for all agent components in the Django Pymetrics framework.

Tests cover EventLogger, MetricExtractor, TraitInferencer, and ReportGenerator agents
with various scenarios including edge cases and error conditions.
"""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from agents.event_logger import EventLogger
from agents.metric_extractor import MetricExtractor
from agents.trait_inferencer import TraitInferencer
from agents.report_generator import ReportGenerator
from behavioral_data.models import BehavioralSession, BehavioralEvent, BalloonRiskEvent, BehavioralMetric
from ai_model.models import TraitProfile


class TestEventLogger(TestCase):
    """Test cases for EventLogger agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.event_logger = EventLogger()
        self.test_session_id = "test_session_123"
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="test_user_123",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="active"
        )
    
    def test_log_valid_balloon_risk_event(self):
        """Test logging a valid balloon risk event."""
        event_data = {
            'session_id': self.test_session_id,
            'event_type': 'balloon_risk',
            'action': 'pump',
            'balloon_id': 1,
            'pump_number': 5,
            'timestamp': timezone.now().isoformat(),
            'reaction_time_ms': 750
        }
        
        result = self.event_logger.process(event_data)
        
        self.assertTrue(result['processed'])
        self.assertIn('event_id', result)
        
        # Verify event was stored
        event = BalloonRiskEvent.objects.get(event_id=result['event_id'])
        self.assertEqual(event.action, 'pump')
        self.assertEqual(event.balloon_id, 1)
        self.assertEqual(event.pump_number, 5)
    
    def test_log_invalid_event_missing_required_field(self):
        """Test logging an event with missing required fields."""
        event_data = {
            'session_id': self.test_session_id,
            'event_type': 'balloon_risk',
            # Missing 'action' field
            'balloon_id': 1,
            'timestamp': timezone.now().isoformat()
        }
        
        result = self.event_logger.process(event_data)
        
        self.assertFalse(result['processed'])
        self.assertIn('error', result)
        self.assertIn('action', result['error'])
    
    def test_log_event_invalid_session(self):
        """Test logging an event with invalid session ID."""
        event_data = {
            'session_id': 'nonexistent_session',
            'event_type': 'balloon_risk',
            'action': 'pump',
            'balloon_id': 1,
            'timestamp': timezone.now().isoformat()
        }
        
        result = self.event_logger.process(event_data)
        
        self.assertFalse(result['processed'])
        self.assertIn('error', result)
    
    def test_batch_event_logging(self):
        """Test batch logging of multiple events."""
        events = []
        for i in range(5):
            events.append({
                'session_id': self.test_session_id,
                'event_type': 'balloon_risk',
                'action': 'pump',
                'balloon_id': 1,
                'pump_number': i + 1,
                'timestamp': timezone.now().isoformat(),
                'reaction_time_ms': 500 + i * 100
            })
        
        result = self.event_logger.batch_log_events(events)
        
        self.assertEqual(result['total_events'], 5)
        self.assertEqual(result['successful'], 5)
        self.assertEqual(result['failed'], 0)
        
        # Verify all events were stored
        stored_events = BalloonRiskEvent.objects.filter(session=self.test_session)
        self.assertEqual(stored_events.count(), 5)


class TestMetricExtractor(TestCase):
    """Test cases for MetricExtractor agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.metric_extractor = MetricExtractor()
        self.test_session_id = "test_session_metrics"
        
        # Create test session with events
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="test_user_metrics",
            game_type="balloon_risk",
            started_at=timezone.now() - timedelta(minutes=10),
            status="completed",
            duration_ms=600000  # 10 minutes
        )
        
        # Create test events
        self._create_test_events()
    
    def _create_test_events(self):
        """Create test balloon risk events."""
        base_time = timezone.now() - timedelta(minutes=10)
        
        # Create pump events for 3 balloons
        for balloon_id in range(1, 4):
            for pump_num in range(1, 8 + balloon_id):  # Varying pump counts
                BalloonRiskEvent.objects.create(
                    session=self.test_session,
                    event_type='balloon_risk',
                    action='pump',
                    balloon_id=balloon_id,
                    pump_number=pump_num,
                    timestamp=base_time + timedelta(seconds=balloon_id * 30 + pump_num * 2),
                    reaction_time_ms=500 + pump_num * 50,
                    event_id=f"event_{balloon_id}_{pump_num}"
                )
            
            # Create pop event for balloon 1 and 2
            if balloon_id <= 2:
                BalloonRiskEvent.objects.create(
                    session=self.test_session,
                    event_type='balloon_risk',
                    action='pop',
                    balloon_id=balloon_id,
                    pump_number=8 + balloon_id,
                    timestamp=base_time + timedelta(seconds=balloon_id * 30 + (8 + balloon_id) * 2),
                    event_id=f"pop_{balloon_id}"
                )
            else:
                # Cash out balloon 3
                BalloonRiskEvent.objects.create(
                    session=self.test_session,
                    event_type='balloon_risk',
                    action='cash_out',
                    balloon_id=balloon_id,
                    pump_number=8 + balloon_id,
                    timestamp=base_time + timedelta(seconds=balloon_id * 30 + (8 + balloon_id) * 2),
                    event_id=f"cash_{balloon_id}"
                )
    
    def test_extract_balloon_risk_metrics(self):
        """Test extraction of balloon risk metrics."""
        result = self.metric_extractor.extract_session_metrics(self.test_session_id)
        
        self.assertTrue(result['processed'])
        self.assertIn('balloon_risk', result)
        
        balloon_metrics = result['balloon_risk']
        
        # Check that key metrics are present
        self.assertIn('risk_tolerance', balloon_metrics)
        self.assertIn('consistency', balloon_metrics)
        self.assertIn('learning', balloon_metrics)
        
        # Verify specific metrics
        risk_metrics = balloon_metrics['risk_tolerance']
        self.assertIn('average_pumps', risk_metrics)
        self.assertIn('risk_escalation', risk_metrics)
        
        # Average pumps should be reasonable (around 9-10 based on test data)
        self.assertGreater(risk_metrics['average_pumps'], 5)
        self.assertLess(risk_metrics['average_pumps'], 15)
    
    def test_extract_metrics_insufficient_data(self):
        """Test metric extraction with insufficient data."""
        # Create session with very few events
        minimal_session = BehavioralSession.objects.create(
            session_id="minimal_session",
            user_id="test_user_minimal",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="active"
        )
        
        # Create only 2 events (below minimum threshold)
        for i in range(2):
            BalloonRiskEvent.objects.create(
                session=minimal_session,
                event_type='balloon_risk',
                action='pump',
                balloon_id=1,
                pump_number=i + 1,
                timestamp=timezone.now(),
                event_id=f"minimal_{i}"
            )
        
        result = self.metric_extractor.extract_session_metrics("minimal_session")
        
        self.assertFalse(result['processed'])
        self.assertIn('error', result)
        self.assertIn('Insufficient events', result['error'])
    
    def test_batch_metric_extraction(self):
        """Test batch extraction of metrics for multiple sessions."""
        # Create additional test session
        session2 = BehavioralSession.objects.create(
            session_id="test_session_2",
            user_id="test_user_2",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Add some events to session2
        for i in range(15):
            BalloonRiskEvent.objects.create(
                session=session2,
                event_type='balloon_risk',
                action='pump',
                balloon_id=1,
                pump_number=i + 1,
                timestamp=timezone.now(),
                event_id=f"batch_{i}"
            )
        
        session_ids = [self.test_session_id, "test_session_2"]
        results = self.metric_extractor.batch_extract_metrics(session_ids)
        
        self.assertEqual(len(results), 2)
        self.assertIn(self.test_session_id, results)
        self.assertIn("test_session_2", results)
        
        # Both should be processed successfully
        self.assertTrue(results[self.test_session_id]['processed'])
        self.assertTrue(results["test_session_2"]['processed'])


class TestTraitInferencer(TestCase):
    """Test cases for TraitInferencer agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trait_inferencer = TraitInferencer()
        self.test_session_id = "test_session_traits"
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="test_user_traits",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create test metrics
        self._create_test_metrics()
    
    def _create_test_metrics(self):
        """Create test behavioral metrics."""
        metrics_data = [
            ('balloon_risk_risk_tolerance_average_pumps', 8.5),
            ('balloon_risk_risk_tolerance_risk_escalation', 0.12),
            ('balloon_risk_consistency_behavioral_consistency', 0.75),
            ('balloon_risk_learning_adaptation_rate', 0.68),
            ('balloon_risk_learning_learning_curve', 0.45),
            ('balloon_risk_learning_feedback_response', 0.82),
            ('balloon_risk_emotion_stress_response', 0.35),
            ('balloon_risk_emotion_recovery_time', 3.2),
            ('balloon_risk_emotion_post_loss_behavior', 0.71)
        ]
        
        for metric_name, metric_value in metrics_data:
            BehavioralMetric.objects.create(
                session=self.test_session,
                metric_type='game_level',
                metric_name=metric_name,
                game_type='balloon_risk',
                metric_value=metric_value,
                metric_unit='score',
                sample_size=25,
                calculation_method='MetricExtractor Agent',
                calculation_timestamp=timezone.now(),
                data_version='1.0'
            )
    
    def test_infer_session_traits(self):
        """Test trait inference for a session."""
        result = self.trait_inferencer.infer_session_traits(self.test_session_id)
        
        self.assertTrue(result['processed'])
        self.assertIn('trait_scores', result)
        self.assertIn('confidence_scores', result)
        
        trait_scores = result['trait_scores']
        confidence_scores = result['confidence_scores']
        
        # Check that main traits are inferred
        expected_traits = ['risk_tolerance', 'learning_ability', 'emotion_regulation']
        for trait in expected_traits:
            if trait in trait_scores:  # May not be present if confidence too low
                self.assertGreaterEqual(trait_scores[trait], 0.0)
                self.assertLessEqual(trait_scores[trait], 1.0)
                self.assertGreaterEqual(confidence_scores[trait], 0.0)
                self.assertLessEqual(confidence_scores[trait], 1.0)
    
    def test_infer_traits_insufficient_metrics(self):
        """Test trait inference with insufficient metrics."""
        # Create session with minimal metrics
        minimal_session = BehavioralSession.objects.create(
            session_id="minimal_traits_session",
            user_id="test_user_minimal_traits",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create only one metric
        BehavioralMetric.objects.create(
            session=minimal_session,
            metric_type='game_level',
            metric_name='balloon_risk_risk_tolerance_average_pumps',
            game_type='balloon_risk',
            metric_value=5.0,
            metric_unit='score',
            sample_size=5,
            calculation_method='MetricExtractor Agent',
            calculation_timestamp=timezone.now(),
            data_version='1.0'
        )
        
        result = self.trait_inferencer.infer_session_traits("minimal_traits_session")
        
        # Should still process but may have low confidence or fewer traits
        self.assertTrue(result['processed'])
        # Confidence scores may be low due to insufficient data
    
    def test_validate_trait_profile(self):
        """Test trait profile validation."""
        # First infer traits
        result = self.trait_inferencer.infer_session_traits(self.test_session_id)
        
        if result['processed'] and result['trait_scores']:
            # Test validation
            trait_scores = result['trait_scores']
            confidence_scores = result['confidence_scores']
            
            validation_result = self.trait_inferencer.validate_trait_profile(
                self.test_session_id, trait_scores, confidence_scores
            )
            
            self.assertIn('is_valid', validation_result)
            self.assertIn('confidence_score', validation_result)
            self.assertIn('data_quality_score', validation_result)


class TestReportGenerator(TestCase):
    """Test cases for ReportGenerator agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.report_generator = ReportGenerator()
        self.test_session_id = "test_session_reports"
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="test_user_reports",
            game_type="balloon_risk",
            started_at=timezone.now() - timedelta(hours=1),
            status="completed",
            duration_ms=3600000  # 1 hour
        )
        
        # Create test trait profiles
        self._create_test_trait_profiles()
    
    def _create_test_trait_profiles(self):
        """Create test trait profiles."""
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
                data_version='1.0',
                created_at=timezone.now()
            )
    
    def test_generate_session_report(self):
        """Test generation of session report."""
        result = self.report_generator.generate_session_report(self.test_session_id)
        
        self.assertTrue(result['generated'])
        self.assertIn('report', result)
        
        report = result['report']
        
        # Check report structure
        self.assertIn('session_summary', report)
        self.assertIn('trait_profiles', report)
        self.assertIn('recommendations', report)
        self.assertIn('metadata', report)
        
        # Check session summary
        session_summary = report['session_summary']
        self.assertEqual(session_summary['session_id'], self.test_session_id)
        self.assertIn('duration_minutes', session_summary)
        
        # Check trait profiles
        trait_profiles = report['trait_profiles']
        self.assertGreater(len(trait_profiles), 0)
        
        for trait_profile in trait_profiles:
            self.assertIn('trait_name', trait_profile)
            self.assertIn('score', trait_profile)
            self.assertIn('confidence', trait_profile)
            self.assertIn('interpretation', trait_profile)
    
    def test_generate_report_no_traits(self):
        """Test report generation for session without trait profiles."""
        # Create session without trait profiles
        empty_session = BehavioralSession.objects.create(
            session_id="empty_session",
            user_id="test_user_empty",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        result = self.report_generator.generate_session_report("empty_session")
        
        # Should still generate a report but with warnings
        self.assertTrue(result['generated'])
        self.assertIn('warnings', result)
    
    def test_generate_comparative_report(self):
        """Test generation of comparative report."""
        # Create second session for comparison
        session2 = BehavioralSession.objects.create(
            session_id="comparison_session",
            user_id="test_user_reports",  # Same user
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create trait profiles for second session
        TraitProfile.objects.create(
            session=session2,
            trait_name='risk_tolerance',
            trait_score=0.65,
            confidence_score=0.80,
            calculation_method='TraitInferencer Agent',
            data_version='1.0',
            created_at=timezone.now()
        )
        
        session_ids = [self.test_session_id, "comparison_session"]
        result = self.report_generator.generate_comparative_report(session_ids)
        
        self.assertTrue(result['generated'])
        self.assertIn('comparison_analysis', result['report'])
        self.assertIn('trend_analysis', result['report'])


class TestAgentIntegration(TestCase):
    """Integration tests for agent workflows."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.event_logger = EventLogger()
        self.metric_extractor = MetricExtractor()
        self.trait_inferencer = TraitInferencer()
        self.report_generator = ReportGenerator()
        
        self.test_session_id = "integration_test_session"
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="integration_test_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="active"
        )
    
    def test_complete_workflow(self):
        """Test complete workflow from event logging to report generation."""
        # Step 1: Log events
        events = []
        for balloon_id in range(1, 4):
            for pump_num in range(1, 10):
                events.append({
                    'session_id': self.test_session_id,
                    'event_type': 'balloon_risk',
                    'action': 'pump',
                    'balloon_id': balloon_id,
                    'pump_number': pump_num,
                    'timestamp': timezone.now().isoformat(),
                    'reaction_time_ms': 500 + pump_num * 50
                })
            
            # Add pop or cash out
            action = 'pop' if balloon_id <= 2 else 'cash_out'
            events.append({
                'session_id': self.test_session_id,
                'event_type': 'balloon_risk',
                'action': action,
                'balloon_id': balloon_id,
                'pump_number': 10,
                'timestamp': timezone.now().isoformat()
            })
        
        # Log all events
        event_result = self.event_logger.batch_log_events(events)
        self.assertEqual(event_result['successful'], len(events))
        
        # Step 2: Extract metrics
        metrics_result = self.metric_extractor.extract_session_metrics(self.test_session_id)
        self.assertTrue(metrics_result['processed'])
        
        # Step 3: Infer traits
        traits_result = self.trait_inferencer.infer_session_traits(self.test_session_id)
        self.assertTrue(traits_result['processed'])
        
        # Step 4: Generate report
        report_result = self.report_generator.generate_session_report(self.test_session_id)
        self.assertTrue(report_result['generated'])
        
        # Verify complete workflow
        self.assertIn('trait_profiles', report_result['report'])
        trait_profiles = report_result['report']['trait_profiles']
        self.assertGreater(len(trait_profiles), 0)


if __name__ == '__main__':
    unittest.main()
