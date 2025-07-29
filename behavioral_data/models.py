"""
Behavioral Data Models for Django Pymetrics

This module defines models for capturing granular behavioral data from neuroscience-based games.
All models are designed for scientific reproducibility, privacy compliance, and scalability.

UPDATED: Enhanced for comprehensive Pymetrics upgrade with 1000+ data points per session.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import json
import uuid

User = get_user_model()


class BehavioralSession(models.Model):
    """
    Represents a complete behavioral assessment session.
    
    This model captures session-level metadata and provides the foundation
    for all granular behavioral data collection.
    """
    SESSION_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    GAME_TYPES = [
        ('balloon_risk', 'Balloon Risk Game'),
        ('memory_cards', 'Memory Cards Game'),
        ('reaction_timer', 'Reaction Timer Game'),
        ('mixed', 'Multiple Games'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behavioral_sessions')
    session_id = models.CharField(max_length=64, unique=True)
    game_type = models.CharField(max_length=32, choices=GAME_TYPES, default='mixed',
                               help_text="Type of game(s) in this session")
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='pending')
    device_info = models.JSONField(default=dict, help_text="Device and browser information")
    session_start_time = models.DateTimeField(default=timezone.now, db_index=True)
    session_end_time = models.DateTimeField(null=True, blank=True, db_index=True)
    started_at = models.DateTimeField(null=True, blank=True,
                                    help_text="When the session was actually started by the user")
    is_completed = models.BooleanField(default=False)
    total_games_played = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0, help_text="Total session duration in milliseconds")
    duration_ms = models.IntegerField(null=True, blank=True, 
                                    help_text="Duration of the session in milliseconds")
    
    # Privacy and compliance fields
    data_anonymized = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    data_retention_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'behavioral_sessions'
        ordering = ['-session_start_time']
        indexes = [
            models.Index(fields=['user', 'session_start_time']),
            models.Index(fields=['session_id']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['status']),
            models.Index(fields=['game_type']),
            models.Index(fields=['started_at']),
            models.Index(fields=['session_start_time', 'session_end_time']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.session_id} - {self.session_start_time}"
    
    def complete_session(self):
        """Mark session as completed and set end time."""
        self.session_end_time = timezone.now()
        self.is_completed = True
        self.save()


class BehavioralEvent(models.Model):
    """
    Base model for all granular behavioral events.
    
    This model captures the fundamental structure of behavioral events
    with proper timestamping, event categorization, and data validation.
    """
    EVENT_TYPES = [
        ('session_start', 'Session Start'),
        ('session_end', 'Session End'),
        ('game_start', 'Game Start'),
        ('game_end', 'Game End'),
        ('user_action', 'User Action'),
        ('system_event', 'System Event'),
        ('error_event', 'Error Event'),
        ('focus_event', 'Focus/Blur Event'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(BehavioralSession, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=128, help_text="Specific event name (e.g., 'pump', 'cash_out')")
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    timestamp_milliseconds = models.IntegerField(help_text="Millisecond precision timestamp")
    
    # Event data stored as JSON for flexibility
    event_data = models.JSONField(default=dict, help_text="Event-specific data")
    metadata = models.JSONField(default=dict, help_text="Additional metadata")
    
    # Performance and validation fields
    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in milliseconds")
    validation_status = models.CharField(max_length=32, default='pending', 
                                       choices=[('pending', 'Pending'), ('valid', 'Valid'), ('invalid', 'Invalid')])
    
    class Meta:
        db_table = 'behavioral_events'
        ordering = ['timestamp', 'timestamp_milliseconds']
        indexes = [
            models.Index(fields=['session', 'event_type', 'timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['validation_status']),
        ]
    
    def __str__(self):
        return f"{self.session.session_id} - {self.event_type} - {self.event_name} - {self.timestamp}"


class BalloonRiskEvent(models.Model):
    """
    Specific event model for Balloon Risk Game behavioral data.
    
    Captures all granular interactions in the balloon risk game including
    pumps, cash outs, pops, and session-level metrics.
    """
    EVENT_TYPES = [
        ('balloon_start', 'Balloon Start'),
        ('balloon_end', 'Balloon End'),
        ('pump', 'Pump'),
        ('cash_out', 'Cash Out'),
        ('pop', 'Pop'),
        ('focus', 'Focus/Blur'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(BehavioralSession, on_delete=models.CASCADE, related_name='balloon_events')
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    balloon_id = models.CharField(max_length=64, null=True, blank=True)
    balloon_index = models.IntegerField(null=True, blank=True)
    balloon_color = models.CharField(max_length=32, null=True, blank=True)
    
    # Timing data with millisecond precision
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    timestamp_milliseconds = models.IntegerField(help_text="Millisecond precision timestamp")
    
    # Pump-specific data
    pump_number = models.IntegerField(null=True, blank=True, help_text="Nth pump for this balloon")
    time_since_prev_pump = models.FloatField(null=True, blank=True, help_text="Time since previous pump in milliseconds")
    balloon_size = models.FloatField(null=True, blank=True, help_text="Balloon size at pump")
    
    # Financial data
    current_earnings = models.FloatField(null=True, blank=True, help_text="Earnings for current balloon")
    total_earnings = models.FloatField(null=True, blank=True, help_text="Total session earnings")
    
    # Outcome data
    outcome = models.CharField(max_length=16, null=True, blank=True, 
                              choices=[('popped', 'Popped'), ('cashed', 'Cashed Out'), ('ongoing', 'Ongoing')])
    earnings_lost = models.FloatField(null=True, blank=True, help_text="Earnings lost if popped")
    
    # Behavioral patterns
    is_new_personal_max = models.BooleanField(null=True, blank=True, help_text="Pumped to new personal max")
    is_rapid_pump = models.BooleanField(null=True, blank=True, help_text="Rapid pump based on interval")
    hesitation_time = models.FloatField(null=True, blank=True, help_text="Hesitation time before action")
    
    # Additional context
    device_info = models.JSONField(default=dict, help_text="Device context at event")
    user_context = models.JSONField(default=dict, help_text="User context and state")
    
    class Meta:
        db_table = 'balloon_risk_events'
        ordering = ['timestamp', 'timestamp_milliseconds']
        indexes = [
            models.Index(fields=['session', 'balloon_id', 'event_type']),
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['balloon_index', 'pump_number']),
        ]
    
    def __str__(self):
        return f"{self.session.session_id} - Balloon {self.balloon_index} - {self.event_type} - {self.timestamp}"


class MemoryCardsEvent(models.Model):
    """
    Specific event model for Memory Cards Game behavioral data.
    
    Captures card flips, matches, mismatches, and memory-related metrics.
    """
    EVENT_TYPES = [
        ('card_flip', 'Card Flip'),
        ('card_match', 'Card Match'),
        ('card_mismatch', 'Card Mismatch'),
        ('round_start', 'Round Start'),
        ('round_end', 'Round End'),
        ('game_start', 'Game Start'),
        ('game_end', 'Game End'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(BehavioralSession, on_delete=models.CASCADE, related_name='memory_events')
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    
    # Card-specific data
    card_id = models.CharField(max_length=64, null=True, blank=True)
    card_position = models.IntegerField(null=True, blank=True)
    card_value = models.CharField(max_length=32, null=True, blank=True)
    
    # Timing data
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    timestamp_milliseconds = models.IntegerField(help_text="Millisecond precision timestamp")
    reaction_time = models.FloatField(null=True, blank=True, help_text="Reaction time in milliseconds")
    
    # Game state data
    round_number = models.IntegerField(null=True, blank=True)
    cards_flipped = models.IntegerField(default=0, help_text="Number of cards flipped in current round")
    matches_found = models.IntegerField(default=0, help_text="Total matches found")
    
    # Memory and performance data
    is_correct_match = models.BooleanField(null=True, blank=True)
    memory_accuracy = models.FloatField(null=True, blank=True, help_text="Memory accuracy percentage")
    
    class Meta:
        db_table = 'memory_cards_events'
        ordering = ['timestamp', 'timestamp_milliseconds']
        indexes = [
            models.Index(fields=['session', 'event_type', 'timestamp']),
            models.Index(fields=['card_id', 'round_number']),
        ]
    
    def __str__(self):
        return f"{self.session.session_id} - {self.event_type} - Card {self.card_id} - {self.timestamp}"


class ReactionTimerEvent(models.Model):
    """
    Specific event model for Reaction Timer Game behavioral data.
    
    Captures stimulus presentation, response times, and accuracy metrics.
    """
    EVENT_TYPES = [
        ('stimulus_present', 'Stimulus Present'),
        ('user_response', 'User Response'),
        ('trial_start', 'Trial Start'),
        ('trial_end', 'Trial End'),
        ('block_start', 'Block Start'),
        ('block_end', 'Block End'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(BehavioralSession, on_delete=models.CASCADE, related_name='reaction_events')
    event_type = models.CharField(max_length=32, choices=EVENT_TYPES)
    
    # Trial-specific data
    trial_number = models.IntegerField(null=True, blank=True)
    block_number = models.IntegerField(null=True, blank=True)
    stimulus_type = models.CharField(max_length=32, null=True, blank=True)
    
    # Timing data
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    timestamp_milliseconds = models.IntegerField(help_text="Millisecond precision timestamp")
    stimulus_time = models.FloatField(null=True, blank=True, help_text="Stimulus presentation time")
    response_time = models.FloatField(null=True, blank=True, help_text="Response time in milliseconds")
    
    # Performance data
    is_correct = models.BooleanField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True, help_text="Response accuracy")
    
    # Additional context
    stimulus_data = models.JSONField(default=dict, help_text="Stimulus-specific data")
    response_data = models.JSONField(default=dict, help_text="Response-specific data")
    
    class Meta:
        db_table = 'reaction_timer_events'
        ordering = ['timestamp', 'timestamp_milliseconds']
        indexes = [
            models.Index(fields=['session', 'event_type', 'timestamp']),
            models.Index(fields=['trial_number', 'block_number']),
        ]
    
    def __str__(self):
        return f"{self.session.session_id} - Trial {self.trial_number} - {self.event_type} - {self.timestamp}"


class BehavioralMetric(models.Model):
    """
    Aggregated behavioral metrics derived from raw events.
    
    This model stores calculated metrics for scientific analysis and trait inference.
    """
    METRIC_TYPES = [
        ('session_level', 'Session Level'),
        ('game_level', 'Game Level'),
        ('trial_level', 'Trial Level'),
        ('user_level', 'User Level'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(BehavioralSession, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.CharField(max_length=32, choices=METRIC_TYPES)
    metric_name = models.CharField(max_length=128, help_text="Metric name (e.g., 'avg_pumps_per_balloon')")
    game_type = models.CharField(max_length=64, null=True, blank=True)
    
    # Metric values
    metric_value = models.FloatField(help_text="Calculated metric value")
    metric_unit = models.CharField(max_length=32, null=True, blank=True, help_text="Unit of measurement")
    
    # Statistical context
    sample_size = models.IntegerField(null=True, blank=True, help_text="Number of samples used")
    standard_error = models.FloatField(null=True, blank=True, help_text="Standard error of the metric")
    confidence_interval = models.JSONField(null=True, blank=True, help_text="Confidence interval bounds")
    
    # Calculation metadata
    calculation_method = models.CharField(max_length=128, help_text="Method used for calculation")
    calculation_timestamp = models.DateTimeField(default=timezone.now)
    data_version = models.CharField(max_length=32, default='1.0', help_text="Data schema version")
    
    class Meta:
        db_table = 'behavioral_metrics'
        ordering = ['-calculation_timestamp']
        indexes = [
            models.Index(fields=['session', 'metric_type', 'metric_name']),
            models.Index(fields=['game_type', 'metric_name']),
        ]
        unique_together = ['session', 'metric_name', 'game_type']
    
    def __str__(self):
        return f"{self.session.session_id} - {self.metric_name} - {self.metric_value}" 