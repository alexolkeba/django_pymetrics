from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TraitDimension, TraitDefinition, TraitMeasurement, TraitProfile
from .comprehensive_traits import ComprehensiveTraitSystem

User = get_user_model()


class TraitMappingModelsTest(TestCase):
    """Test cases for trait mapping models."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.dimension = TraitDimension.objects.create(
            name='emotion',
            description='Emotional traits and responses',
            scientific_basis='Based on emotional intelligence research'
        )
        
        self.trait_definition = TraitDefinition.objects.create(
            dimension=self.dimension,
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
    
    def test_trait_dimension_creation(self):
        """Test trait dimension creation."""
        self.assertEqual(self.dimension.name, 'emotion')
        self.assertEqual(self.dimension.get_name_display(), 'Emotion')
        self.assertIn('emotional intelligence', self.dimension.scientific_basis.lower())
    
    def test_trait_definition_creation(self):
        """Test trait definition creation."""
        self.assertEqual(self.trait_definition.name, 'emotional_recognition')
        self.assertEqual(self.trait_definition.dimension, self.dimension)
        self.assertEqual(self.trait_definition.reliability_coefficient, 0.78)
        self.assertTrue(self.trait_definition.is_active)
    
    def test_trait_measurement_creation(self):
        """Test trait measurement creation."""
        measurement = TraitMeasurement.objects.create(
            user=self.user,
            trait_definition=self.trait_definition,
            session_id='test_session_123',
            game_type='faces_game',
            raw_score=0.85,
            normalized_score=0.82,
            confidence_interval={'lower': 0.75, 'upper': 0.89},
            reliability_coefficient=0.78,
            measurement_method='facial_expression_identification',
            data_points_used=150
        )
        
        self.assertEqual(measurement.user, self.user)
        self.assertEqual(measurement.normalized_score, 0.82)
        self.assertEqual(measurement.data_points_used, 150)
    
    def test_trait_profile_creation(self):
        """Test trait profile creation."""
        profile = TraitProfile.objects.create(
            user=self.user,
            session_id='test_session_123',
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
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.overall_confidence, 0.78)
        self.assertEqual(profile.traits_measured, 1)
        self.assertEqual(profile.total_data_points, 150)


class ComprehensiveTraitSystemTest(TestCase):
    """Test cases for comprehensive trait system."""
    
    def setUp(self):
        """Set up test data."""
        self.trait_system = ComprehensiveTraitSystem()
    
    def test_trait_system_initialization(self):
        """Test trait system initialization."""
        self.assertIsNotNone(self.trait_system.trait_definitions)
        self.assertIsNotNone(self.trait_system.dimension_mappings)
        self.assertGreater(len(self.trait_system.get_all_traits()), 80)  # Should have 90+ traits
    
    def test_get_all_traits(self):
        """Test getting all traits."""
        traits = self.trait_system.get_all_traits()
        self.assertIsInstance(traits, list)
        self.assertGreater(len(traits), 80)  # Should have 90+ traits
        
        # Check for specific traits
        expected_traits = ['emotional_recognition', 'sustained_attention', 'effort_allocation']
        for trait in expected_traits:
            self.assertIn(trait, traits)
    
    def test_get_traits_by_dimension(self):
        """Test getting traits by dimension."""
        from .comprehensive_traits import TraitDimension
        
        emotion_traits = self.trait_system.get_traits_by_dimension(TraitDimension.EMOTION)
        self.assertIsInstance(emotion_traits, list)
        self.assertEqual(len(emotion_traits), 10)  # Should have 10 emotion traits
        
        attention_traits = self.trait_system.get_traits_by_dimension(TraitDimension.ATTENTION)
        self.assertIsInstance(attention_traits, list)
        self.assertEqual(len(attention_traits), 10)  # Should have 10 attention traits
    
    def test_get_trait_definition(self):
        """Test getting trait definition."""
        trait_def = self.trait_system.get_trait_definition('emotional_recognition')
        self.assertIsNotNone(trait_def)
        self.assertEqual(trait_def.name, 'Emotional Recognition')
        self.assertEqual(trait_def.dimension.value, 'emotion')
        self.assertEqual(trait_def.reliability_coefficient, 0.78)
    
    def test_calculate_trait_score(self):
        """Test calculating trait score."""
        behavioral_data = {
            'facial_expression_accuracy': 0.85,
            'emotion_identification_speed': 1200
        }
        
        result = self.trait_system.calculate_trait_score('emotional_recognition', behavioral_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn('trait_name', result)
        self.assertIn('normalized_score', result)
        self.assertIn('confidence', result)
        self.assertEqual(result['trait_name'], 'emotional_recognition')
        self.assertGreater(result['confidence'], 0.0)
    
    def test_calculate_all_traits(self):
        """Test calculating all traits."""
        behavioral_data = {
            'facial_expression_accuracy': 0.85,
            'emotion_identification_speed': 1200,
            'reaction_time': 500,
            'accuracy': 0.92
        }
        
        results = self.trait_system.calculate_all_traits(behavioral_data)
        
        self.assertIsInstance(results, dict)
        self.assertIn('summary', results)
        self.assertGreater(len(results), 80)  # Should have 90+ trait results
        
        summary = results['summary']
        self.assertIn('total_traits', summary)
        self.assertIn('valid_traits', summary)
        self.assertIn('average_confidence', summary) 