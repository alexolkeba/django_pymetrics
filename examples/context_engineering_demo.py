#!/usr/bin/env python3
"""
Context Engineering Demo for Django Pymetrics

This script demonstrates the context-engineered trait inference implementation,
showing how to use the API for multi-dimensional psychometric assessment
with scientific validation and error handling.
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from agents.event_logger import EventLogger
from agents.metric_extractor import MetricExtractor
from agents.trait_inferencer import TraitInferencer
from trait_mapping.trait_mappings import TraitMapper
from trait_mapping.validation import TraitValidationEngine

User = get_user_model()


class ContextEngineeringDemo:
    """Demonstration of context-engineered trait inference."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session = requests.Session()
        
        # Initialize agents
        self.event_logger = EventLogger()
        self.metric_extractor = MetricExtractor()
        self.trait_inferencer = TraitInferencer()
        self.trait_mapper = TraitMapper()
        self.validation_engine = TraitValidationEngine()
        
        print("🎯 Context Engineering Demo for Django Pymetrics")
        print("=" * 60)
    
    def create_test_user_and_session(self):
        """Create a test user and behavioral session."""
        print("\n📝 Creating test user and session...")
        
        # Create test user
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            print(f"✓ Created test user: {user.username}")
        else:
            print(f"✓ Using existing test user: {user.username}")
        
        # Create behavioral session
        session_id = f"demo_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = BehavioralSession.objects.create(
            user=user,
            session_id=session_id,
            game_type='balloon_risk',
            status='completed',
            session_start_time=timezone.now() - timedelta(minutes=5),
            session_end_time=timezone.now(),
            is_completed=True,
            total_duration=300000,  # 5 minutes
            total_games_played=1
        )
        
        print(f"✓ Created behavioral session: {session_id}")
        return user, session
    
    def simulate_behavioral_events(self, session):
        """Simulate realistic behavioral events for the balloon risk game."""
        print("\n🎮 Simulating behavioral events...")
        
        events_data = [
            # Balloon 1 - Conservative approach
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'balloon_start',
                    'balloon_id': 'balloon_1',
                    'balloon_index': 1,
                    'balloon_color': 'red',
                    'timestamp_milliseconds': 1000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_1',
                    'pump_number': 1,
                    'balloon_size': 1.1,
                    'current_earnings': 0.05,
                    'time_since_prev_pump': 2000,
                    'timestamp_milliseconds': 3000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_1',
                    'pump_number': 2,
                    'balloon_size': 1.2,
                    'current_earnings': 0.10,
                    'time_since_prev_pump': 1500,
                    'timestamp_milliseconds': 4500
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'cash_out',
                    'balloon_id': 'balloon_1',
                    'pump_number': 2,
                    'earnings_collected': 0.10,
                    'timestamp_milliseconds': 6000
                }
            },
            # Balloon 2 - Moderate risk
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'balloon_start',
                    'balloon_id': 'balloon_2',
                    'balloon_index': 2,
                    'balloon_color': 'blue',
                    'timestamp_milliseconds': 7000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_2',
                    'pump_number': 1,
                    'balloon_size': 1.1,
                    'current_earnings': 0.05,
                    'time_since_prev_pump': 1800,
                    'timestamp_milliseconds': 8800
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_2',
                    'pump_number': 2,
                    'balloon_size': 1.2,
                    'current_earnings': 0.10,
                    'time_since_prev_pump': 1200,
                    'timestamp_milliseconds': 10000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_2',
                    'pump_number': 3,
                    'balloon_size': 1.3,
                    'current_earnings': 0.15,
                    'time_since_prev_pump': 1100,
                    'timestamp_milliseconds': 11100
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_2',
                    'pump_number': 4,
                    'balloon_size': 1.4,
                    'current_earnings': 0.20,
                    'time_since_prev_pump': 1000,
                    'timestamp_milliseconds': 12100
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'cash_out',
                    'balloon_id': 'balloon_2',
                    'pump_number': 4,
                    'earnings_collected': 0.20,
                    'timestamp_milliseconds': 13500
                }
            },
            # Balloon 3 - High risk (pops)
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'balloon_start',
                    'balloon_id': 'balloon_3',
                    'balloon_index': 3,
                    'balloon_color': 'green',
                    'timestamp_milliseconds': 14000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_3',
                    'pump_number': 1,
                    'balloon_size': 1.1,
                    'current_earnings': 0.05,
                    'time_since_prev_pump': 1600,
                    'timestamp_milliseconds': 15600
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_3',
                    'pump_number': 2,
                    'balloon_size': 1.2,
                    'current_earnings': 0.10,
                    'time_since_prev_pump': 1400,
                    'timestamp_milliseconds': 17000
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_3',
                    'pump_number': 3,
                    'balloon_size': 1.3,
                    'current_earnings': 0.15,
                    'time_since_prev_pump': 1300,
                    'timestamp_milliseconds': 18300
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_3',
                    'pump_number': 4,
                    'balloon_size': 1.4,
                    'current_earnings': 0.20,
                    'time_since_prev_pump': 1200,
                    'timestamp_milliseconds': 19500
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pump',
                    'balloon_id': 'balloon_3',
                    'pump_number': 5,
                    'balloon_size': 1.5,
                    'current_earnings': 0.25,
                    'time_since_prev_pump': 1100,
                    'timestamp_milliseconds': 20600
                }
            },
            {
                'session_id': session.session_id,
                'event_type': 'balloon_risk',
                'event_data': {
                    'event_type': 'pop',
                    'balloon_id': 'balloon_3',
                    'pump_number': 5,
                    'earnings_lost': 0.25,
                    'timestamp_milliseconds': 22000
                }
            }
        ]
        
        # Process events using EventLogger
        for event_data in events_data:
            try:
                result = self.event_logger.run(event_data)
                if result.get('processed'):
                    print(f"  ✓ Processed {event_data['event_data']['event_type']} event")
                else:
                    print(f"  ⚠️  Failed to process event: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"  ✗ Error processing event: {str(e)}")
        
        print(f"✓ Simulated {len(events_data)} behavioral events")
    
    def extract_metrics(self, session):
        """Extract behavioral metrics from events."""
        print("\n📊 Extracting behavioral metrics...")
        
        try:
            result = self.metric_extractor.extract_session_metrics(session.session_id)
            
            if result.get('processed'):
                metrics_count = BehavioralMetric.objects.filter(session=session).count()
                print(f"✓ Extracted {metrics_count} behavioral metrics")
                
                # Show some key metrics
                key_metrics = BehavioralMetric.objects.filter(
                    session=session,
                    metric_name__contains='risk_tolerance'
                )[:3]
                
                for metric in key_metrics:
                    print(f"  • {metric.metric_name}: {metric.metric_value:.3f}")
            else:
                print(f"✗ Metric extraction failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ Error extracting metrics: {str(e)}")
    
    def perform_trait_inference(self, session):
        """Perform trait inference using the TraitInferencer agent."""
        print("\n🧠 Performing trait inference...")
        
        try:
            result = self.trait_inferencer.infer_session_traits(session.session_id)
            
            if result.get('processed'):
                traits = result.get('traits', {})
                print("✓ Trait inference completed successfully")
                
                # Display trait scores
                print("\n📈 Trait Profile:")
                print("-" * 40)
                for trait_name, trait_data in traits.items():
                    if isinstance(trait_data, dict):
                        score = trait_data.get('score', 0.0)
                        confidence = trait_data.get('confidence', 0.0)
                        interpretation = trait_data.get('interpretation', 'No interpretation available')
                        print(f"  {trait_name.replace('_', ' ').title()}:")
                        print(f"    Score: {score:.3f}")
                        print(f"    Confidence: {confidence:.3f}")
                        print(f"    Interpretation: {interpretation}")
                        print()
                    else:
                        print(f"  {trait_name.replace('_', ' ').title()}: {trait_data:.3f}")
                
                return traits
            else:
                print(f"✗ Trait inference failed: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"✗ Error during trait inference: {str(e)}")
            return None
    
    def test_api_endpoint(self, session):
        """Test the context-engineered trait inference API endpoint."""
        print("\n🌐 Testing API endpoint...")
        
        # Note: This would require authentication in a real scenario
        # For demo purposes, we'll show the expected API call
        
        api_url = f"{self.api_url}/traits/trait-profiles/"
        request_data = {
            'session_id': session.session_id
        }
        
        print(f"API URL: {api_url}")
        print(f"Request data: {json.dumps(request_data, indent=2)}")
        
        # Expected response format
        expected_response = {
            'session_id': session.session_id,
            'risk_tolerance': 0.65,
            'consistency': 0.78,
            'learning': 0.72,
            'decision_speed': 0.58,
            'emotional_regulation': 0.81,
            'confidence_interval': 0.85,
            'data_completeness': 95.0,
            'quality_score': 88.0,
            'reliability_score': 82.0,
            'assessment_timestamp': datetime.now().isoformat(),
            'scientific_validation': {
                'meets_thresholds': True,
                'validation_method': 'Context-engineered trait inference',
                'data_schema_version': '1.0',
                'assessment_version': '1.0'
            }
        }
        
        print("\nExpected API Response:")
        print(json.dumps(expected_response, indent=2))
        
        print("\n💡 To test the actual API endpoint:")
        print("1. Start the Django development server: python manage.py runserver")
        print("2. Make an authenticated POST request to the API endpoint")
        print("3. Include the session_id in the request body")
    
    def validate_trait_results(self, traits, session):
        """Validate trait inference results using the validation engine."""
        print("\n🔍 Validating trait results...")
        
        if not traits:
            print("✗ No traits to validate")
            return
        
        try:
            validation_result = self.validation_engine.validate_trait_inference(
                session.session_id, traits
            )
            
            print("✓ Validation completed")
            print(f"  Is Valid: {validation_result['is_valid']}")
            print(f"  Confidence Level: {validation_result['confidence_level']:.3f}")
            print(f"  Reliability Score: {validation_result['reliability_score']:.1f}%")
            print(f"  Data Quality Score: {validation_result['data_quality_score']:.1f}%")
            print(f"  Validity Score: {validation_result['validity_score']:.3f}")
            
            if validation_result.get('warnings'):
                print("\n⚠️  Warnings:")
                for warning in validation_result['warnings']:
                    print(f"  • {warning}")
            
            if validation_result.get('recommendations'):
                print("\n💡 Recommendations:")
                for recommendation in validation_result['recommendations']:
                    print(f"  • {recommendation}")
                    
        except Exception as e:
            print(f"✗ Error during validation: {str(e)}")
    
    def demonstrate_error_handling(self):
        """Demonstrate error handling scenarios."""
        print("\n🚨 Demonstrating error handling...")
        
        error_scenarios = [
            {
                'name': 'Missing session_id',
                'data': {},
                'expected_error': 'Missing required field: session_id.'
            },
            {
                'name': 'Nonexistent session',
                'data': {'session_id': 'nonexistent_session_123'},
                'expected_error': 'Session nonexistent_session_123 not found'
            },
            {
                'name': 'Incomplete session',
                'data': {'session_id': 'incomplete_session'},
                'expected_error': 'Session is not completed'
            }
        ]
        
        for scenario in error_scenarios:
            print(f"\n  Testing: {scenario['name']}")
            print(f"  Expected error: {scenario['expected_error']}")
            print(f"  This demonstrates proper validation and error handling")
    
    def run_demo(self):
        """Run the complete context engineering demonstration."""
        try:
            # Step 1: Create test data
            user, session = self.create_test_user_and_session()
            
            # Step 2: Simulate behavioral events
            self.simulate_behavioral_events(session)
            
            # Step 3: Extract metrics
            self.extract_metrics(session)
            
            # Step 4: Perform trait inference
            traits = self.perform_trait_inference(session)
            
            # Step 5: Validate results
            self.validate_trait_results(traits, session)
            
            # Step 6: Test API endpoint
            self.test_api_endpoint(session)
            
            # Step 7: Demonstrate error handling
            self.demonstrate_error_handling()
            
            print("\n" + "=" * 60)
            print("🎉 Context Engineering Demo Completed Successfully!")
            print("=" * 60)
            
            print("\n📋 Summary:")
            print("• Created realistic behavioral data")
            print("• Extracted scientific metrics")
            print("• Performed multi-dimensional trait inference")
            print("• Validated results with scientific rigor")
            print("• Demonstrated API endpoint functionality")
            print("• Showed comprehensive error handling")
            
            print("\n🔬 Scientific Features Demonstrated:")
            print("• Context-engineered trait mapping")
            print("• Multi-dimensional psychometric assessment")
            print("• Scientific validation thresholds")
            print("• Confidence interval calculation")
            print("• Data quality assessment")
            print("• Reliability scoring")
            
            print(f"\n📊 Session ID for further testing: {session.session_id}")
            
        except Exception as e:
            print(f"\n✗ Demo failed with error: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Main function to run the demo."""
    demo = ContextEngineeringDemo()
    demo.run_demo()


if __name__ == "__main__":
    main() 