"""
Enhanced Trait Profile Models for Django Pymetrics

This module defines models for psychometric trait profiles and success model comparison.
All models are designed for scientific reproducibility and multi-dimensional trait analysis.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from games.models import GameSession
import uuid

User = get_user_model()


class TraitProfile(models.Model):
    """
    Enhanced trait profile model for multi-dimensional psychometric assessment.
    
    This model captures comprehensive trait profiles derived from behavioral data
    and enables comparison with success models for talent assessment.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(GameSession, on_delete=models.CASCADE, related_name='trait_profile')
    
    # Core cognitive traits
    risk_tolerance = models.FloatField(null=True, blank=True, 
                                      validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      help_text="Risk tolerance score (0-100)")
    working_memory = models.FloatField(null=True, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      help_text="Working memory capacity (0-100)")
    attention_control = models.FloatField(null=True, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         help_text="Attention control ability (0-100)")
    decision_speed = models.FloatField(null=True, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      help_text="Decision-making speed (0-100)")
    learning_agility = models.FloatField(null=True, blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(100)],
                                        help_text="Learning and adaptation ability (0-100)")
    
    # Socio-emotional traits
    emotional_regulation = models.FloatField(null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)],
                                            help_text="Emotional regulation ability (0-100)")
    social_perception = models.FloatField(null=True, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         help_text="Social perception and empathy (0-100)")
    trust_tendency = models.FloatField(null=True, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      help_text="Tendency to trust others (0-100)")
    fairness_perception = models.FloatField(null=True, blank=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)],
                                           help_text="Fairness perception and judgment (0-100)")
    
    # Behavioral traits
    persistence = models.FloatField(null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text="Persistence and grit (0-100)")
    adaptability = models.FloatField(null=True, blank=True,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    help_text="Adaptability to change (0-100)")
    consistency = models.FloatField(null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text="Behavioral consistency (0-100)")
    impulsivity = models.FloatField(null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text="Impulsivity level (0-100)")
    
    # Success model comparison fields
    success_model_match = models.FloatField(null=True, blank=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)],
                                           help_text="Match score with success model (0-100)")
    recommendation_band = models.CharField(max_length=32, blank=True,
                                         choices=[
                                             ('highly_recommend', 'Highly Recommend'),
                                             ('recommend', 'Recommend'),
                                             ('do_not_recommend', 'Do Not Recommend'),
                                             ('borderline', 'Borderline'),
                                         ],
                                         help_text="Recommendation based on success model comparison")
    confidence_level = models.FloatField(null=True, blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(100)],
                                        help_text="Confidence in trait assessment (0-100)")
    
    # Versioning and reproducibility
    assessment_version = models.CharField(max_length=32, default='1.0',
                                        help_text="Version of assessment algorithm used")
    data_schema_version = models.CharField(max_length=32, default='1.0',
                                          help_text="Version of data schema used")
    calculation_timestamp = models.DateTimeField(default=timezone.now,
                                               help_text="When trait profile was calculated")
    
    # Metadata and audit trail
    assessment_notes = models.TextField(blank=True,
                                       help_text="Notes about the assessment process")
    validation_status = models.CharField(max_length=32, default='pending',
                                       choices=[
                                           ('pending', 'Pending'),
                                           ('validated', 'Validated'),
                                           ('flagged', 'Flagged for Review'),
                                           ('invalid', 'Invalid'),
                                       ],
                                       help_text="Validation status of trait profile")
    
    class Meta:
        db_table = 'trait_profiles'
        ordering = ['-calculation_timestamp']
        indexes = [
            models.Index(fields=['session', 'recommendation_band']),
            models.Index(fields=['success_model_match', 'confidence_level']),
            models.Index(fields=['validation_status']),
        ]
    
    def __str__(self):
        return f"{self.session.user.username} - {self.recommendation_band} - {self.calculation_timestamp}"
    
    def get_trait_summary(self):
        """Get a summary of all trait scores."""
        traits = {
            'cognitive': {
                'risk_tolerance': self.risk_tolerance,
                'working_memory': self.working_memory,
                'attention_control': self.attention_control,
                'decision_speed': self.decision_speed,
                'learning_agility': self.learning_agility,
            },
            'socio_emotional': {
                'emotional_regulation': self.emotional_regulation,
                'social_perception': self.social_perception,
                'trust_tendency': self.trust_tendency,
                'fairness_perception': self.fairness_perception,
            },
            'behavioral': {
                'persistence': self.persistence,
                'adaptability': self.adaptability,
                'consistency': self.consistency,
                'impulsivity': self.impulsivity,
            }
        }
        return traits
    
    def get_average_trait_score(self, trait_category=None):
        """Calculate average trait score for a category or overall."""
        traits = self.get_trait_summary()
        
        if trait_category and trait_category in traits:
            category_traits = traits[trait_category]
        else:
            # Combine all categories
            category_traits = {}
            for category in traits.values():
                category_traits.update(category)
        
        valid_scores = [score for score in category_traits.values() if score is not None]
        return sum(valid_scores) / len(valid_scores) if valid_scores else None


