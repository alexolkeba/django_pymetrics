"""
Trait Mapping Models for Django Pymetrics

This module defines models for storing trait measurements and mapping configurations
for the comprehensive 90+ trait system across 9 bi-directional dimensions.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class TraitDimension(models.Model):
    """Model for storing trait dimensions."""
    
    DIMENSION_CHOICES = [
        ('emotion', 'Emotion'),
        ('attention', 'Attention'),
        ('effort', 'Effort'),
        ('fairness', 'Fairness'),
        ('focus', 'Focus'),
        ('decision_making', 'Decision Making'),
        ('learning', 'Learning'),
        ('generosity', 'Generosity'),
        ('risk_tolerance', 'Risk Tolerance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=DIMENSION_CHOICES, unique=True)
    description = models.TextField(help_text="Description of the trait dimension")
    scientific_basis = models.TextField(help_text="Scientific basis for this dimension")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trait_dimensions'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()} Dimension"


class TraitDefinition(models.Model):
    """Model for storing trait definitions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dimension = models.ForeignKey(TraitDimension, on_delete=models.CASCADE, related_name='traits')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(help_text="Description of the trait")
    scientific_basis = models.TextField(help_text="Scientific basis for this trait")
    measurement_method = models.CharField(max_length=200, help_text="Method used to measure this trait")
    reliability_coefficient = models.FloatField(help_text="Reliability coefficient for this trait")
    validity_evidence = models.TextField(help_text="Evidence of validity for this trait")
    source_games = models.JSONField(default=list, help_text="Games that measure this trait")
    metrics_used = models.JSONField(default=list, help_text="Metrics used to calculate this trait")
    normalization_method = models.CharField(max_length=50, help_text="Normalization method used")
    confidence_threshold = models.FloatField(help_text="Confidence threshold for this trait")
    is_active = models.BooleanField(default=True, help_text="Whether this trait is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trait_definitions'
        ordering = ['dimension', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.dimension.get_name_display()})"


class TraitMeasurement(models.Model):
    """Model for storing individual trait measurements."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trait_measurements')
    trait_definition = models.ForeignKey(TraitDefinition, on_delete=models.CASCADE, related_name='measurements')
    session_id = models.CharField(max_length=64, help_text="Session ID for this measurement")
    game_type = models.CharField(max_length=50, help_text="Game type that generated this measurement")
    
    # Measurement values
    raw_score = models.FloatField(help_text="Raw score before normalization")
    normalized_score = models.FloatField(help_text="Normalized score (0-1 scale)")
    confidence_interval = models.JSONField(default=dict, help_text="Confidence interval bounds")
    
    # Scientific validation
    reliability_coefficient = models.FloatField(help_text="Reliability coefficient for this measurement")
    validity_evidence = models.TextField(blank=True, help_text="Evidence of validity")
    
    # Metadata
    measurement_method = models.CharField(max_length=100, help_text="Method used for measurement")
    data_points_used = models.IntegerField(default=0, help_text="Number of data points used")
    calculation_timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'trait_measurements'
        ordering = ['-calculation_timestamp']
        indexes = [
            models.Index(fields=['user', 'trait_definition']),
            models.Index(fields=['session_id', 'game_type']),
            models.Index(fields=['calculation_timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.trait_definition.name} - {self.normalized_score}"


class TraitProfile(models.Model):
    """Model for storing complete trait profiles for users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trait_profiles')
    session_id = models.CharField(max_length=64, unique=True, help_text="Session ID for this profile")
    
    # Profile data
    trait_scores = models.JSONField(default=dict, help_text="All trait scores for this profile")
    dimension_scores = models.JSONField(default=dict, help_text="Dimension-level scores")
    confidence_scores = models.JSONField(default=dict, help_text="Confidence scores for each trait")
    
    # Quality metrics
    overall_confidence = models.FloatField(help_text="Overall confidence in the profile")
    data_completeness = models.FloatField(help_text="Percentage of data completeness")
    quality_score = models.FloatField(help_text="Overall quality score")
    
    # Metadata
    calculation_method = models.CharField(max_length=100, help_text="Method used for calculation")
    traits_measured = models.IntegerField(default=0, help_text="Number of traits measured")
    total_data_points = models.IntegerField(default=0, help_text="Total data points used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trait_mapping_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'session_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.session_id} - {self.overall_confidence}"


class TraitMappingConfiguration(models.Model):
    """Model for storing trait mapping configurations."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="Configuration name")
    description = models.TextField(help_text="Description of this configuration")
    
    # Configuration data
    trait_weights = models.JSONField(default=dict, help_text="Weights for different traits")
    normalization_settings = models.JSONField(default=dict, help_text="Normalization settings")
    confidence_thresholds = models.JSONField(default=dict, help_text="Confidence thresholds")
    
    # Versioning
    version = models.CharField(max_length=20, default='1.0', help_text="Configuration version")
    is_active = models.BooleanField(default=True, help_text="Whether this configuration is active")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trait_mapping_configurations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} v{self.version}" 