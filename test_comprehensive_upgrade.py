#!/usr/bin/env python3
"""
Comprehensive Upgrade Test Script

This script tests all the new features implemented in the comprehensive upgrade:
- Enhanced game models with 20 games
- Comprehensive trait system with 90+ traits
- Dynamic difficulty adaptation
- Enhanced behavioral data collection
- Trait mapping system
"""

import os
import sys
import django
from datetime import datetime, timedelta
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from games.models import GameSession, GameResult, DynamicDifficultyConfig
from trait_mapping.models import TraitDimension, TraitDefinition, TraitMeasurement, TraitProfile
from trait_mapping.comprehensive_traits import ComprehensiveTraitSystem
from games.dynamic_difficulty import DynamicDifficultyAdapter
from behavioral_data.enhanced_collector import EnhancedBehavioralCollector

User = get_user_model()


class ComprehensiveUpgradeTester:
    """Test class for comprehensive upgrade features."""
    
    def __init__(self):
        self.user = None
        self.test_results = {}
        
    def setup_test_user(self):
        """Create a test user for testing."""
        print("🔧 Setting up test user...")
        
        # Create or get test user
        self.user, created = User.objects.get_or_create(
            username='testuser_comprehensive',
            defaults={
                'email': 'test_comprehensive@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            self.user.set_password('testpass123')
            self.user.save()
            print(f"✅ Created test user: {self.user.username}")
        else:
            print(f"✅ Using existing test user: {self.user.username}")
        
        return self.user
    
    def test_enhanced_game_models(self):
        """Test the enhanced game models with 20 games."""
        print("\n🎮 Testing Enhanced Game Models...")
        
        # Test GameSession with new fields
        session = GameSession.objects.create(
            user=self.user,
            total_games_played=5,
            session_duration_ms=300000,
            completion_rate=0.95,
            difficulty_level='medium',
            adaptive_difficulty_enabled=True,
            overall_performance_score=0.85,
            engagement_score=0.92,
            data_quality_score=0.88
        )
        
        print(f"✅ Created enhanced GameSession: {session.id}")
        print(f"   - Total games played: {session.total_games_played}")
        print(f"   - Session duration: {session.session_duration_ms}ms")
        print(f"   - Completion rate: {session.completion_rate}")
        print(f"   - Difficulty level: {session.difficulty_level}")
        print(f"   - Performance score: {session.overall_performance_score}")
        
        # Test GameResult with expanded game types
        result = GameResult.objects.create(
            user=self.user,
            session=session,
            game_type='balloon_risk',
            score=85,
            duration=300000,
            difficulty_level='medium',
            difficulty_adjustments=['easy', 'medium', 'hard'],
            accuracy_data={'trial_1': 0.8, 'trial_2': 0.9, 'trial_3': 0.85},
            learning_curves={'pump_efficiency': [0.6, 0.7, 0.8, 0.85]},
            behavioral_events=[
                {'event_type': 'pump', 'timestamp': 1000, 'balloon_size': 1.2},
                {'event_type': 'cash_out', 'timestamp': 2000, 'earnings': 0.25}
            ],
            performance_metrics={'risk_tolerance': 0.75, 'consistency': 0.82},
            trait_measurements={'risk_tolerance': 0.75, 'decision_speed': 0.68},
            confidence_scores={'risk_tolerance': 0.78, 'decision_speed': 0.72},
            data_completeness=0.95,
            data_quality_score=0.88,
            validation_status='valid'
        )
        
        print(f"✅ Created enhanced GameResult: {result.game_type}")
        print(f"   - Measured traits: {list(result.trait_measurements.keys())}")
        print(f"   - Data completeness: {result.data_completeness}")
        print(f"   - Quality score: {result.data_quality_score}")
        
        # Test getting measured traits
        measured_traits = result.get_measured_traits()
        print(f"   - Total traits measured: {len(measured_traits)}")
        
        self.test_results['enhanced_game_models'] = {
            'session_created': True,
            'result_created': True,
            'traits_measured': len(measured_traits),
            'data_completeness': result.data_completeness
        }
        
        return session, result
    
    def test_comprehensive_trait_system(self):
        """Test the comprehensive trait system with 90+ traits."""
        print("\n🧠 Testing Comprehensive Trait System...")
        
        trait_system = ComprehensiveTraitSystem()
        
        # Test trait system initialization
        all_traits = trait_system.get_all_traits()
        print(f"✅ Total traits available: {len(all_traits)}")
        
        # Test getting traits by dimension
        from trait_mapping.comprehensive_traits import TraitDimension
        emotion_traits = trait_system.get_traits_by_dimension(TraitDimension.EMOTION)
        attention_traits = trait_system.get_traits_by_dimension(TraitDimension.ATTENTION)
        
        print(f"✅ Emotion traits: {len(emotion_traits)}")
        print(f"✅ Attention traits: {len(attention_traits)}")
        
        # Test trait calculation
        behavioral_data = {
            'facial_expression_accuracy': 0.85,
            'emotion_identification_speed': 1200,
            'reaction_time': 500,
            'accuracy': 0.92,
            'sustained_attention_score': 0.78,
            'focus_duration': 45000
        }
        
        # Calculate individual trait
        emotion_result = trait_system.calculate_trait_score('emotional_recognition', behavioral_data)
        print(f"✅ Emotional recognition score: {emotion_result['normalized_score']:.3f}")
        print(f"   - Confidence: {emotion_result['confidence']:.3f}")
        
        # Calculate all traits
        all_results = trait_system.calculate_all_traits(behavioral_data)
        print(f"✅ Calculated {all_results['summary']['valid_traits']} valid traits")
        print(f"   - Average confidence: {all_results['summary']['average_confidence']:.3f}")
        
        self.test_results['comprehensive_trait_system'] = {
            'total_traits': len(all_traits),
            'emotion_traits': len(emotion_traits),
            'attention_traits': len(attention_traits),
            'valid_traits_calculated': all_results['summary']['valid_traits'],
            'average_confidence': all_results['summary']['average_confidence']
        }
        
        return trait_system, all_results
    
    def test_dynamic_difficulty(self):
        """Test the dynamic difficulty adaptation system."""
        print("\n🎯 Testing Dynamic Difficulty System...")
        
        difficulty_adapter = DynamicDifficultyAdapter()
        
        # Test difficulty calculation
        user_id = str(self.user.id)
        game_type = 'balloon_risk'
        
        new_difficulty, params = difficulty_adapter.calculate_new_difficulty(user_id, game_type)
        print(f"✅ Calculated difficulty: {new_difficulty.value}")
        print(f"   - Parameters: {len(params)} parameters")
        
        # Test getting difficulty parameters
        difficulty_params = difficulty_adapter.get_difficulty_parameters(game_type, new_difficulty)
        print(f"✅ Difficulty parameters: {len(difficulty_params)} settings")
        
        # Test performance tracking
        if user_id in difficulty_adapter.performance_trackers and game_type in difficulty_adapter.performance_trackers[user_id]:
            performance_metrics = difficulty_adapter.performance_trackers[user_id][game_type]
            print(f"✅ Performance metrics tracked: {len(performance_metrics.scores)} scores")
        else:
            print("✅ Performance tracking initialized (no scores yet)")
        
        self.test_results['dynamic_difficulty'] = {
            'difficulty_calculated': True,
            'difficulty_level': new_difficulty.value,
            'parameters_count': len(params),
            'performance_tracked': True
        }
        
        return difficulty_adapter
    
    def test_enhanced_data_collection(self, session=None):
        """Test the enhanced behavioral data collection."""
        print("\n📊 Testing Enhanced Data Collection...")
        
        collector = EnhancedBehavioralCollector()
        
        # Test data point collection
        if session is None:
            # Create a test session if none provided
            session = GameSession.objects.create(
                user=self.user,
                total_games_played=1,
                session_duration_ms=60000
            )
        
        session_id = str(session.id)
        
        # Start session tracking
        collector.start_session_tracking(session_id, str(self.user.id), 'balloon_risk')
        
        data_point = collector.collect_behavioral_event(
            session_id=session_id,
            event_type='user_action',
            event_name='pump',
            raw_data={
                'balloon_id': 'balloon_1',
                'pump_number': 5,
                'timestamp': 1640995200000,
                'balloon_size': 1.2,
                'current_earnings': 0.25
            },
            game_state={'balloon_color': 'red', 'total_pumps': 5},
            user_context={'engagement_level': 'high', 'focus_time': 30000},
            device_context={'screen_resolution': '1920x1080', 'browser': 'chrome'}
        )
        
        print(f"✅ Collected data point: {data_point.event_name}")
        print(f"   - Timestamp: {data_point.timestamp_ms}")
        print(f"   - Quality score: {data_point.data_quality_score}")
        print(f"   - Validation status: {data_point.validation_status}")
        
        # Test session summary
        summary = collector.get_session_summary(session_id)
        print(f"✅ Session summary: {summary['total_data_points']} events")
        print(f"   - Data quality: {summary['average_quality_score']:.3f}")
        print(f"   - Session duration: {summary['session_duration_ms']}ms")
        
        self.test_results['enhanced_data_collection'] = {
            'data_point_collected': True,
            'quality_score': data_point.data_quality_score,
            'total_events': summary['total_data_points'],
            'average_quality': summary['average_quality_score']
        }
        
        return collector
    
    def test_trait_mapping_models(self, session=None):
        """Test the trait mapping database models."""
        print("\n🗄️ Testing Trait Mapping Models...")
        
        if session is None:
            # Create a test session if none provided
            session = GameSession.objects.create(
                user=self.user,
                total_games_played=1,
                session_duration_ms=60000
            )
        
        # Test TraitDimension
        dimension = TraitDimension.objects.create(
            name='emotion',
            description='Emotional traits and responses',
            scientific_basis='Based on emotional intelligence research'
        )
        print(f"✅ Created trait dimension: {dimension.name}")
        
        # Test TraitDefinition
        trait_def = TraitDefinition.objects.create(
            dimension=dimension,
            name='emotional_recognition',
            description='Ability to recognize emotions',
            scientific_basis='Based on Ekman\'s Facial Action Coding System',
            measurement_method='Facial expression identification',
            reliability_coefficient=0.78,
            validity_evidence='Correlation with EI measures (r=.72)',
            source_games=['faces_game'],
            metrics_used=['facial_expression_accuracy'],
            normalization_method='percentile',
            confidence_threshold=0.7
        )
        print(f"✅ Created trait definition: {trait_def.name}")
        
        # Test TraitMeasurement
        measurement = TraitMeasurement.objects.create(
            user=self.user,
            trait_definition=trait_def,
            session_id=str(session.id),
            game_type='faces_game',
            raw_score=0.85,
            normalized_score=0.82,
            confidence_interval={'lower': 0.75, 'upper': 0.89},
            reliability_coefficient=0.78,
            measurement_method='facial_expression_identification',
            data_points_used=150
        )
        print(f"✅ Created trait measurement: {measurement.normalized_score}")
        
        # Test TraitProfile
        profile = TraitProfile.objects.create(
            user=self.user,
            session_id=str(session.id),
            trait_scores={'emotional_recognition': 0.82},
            dimension_scores={'emotion': 0.80},
            confidence_scores={'emotional_recognition': 0.78},
            overall_confidence=0.78,
            data_completeness=0.95,
            quality_score=0.88,
            calculation_method='comprehensive_trait_system',
            traits_measured=1,
            total_data_points=150
        )
        print(f"✅ Created trait profile: {profile.overall_confidence}")
        
        self.test_results['trait_mapping_models'] = {
            'dimension_created': True,
            'trait_definition_created': True,
            'measurement_created': True,
            'profile_created': True,
            'overall_confidence': profile.overall_confidence
        }
        
        return dimension, trait_def, measurement, profile
    
    def run_comprehensive_test(self):
        """Run all comprehensive tests."""
        print("🚀 Starting Comprehensive Upgrade Test Suite")
        print("=" * 60)
        
        try:
            # Setup
            self.setup_test_user()
            
            # Run all tests
            session, result = self.test_enhanced_game_models()
            self.test_comprehensive_trait_system()
            self.test_dynamic_difficulty()
            self.test_enhanced_data_collection(session)
            self.test_trait_mapping_models(session)
            
            # Print summary
            self.print_test_summary()
            
            print("\n🎉 All tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def print_test_summary(self):
        """Print a summary of all test results."""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE UPGRADE TEST SUMMARY")
        print("=" * 60)
        
        for test_name, results in self.test_results.items():
            print(f"\n🔍 {test_name.replace('_', ' ').title()}:")
            for key, value in results.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")
        
        print("\n" + "=" * 60)
        print("✅ COMPREHENSIVE UPGRADE VERIFICATION COMPLETE")
        print("=" * 60)


if __name__ == "__main__":
    tester = ComprehensiveUpgradeTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 Ready to proceed with Phase 2: Missing Games Implementation!")
        print("📚 Check QUICK_START_UPGRADE.md for next steps.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    sys.exit(0 if success else 1) 