class SuccessModel(models.Model):
    """
    Success model for role-specific trait profiles.
    
    This model defines the ideal trait profile for success in specific roles,
    enabling comparison with candidate trait profiles.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True, help_text="Name of the success model")
    role_title = models.CharField(max_length=128, help_text="Job role title")
    organization = models.CharField(max_length=128, help_text="Organization name")
    
    # Trait requirements (same structure as TraitProfile)
    risk_tolerance_target = models.FloatField(null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    working_memory_target = models.FloatField(null=True, blank=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    attention_control_target = models.FloatField(null=True, blank=True,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    decision_speed_target = models.FloatField(null=True, blank=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    learning_agility_target = models.FloatField(null=True, blank=True,
                                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    emotional_regulation_target = models.FloatField(null=True, blank=True,
                                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    social_perception_target = models.FloatField(null=True, blank=True,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    trust_tendency_target = models.FloatField(null=True, blank=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    fairness_perception_target = models.FloatField(null=True, blank=True,
                                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    persistence_target = models.FloatField(null=True, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    adaptability_target = models.FloatField(null=True, blank=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    consistency_target = models.FloatField(null=True, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    impulsivity_target = models.FloatField(null=True, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Matching criteria
    trait_weights = models.JSONField(default=dict, help_text="Weights for different traits in matching")
    match_thresholds = models.JSONField(default=dict, help_text="Thresholds for recommendation bands")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_success_models')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text="Whether this model is currently active")
    version = models.CharField(max_length=32, default='1.0', help_text="Model version")
    
    class Meta:
        db_table = 'success_models'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role_title', 'organization']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.role_title} at {self.organization}"
    
    def get_target_traits(self):
        """Get target trait values as dictionary."""
        return {
            'risk_tolerance': self.risk_tolerance_target,
            'working_memory': self.working_memory_target,
            'attention_control': self.attention_control_target,
            'decision_speed': self.decision_speed_target,
            'learning_agility': self.learning_agility_target,
            'emotional_regulation': self.emotional_regulation_target,
            'social_perception': self.social_perception_target,
            'trust_tendency': self.trust_tendency_target,
            'fairness_perception': self.fairness_perception_target,
            'persistence': self.persistence_target,
            'adaptability': self.adaptability_target,
            'consistency': self.consistency_target,
            'impulsivity': self.impulsivity_target,
        }


class TraitAssessment(models.Model):
    """
    Individual trait assessment for specific games or components.
    
    This model captures detailed trait assessments for individual games
    or assessment components, providing granular insights.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trait_profile = models.ForeignKey(TraitProfile, on_delete=models.CASCADE, related_name='assessments')
    game_type = models.CharField(max_length=64, help_text="Type of game assessed")
    component_name = models.CharField(max_length=128, help_text="Specific component or metric assessed")
    
    # Assessment results
    trait_value = models.FloatField(help_text="Calculated trait value")
    confidence_interval = models.JSONField(default=dict, help_text="Confidence interval bounds")
    sample_size = models.IntegerField(help_text="Number of data points used")
    
    # Metadata
    assessment_method = models.CharField(max_length=128, help_text="Method used for assessment")
    assessment_timestamp = models.DateTimeField(default=timezone.now)
    data_version = models.CharField(max_length=32, default='1.0', help_text="Data schema version")
    
    class Meta:
        db_table = 'trait_assessments'
        ordering = ['-assessment_timestamp']
        indexes = [
            models.Index(fields=['trait_profile', 'game_type']),
            models.Index(fields=['component_name']),
        ]
        unique_together = ['trait_profile', 'game_type', 'component_name']
    
    def __str__(self):
        return f"{self.trait_profile.session.user.username} - {self.game_type} - {self.component_name}"


class AssessmentValidation(models.Model):
    """
    Validation records for trait assessments.
    
    This model tracks validation status and quality metrics for trait assessments,
    ensuring scientific reproducibility and data quality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trait_profile = models.OneToOneField(TraitProfile, on_delete=models.CASCADE, related_name='validation')
    
    # Validation metrics
    data_completeness = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         help_text="Percentage of required data collected")
    data_quality_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                          help_text="Overall data quality score")
    assessment_reliability = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                              help_text="Reliability score of assessment")
    
    # Validation flags
    has_sufficient_data = models.BooleanField(default=False, help_text="Whether sufficient data was collected")
    meets_quality_threshold = models.BooleanField(default=False, help_text="Whether quality threshold was met")
    is_scientifically_valid = models.BooleanField(default=False, help_text="Whether assessment is scientifically valid")
    
    # Validation details
    validation_notes = models.TextField(blank=True, help_text="Notes about validation process")
    quality_issues = models.JSONField(default=list, help_text="List of quality issues found")
    
    # Metadata
    validated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='validated_assessments')
    validation_timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'assessment_validations'
        ordering = ['-validation_timestamp']
        indexes = [
            models.Index(fields=['has_sufficient_data', 'meets_quality_threshold']),
            models.Index(fields=['is_scientifically_valid']),
        ]
    
    def __str__(self):
        return f"{self.trait_profile.session.user.username} - Validation {self.validation_timestamp}"
