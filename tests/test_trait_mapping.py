"""
Comprehensive tests for trait mapping components.

Tests cover TraitMapper, ScientificTraitModel, and TraitValidation
with various scenarios including edge cases and scientific validation.
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from trait_mapping.trait_mappings import TraitMapper, TraitDimension
from trait_mapping.scientific_models import (
    ScientificTraitModel, RiskToleranceModel, 
    LearningAbilityModel, EmotionRegulationModel
)
from trait_mapping.validation import TraitValidation, ValidationCriteria, ValidationResult
from behavioral_data.models import BehavioralSession, BehavioralMetric
from ai_model.models import TraitProfile


class TestTraitMapper(TestCase):
    """Test cases for TraitMapper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trait_mapper = TraitMapper()
        self.test_session_id = "test_trait_mapping_session"
        
        # Create test session
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user_id="test_trait_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        # Create comprehensive test metrics
        self._create_test_metrics()
    
    def _create_test_metrics(self):
        """Create comprehensive test metrics for trait mapping."""
        metrics_data = [
            # Risk tolerance metrics
            ('balloon_risk_risk_tolerance_average_pumps', 8.5),
            ('balloon_risk_risk_tolerance_risk_escalation', 0.12),
            ('balloon_risk_consistency_behavioral_consistency', 0.75),
            ('balloon_risk_learning_adaptation_rate', 0.68),
            
            # Learning metrics
            ('balloon_risk_learning_learning_curve', 0.45),
            ('balloon_risk_learning_feedback_response', 0.82),
            ('memory_cards_learning_improvement_rate', 0.71),
            
            # Emotion regulation metrics
            ('balloon_risk_emotion_stress_response', 0.35),
            ('balloon_risk_emotion_recovery_time', 3.2),
            ('balloon_risk_emotion_post_loss_behavior', 0.71),
            
            # Attention metrics
            ('reaction_timer_attention_reaction_time_consistency', 0.88),
            ('reaction_timer_attention_sustained_attention', 0.79),
            ('memory_cards_attention_focus_duration', 0.83),
            
            # Decision making metrics
            ('balloon_risk_decision_making_decision_speed', 0.67),
            ('reaction_timer_decision_making_response_accuracy', 0.91)
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
    
    def test_map_session_traits_comprehensive(self):
        """Test comprehensive trait mapping for a session."""
        result = self.trait_mapper.map_session_traits(self.test_session_id)
        
        self.assertIn('session_id', result)
        self.assertEqual(result['session_id'], self.test_session_id)
        self.assertIn('trait_scores', result)
        self.assertIn('confidence_scores', result)
        self.assertIn('metadata', result)
        
        trait_scores = result['trait_scores']
        confidence_scores = result['confidence_scores']
        
        # Check that traits are calculated
        expected_traits = ['risk_tolerance', 'learning', 'emotion_regulation', 'attention', 'decision_making']
        
        for trait in expected_traits:
            if trait in trait_scores:
                # Verify score is in valid range
                self.assertGreaterEqual(trait_scores[trait], 0.0)
                self.assertLessEqual(trait_scores[trait], 1.0)
                
                # Verify confidence is reasonable
                self.assertIn(trait, confidence_scores)
                self.assertGreaterEqual(confidence_scores[trait], 0.0)
                self.assertLessEqual(confidence_scores[trait], 1.0)
    
    def test_map_traits_insufficient_metrics(self):
        """Test trait mapping with insufficient metrics."""
        # Create session with minimal metrics
        minimal_session = BehavioralSession.objects.create(
            session_id="minimal_mapping_session",
            user_id="minimal_user",
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
        
        result = self.trait_mapper.map_session_traits("minimal_mapping_session")
        
        # Should still return results but may have fewer traits due to low confidence
        self.assertIn('trait_scores', result)
        self.assertIn('confidence_scores', result)
    
    def test_trait_explanation_generation(self):
        """Test generation of trait explanations."""
        # Test risk tolerance explanation
        explanation = self.trait_mapper.get_trait_explanation(
            TraitDimension.RISK_TOLERANCE, 0.8
        )
        
        self.assertIn('trait_dimension', explanation)
        self.assertIn('score', explanation)
        self.assertIn('level', explanation)
        self.assertIn('description', explanation)
        self.assertIn('interpretation', explanation)
        self.assertIn('scientific_basis', explanation)
        
        self.assertEqual(explanation['trait_dimension'], 'risk_tolerance')
        self.assertEqual(explanation['score'], 0.8)
        self.assertEqual(explanation['level'], 'Very High')
    
    def test_normalization_methods(self):
        """Test different normalization methods."""
        test_metrics = {
            'metric1': 10.0,
            'metric2': 15.0,
            'metric3': 20.0
        }
        
        # Test z-score normalization
        normalized_z = self.trait_mapper._normalize_metrics(test_metrics, "z_score")
        self.assertEqual(len(normalized_z), 3)
        
        # Test min-max normalization
        normalized_minmax = self.trait_mapper._normalize_metrics(test_metrics, "min_max")
        self.assertEqual(len(normalized_minmax), 3)
        
        # Test percentile normalization
        normalized_percentile = self.trait_mapper._normalize_metrics(test_metrics, "percentile")
        self.assertEqual(len(normalized_percentile), 3)
    
    def test_weight_functions(self):
        """Test different weight functions."""
        test_values = [0.5, 0.7, 0.8, 0.6]
        
        # Test weighted average
        result_weighted = self.trait_mapper._weighted_average(test_values, TraitDimension.RISK_TOLERANCE)
        self.assertGreaterEqual(result_weighted, 0.0)
        self.assertLessEqual(result_weighted, 1.0)
        
        # Test learning curve analysis
        test_metrics = {
            'learning_curve': 0.6,
            'adaptation_rate': 0.7,
            'feedback_response': 0.8
        }
        result_learning = self.trait_mapper._learning_curve_analysis(test_metrics)
        self.assertGreaterEqual(result_learning, 0.0)
        
        # Test emotion regulation model
        emotion_metrics = {
            'stress_response': 0.3,
            'recovery_time': 2.5,
            'post_loss_behavior': 0.8
        }
        result_emotion = self.trait_mapper._emotion_regulation_model(emotion_metrics)
        self.assertGreaterEqual(result_emotion, 0.0)
        self.assertLessEqual(result_emotion, 1.0)


class TestScientificTraitModel(TestCase):
    """Test cases for ScientificTraitModel and specific models."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scientific_model = ScientificTraitModel()
        self.risk_model = RiskToleranceModel()
        self.learning_model = LearningAbilityModel()
        self.emotion_model = EmotionRegulationModel()
    
    def test_risk_tolerance_model_prediction(self):
        """Test risk tolerance model prediction."""
        behavioral_data = {
            'balloon_risk_risk_tolerance_average_pumps': 8.5,
            'balloon_risk_risk_tolerance_risk_escalation': 0.12,
            'balloon_risk_consistency_behavioral_consistency': 0.75,
            'balloon_risk_learning_adaptation_rate': 0.68
        }
        
        result = self.risk_model.predict(behavioral_data)
        
        self.assertIn('risk_tolerance', result)
        self.assertIn('risk_category', result)
        self.assertIn('confidence', result)
        self.assertIn('component_scores', result)
        
        # Verify score is in valid range
        self.assertGreaterEqual(result['risk_tolerance'], 0.0)
        self.assertLessEqual(result['risk_tolerance'], 1.0)
        
        # Verify confidence is reasonable
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
    
    def test_learning_ability_model_prediction(self):
        """Test learning ability model prediction."""
        behavioral_data = {
            'balloon_risk_learning_learning_curve': 0.45,
            'balloon_risk_learning_adaptation_rate': 0.68,
            'balloon_risk_learning_feedback_response': 0.82
        }
        
        result = self.learning_model.predict(behavioral_data)
        
        self.assertIn('learning_ability', result)
        self.assertIn('learning_category', result)
        self.assertIn('confidence', result)
        
        # Verify score is in valid range
        self.assertGreaterEqual(result['learning_ability'], 0.0)
        self.assertLessEqual(result['learning_ability'], 1.0)
    
    def test_emotion_regulation_model_prediction(self):
        """Test emotion regulation model prediction."""
        behavioral_data = {
            'balloon_risk_emotion_stress_response': 0.35,
            'balloon_risk_emotion_recovery_time': 3.2,
            'balloon_risk_emotion_post_loss_behavior': 0.71
        }
        
        result = self.emotion_model.predict(behavioral_data)
        
        self.assertIn('emotion_regulation', result)
        self.assertIn('regulation_category', result)
        self.assertIn('confidence', result)
        
        # Verify score is in valid range
        self.assertGreaterEqual(result['emotion_regulation'], 0.0)
        self.assertLessEqual(result['emotion_regulation'], 1.0)
    
    def test_confidence_intervals(self):
        """Test confidence interval calculations."""
        # Test risk tolerance confidence interval
        ci_lower, ci_upper = self.risk_model.get_confidence_interval(0.75, 0.95)
        
        self.assertLessEqual(ci_lower, 0.75)
        self.assertGreaterEqual(ci_upper, 0.75)
        self.assertLess(ci_lower, ci_upper)
        self.assertGreaterEqual(ci_lower, 0.0)
        self.assertLessEqual(ci_upper, 1.0)
    
    def test_predict_all_traits(self):
        """Test prediction of all traits using scientific models."""
        comprehensive_data = {
            # Risk tolerance data
            'balloon_risk_risk_tolerance_average_pumps': 8.5,
            'balloon_risk_risk_tolerance_risk_escalation': 0.12,
            'balloon_risk_consistency_behavioral_consistency': 0.75,
            'balloon_risk_learning_adaptation_rate': 0.68,
            
            # Learning data
            'balloon_risk_learning_learning_curve': 0.45,
            'balloon_risk_learning_feedback_response': 0.82,
            
            # Emotion regulation data
            'balloon_risk_emotion_stress_response': 0.35,
            'balloon_risk_emotion_recovery_time': 3.2,
            'balloon_risk_emotion_post_loss_behavior': 0.71
        }
        
        results = self.scientific_model.predict_all_traits(comprehensive_data)
        
        self.assertIn('risk_tolerance', results)
        self.assertIn('learning_ability', results)
        self.assertIn('emotion_regulation', results)
        self.assertIn('metadata', results)
        
        # Verify each trait prediction has required fields
        for trait_name in ['risk_tolerance', 'learning_ability', 'emotion_regulation']:
            trait_result = results[trait_name]
            if 'error' not in trait_result:
                self.assertIn(trait_name, trait_result)
                self.assertIn('confidence', trait_result)
    
    def test_model_validation(self):
        """Test model validation functionality."""
        test_predictions = {
            'risk_tolerance': {'risk_tolerance': 0.75, 'confidence': 0.85},
            'learning_ability': {'learning_ability': 0.68, 'confidence': 0.78},
            'emotion_regulation': {'emotion_regulation': 0.82, 'confidence': 0.88}
        }
        
        validation_results = self.scientific_model.validate_predictions(test_predictions)
        
        self.assertIn('overall_validity', validation_results)
        self.assertIn('individual_validations', validation_results)
        self.assertIn('confidence_summary', validation_results)
        
        # Check individual validations
        for trait_name in test_predictions.keys():
            self.assertIn(trait_name, validation_results['individual_validations'])


class TestTraitValidation(TestCase):
    """Test cases for TraitValidation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Create test user
        self.test_user = User.objects.create_user(
            username='test_validation_user',
            password='testpass123',
            email='test_validation@example.com'
        )
        
        self.validation_criteria = ValidationCriteria(
            min_confidence=0.7,
            min_data_completeness=0.8,
            min_sample_size=10
        )
        self.trait_validation = TraitValidation(self.validation_criteria)
        
        self.test_session_id = "test_validation_session"
        
        # Create test session with the test user
        self.test_session = BehavioralSession.objects.create(
            session_id=self.test_session_id,
            user=self.test_user,  # Use the created user instance
            game_type="balloon_risk",
            started_at=timezone.now() - timedelta(minutes=30),
            status="completed",
            duration_ms=1800000  # 30 minutes
        )
        
        # Create test events and metrics
        self._create_validation_test_data()
    
    def _create_validation_test_data(self):
        """Create test data for validation."""
        # Create sufficient events
        from behavioral_data.models import BalloonRiskEvent
        
        for i in range(20):
            BalloonRiskEvent.objects.create(
                session=self.test_session,
                event_type='balloon_risk',
                action='pump',
                balloon_id=1,
                pump_number=i + 1,
                timestamp=timezone.now() - timedelta(minutes=30-i),
                reaction_time_ms=500 + i * 25,
                event_id=f"validation_event_{i}"
            )
        
        # Create comprehensive metrics
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
    
    def test_validate_trait_profile_comprehensive(self):
        """Test comprehensive trait profile validation."""
        trait_scores = {
            'risk_tolerance': 0.75,
            'learning_ability': 0.68,
            'emotion_regulation': 0.82
        }
        
        confidence_scores = {
            'risk_tolerance': 0.85,
            'learning_ability': 0.78,
            'emotion_regulation': 0.88
        }
        
        result = self.trait_validation.validate_trait_profile(
            self.test_session_id, trait_scores, confidence_scores
        )
        
        self.assertIsInstance(result, ValidationResult)
        self.assertIn('is_valid', result.__dict__)
        self.assertIn('confidence_score', result.__dict__)
        self.assertIn('data_quality_score', result.__dict__)
        self.assertIn('reliability_score', result.__dict__)
        self.assertIn('validity_score', result.__dict__)
        
        # Check that scores are in valid ranges
        self.assertGreaterEqual(result.confidence_score, 0.0)
        self.assertLessEqual(result.confidence_score, 1.0)
        self.assertGreaterEqual(result.data_quality_score, 0.0)
        self.assertLessEqual(result.data_quality_score, 1.0)
    
    def test_validate_low_quality_data(self):
        """Test validation with low quality data."""
        # Create session with minimal data
        low_quality_session = BehavioralSession.objects.create(
            session_id="low_quality_session",
            user_id="low_quality_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed",
            duration_ms=15000  # Very short duration
        )
        
        # Create minimal events
        from behavioral_data.models import BalloonRiskEvent
        for i in range(3):  # Below minimum threshold
            BalloonRiskEvent.objects.create(
                session=low_quality_session,
                event_type='balloon_risk',
                action='pump',
                balloon_id=1,
                pump_number=i + 1,
                timestamp=timezone.now(),
                event_id=f"low_quality_{i}"
            )
        
        trait_scores = {'risk_tolerance': 0.5}
        confidence_scores = {'risk_tolerance': 0.4}  # Low confidence
        
        result = self.trait_validation.validate_trait_profile(
            "low_quality_session", trait_scores, confidence_scores
        )
        
        # Should identify low quality
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.warnings), 0)
        self.assertGreater(len(result.recommendations), 0)
    
    def test_temporal_stability_validation(self):
        """Test temporal stability validation."""
        # Create previous session for the same user
        previous_session = BehavioralSession.objects.create(
            session_id="previous_session",
            user_id="test_validation_user",  # Same user
            game_type="balloon_risk",
            started_at=timezone.now() - timedelta(days=7),
            status="completed"
        )
        
        # Create previous trait profile
        TraitProfile.objects.create(
            session=previous_session,
            trait_name='risk_tolerance',
            trait_score=0.70,  # Similar to current
            confidence_score=0.80,
            calculation_method='TraitInferencer Agent',
            data_version='1.0',
            created_at=timezone.now() - timedelta(days=7)
        )
        
        current_scores = {'risk_tolerance': 0.75}  # Small change
        confidence_scores = {'risk_tolerance': 0.85}
        
        result = self.trait_validation.validate_trait_profile(
            self.test_session_id, current_scores, confidence_scores
        )
        
        # Should show good temporal stability
        self.assertGreaterEqual(result.validity_score, 0.5)
    
    def test_validation_summary(self):
        """Test validation summary functionality."""
        # Perform multiple validations
        for i in range(5):
            trait_scores = {'risk_tolerance': 0.7 + i * 0.05}
            confidence_scores = {'risk_tolerance': 0.8 + i * 0.02}
            
            self.trait_validation.validate_trait_profile(
                self.test_session_id, trait_scores, confidence_scores
            )
        
        summary = self.trait_validation.get_validation_summary()
        
        self.assertIn('total_validations', summary)
        self.assertIn('recent_validity_rate', summary)
        self.assertIn('average_confidence', summary)
        self.assertIn('average_quality', summary)
        
        self.assertEqual(summary['total_validations'], 5)
    
    def test_outlier_detection(self):
        """Test outlier detection in metrics."""
        # Create metrics with outliers
        normal_values = [5.0, 6.0, 7.0, 8.0, 9.0]
        outlier_values = [5.0, 6.0, 7.0, 50.0, 9.0]  # 50.0 is an outlier
        
        # Create session with outlier metrics
        outlier_session = BehavioralSession.objects.create(
            session_id="outlier_session",
            user_id="outlier_user",
            game_type="balloon_risk",
            started_at=timezone.now(),
            status="completed"
        )
        
        for i, value in enumerate(outlier_values):
            BehavioralMetric.objects.create(
                session=outlier_session,
                metric_type='game_level',
                metric_name=f'test_metric_{i}',
                game_type='balloon_risk',
                metric_value=value,
                metric_unit='score',
                sample_size=10,
                calculation_method='Test',
                calculation_timestamp=timezone.now(),
                data_version='1.0'
            )
        
        # Test outlier detection
        outlier_ratio = self.trait_validation._detect_outliers(
            BehavioralMetric.objects.filter(session=outlier_session)
        )
        
        self.assertGreater(outlier_ratio, 0.0)  # Should detect outliers


if __name__ == '__main__':
    unittest.main()
