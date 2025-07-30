from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    # Enhanced session tracking
    total_games_played = models.IntegerField(default=0)
    session_duration_ms = models.IntegerField(default=0, help_text="Total session duration in milliseconds")
    completion_rate = models.FloatField(default=0.0, help_text="Percentage of games completed")
    
    # Dynamic difficulty tracking
    difficulty_level = models.CharField(max_length=20, default='medium', 
                                      choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    adaptive_difficulty_enabled = models.BooleanField(default=True)
    
    # Performance metrics
    overall_performance_score = models.FloatField(default=0.0)
    engagement_score = models.FloatField(default=0.0)
    data_quality_score = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.user.username} - {self.started_at}"

class GameResult(models.Model):
    # Expanded game types to match Pymetrics 16-game suite
    GAME_TYPES = [
        # Core Neuroscience Games (12 games)
        ('balloon_risk', 'The Inflation Gambit', 'A high-stakes game of risk and reward. Pump a balloon to increase your potential earnings, but cash out before it bursts or lose everything. How far are you willing to go?'),
        ('memory_cards', 'Cognitive Atlas Challenge'),
        ('reaction_timer', 'Reaction Timer Game'),
        ('sorting_task', 'Sorting Task Game'),
        ('pattern_completion', 'Pattern Completion Game'),
        ('stroop_test', 'Stroop Test Game'),
        ('tower_of_hanoi', 'Tower of Hanoi Game'),
        ('emotional_faces', 'Emotional Faces Game'),
        ('trust_game', 'Trust Game'),
        ('stop_signal', 'Stop Signal Game'),
        ('digit_span', 'Digit Span Game'),
        ('fairness_game', 'Fairness Game'),
        
        # Additional Core Games (8 games)
        ('money_exchange_1', 'Money Exchange Game #1'),
        ('money_exchange_2', 'Money Exchange Game #2'),
        ('easy_or_hard', 'Easy or Hard Game'),
        ('cards_game', 'Cards Game (Iowa Gambling)'),
        ('arrows_game', 'Arrows Game'),
        ('lengths_game', 'Lengths Game'),
        ('keypresses', 'Keypresses Game'),
        ('faces_game', 'Faces Game'),
        
        # Numerical & Logical Reasoning Games (4 games)
        ('letters', 'Letters Game (N-back)'),
        ('magnitudes', 'Magnitudes Game'),
        ('sequences', 'Sequences Game'),
        ('shapes', 'Shapes Game'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, null=True, blank=True)
    game_type = models.CharField(max_length=50, choices=GAME_TYPES)
    
    # Enhanced scoring system
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    duration = models.IntegerField(help_text="Duration in milliseconds")
    
    # Dynamic difficulty tracking
    difficulty_level = models.CharField(max_length=20, default='medium',
                                      choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    difficulty_adjustments = models.JSONField(default=list, help_text="History of difficulty adjustments")
    
    # Enhanced behavioral data collection
    decisions = models.JSONField(default=list, blank=True)
    reaction_times = models.JSONField(default=list, blank=True)
    accuracy_data = models.JSONField(default=dict, blank=True)
    learning_curves = models.JSONField(default=dict, blank=True)
    
    # Expanded raw data collection (1000+ data points target)
    raw_data = models.JSONField(default=dict, blank=True)
    behavioral_events = models.JSONField(default=list, blank=True)
    performance_metrics = models.JSONField(default=dict, blank=True)
    
    # Trait-specific data
    trait_measurements = models.JSONField(default=dict, blank=True)
    confidence_scores = models.JSONField(default=dict, blank=True)
    
    completed_at = models.DateTimeField(auto_now_add=True)
    
    # Game completion tracking
    COMPLETION_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('incomplete', 'Incomplete'),
        ('abandoned', 'Abandoned'),
    ]
    completion_status = models.CharField(
        max_length=20, 
        choices=COMPLETION_STATUS_CHOICES, 
        default='incomplete',
        help_text="Whether the game was fully completed or abandoned early"
    )
    
    # Data quality and validation
    data_completeness = models.FloatField(default=0.0, help_text="Percentage of expected data collected")
    data_quality_score = models.FloatField(default=0.0, help_text="Quality assessment of collected data")
    validation_status = models.CharField(max_length=20, default='pending',
                                       choices=[('pending', 'Pending'), ('valid', 'Valid'), ('invalid', 'Invalid')])
    
    def __str__(self):
        return f"{self.user.username} - {self.get_game_type_display()} - {self.score}"
    
    def get_game_name(self):
        """Get the display name of the game"""
        game_names = {
            # Core Neuroscience Games
            'balloon_risk': 'Balloon Risk Game',
            'memory_cards': 'Cognitive Atlas Challenge',
            'reaction_timer': 'Reaction Timer Game',
            'sorting_task': 'Sorting Task Game',
            'pattern_completion': 'Pattern Completion Game',
            'stroop_test': 'Stroop Test Game',
            'tower_of_hanoi': 'Tower of Hanoi Game',
            'emotional_faces': 'Emotional Faces Game',
            'trust_game': 'Trust Game',
            'stop_signal': 'Stop Signal Game',
            'digit_span': 'Digit Span Game',
            'fairness_game': 'Fairness Game',
            
            # Additional Core Games
            'money_exchange_1': 'Money Exchange Game #1',
            'money_exchange_2': 'Money Exchange Game #2',
            'easy_or_hard': 'Easy or Hard Game',
            'cards_game': 'Cards Game (Iowa Gambling)',
            'arrows_game': 'Arrows Game',
            'lengths_game': 'Lengths Game',
            'keypresses': 'Keypresses Game',
            'faces_game': 'Faces Game',
            
            # Numerical & Logical Reasoning Games
            'letters': 'Letters Game (N-back)',
            'magnitudes': 'Magnitudes Game',
            'sequences': 'Sequences Game',
            'shapes': 'Shapes Game',
        }
        return game_names.get(self.game_type, self.game_type.replace('_', ' ').title())
    
    def get_game_trait(self):
        """Get the primary trait measured by this game"""
        game_traits = {
            # Core Neuroscience Games
            'balloon_risk': 'Risk Tolerance',
            'memory_cards': 'Working Memory',
            'reaction_timer': 'Reaction Speed',
            'sorting_task': 'Cognitive Flexibility',
            'pattern_completion': 'Pattern Recognition',
            'stroop_test': 'Cognitive Control',
            'tower_of_hanoi': 'Planning & Problem Solving',
            'emotional_faces': 'Emotional Intelligence',
            'trust_game': 'Trust & Cooperation',
            'stop_signal': 'Impulse Control',
            'digit_span': 'Working Memory',
            'fairness_game': 'Fairness Perception',
            
            # Additional Core Games
            'money_exchange_1': 'Trust & Reciprocity',
            'money_exchange_2': 'Altruism & Fairness',
            'easy_or_hard': 'Effort Allocation',
            'cards_game': 'Risk Assessment',
            'arrows_game': 'Task Switching',
            'lengths_game': 'Attention to Detail',
            'keypresses': 'Motor Control',
            'faces_game': 'Emotion Recognition',
            
            # Numerical & Logical Reasoning Games
            'letters': 'Working Memory (N-back)',
            'magnitudes': 'Quantitative Reasoning',
            'sequences': 'Sequential Reasoning',
            'shapes': 'Spatial Reasoning',
        }
        return game_traits.get(self.game_type, 'Cognitive Ability')
    
    def get_game_icon(self):
        """Get the emoji icon for the game"""
        game_icons = {
            # Core Neuroscience Games
            'balloon_risk': '🎈',
            'memory_cards': '🃏',
            'reaction_timer': '⚡',
            'sorting_task': '📦',
            'pattern_completion': '🔢',
            'stroop_test': '🎨',
            'tower_of_hanoi': '🗼',
            'emotional_faces': '😊',
            'trust_game': '🤝',
            'stop_signal': '🛑',
            'digit_span': '🔢',
            'fairness_game': '⚖️',
            
            # Additional Core Games
            'money_exchange_1': '💰',
            'money_exchange_2': '💸',
            'easy_or_hard': '🎯',
            'cards_game': '🃏',
            'arrows_game': '➡️',
            'lengths_game': '📏',
            'keypresses': '⌨️',
            'faces_game': '😐',
            
            # Numerical & Logical Reasoning Games
            'letters': '🔤',
            'magnitudes': '📊',
            'sequences': '🔗',
            'shapes': '🔷',
        }
        return game_icons.get(self.game_type, '🎮')
    
    def get_measured_traits(self):
        """Get all traits measured by this game (expanded to 90+ traits)"""
        trait_mappings = {
            'balloon_risk': [
                'risk_tolerance', 'decision_making', 'pattern_recognition',
                'learning_ability', 'emotional_regulation', 'consistency',
                'adaptation_rate', 'risk_assessment', 'impulse_control'
            ],
            'memory_cards': [
                'working_memory', 'attention', 'pattern_recognition',
                'learning_improvement', 'strategy_adaptation', 'focus_duration',
                'memory_accuracy', 'cognitive_flexibility'
            ],
            'reaction_timer': [
                'reaction_speed', 'attention', 'motor_control',
                'sustained_attention', 'response_consistency', 'fatigue_resistance',
                'cognitive_processing_speed'
            ],
            'trust_game': [
                'trust', 'cooperation', 'reciprocity', 'social_preferences',
                'fairness_perception', 'altruism', 'social_learning'
            ],
            'money_exchange_1': [
                'trust', 'reciprocity', 'social_preferences', 'risk_tolerance',
                'cooperation', 'social_learning'
            ],
            'money_exchange_2': [
                'altruism', 'fairness_perception', 'generosity', 'social_preferences',
                'equity_sensitivity', 'prosocial_behavior'
            ],
            'easy_or_hard': [
                'effort_allocation', 'motivation', 'strategic_decision_making',
                'risk_reward_evaluation', 'goal_directed_behavior', 'effort_persistence'
            ],
            'cards_game': [
                'risk_affinity', 'pattern_recognition', 'learning_ability',
                'methodicalness', 'probabilistic_learning', 'decision_making_uncertainty'
            ],
            'arrows_game': [
                'learning', 'adaptivity', 'attention', 'cognitive_flexibility',
                'perceptual_learning', 'task_switching', 'response_inhibition'
            ],
            'lengths_game': [
                'attention_to_detail', 'motivation', 'learning_ability',
                'perceptual_discrimination', 'selective_attention'
            ],
            'tower_of_hanoi': [
                'problem_solving', 'planning_abilities', 'mental_agility',
                'executive_function', 'strategic_thinking'
            ],
            'faces_game': [
                'emotional_intelligence', 'perception', 'empathy',
                'contextual_interpretation', 'emotion_recognition', 'theory_of_mind'
            ],
            'keypresses': [
                'ability_to_follow_instructions', 'impulsivity', 'motor_function',
                'reaction_time', 'focus', 'sustained_attention'
            ],
            'letters': [
                'working_memory', 'executive_function', 'n_back_performance',
                'cognitive_control', 'memory_span'
            ],
            'magnitudes': [
                'approximate_number_sense', 'magnitude_comparison', 'accuracy',
                'response_time', 'numerical_reasoning'
            ],
            'sequences': [
                'numerical_reasoning', 'pattern_recognition', 'inductive_reasoning',
                'series_completion', 'fluid_intelligence'
            ],
            'shapes': [
                'spatial_reasoning', 'visual_perception', 'spatial_visualization',
                'gestalt_principles', 'pattern_completion'
            ]
        }
        return trait_mappings.get(self.game_type, ['cognitive_ability'])

class DynamicDifficultyConfig(models.Model):
    """Configuration for dynamic difficulty adaptation"""
    
    game_type = models.CharField(max_length=50, choices=GameResult.GAME_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Difficulty parameters
    current_difficulty = models.CharField(max_length=20, default='medium')
    performance_threshold = models.FloatField(default=0.7)
    adaptation_rate = models.FloatField(default=0.1)
    
    # Performance tracking
    recent_scores = models.JSONField(default=list)
    performance_trend = models.FloatField(default=0.0)
    
    # Adaptation history
    difficulty_history = models.JSONField(default=list)
    adaptation_reasons = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['game_type', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.game_type} - {self.current_difficulty}"

class TraitMeasurement(models.Model):
    """Detailed trait measurements for each game session"""
    
    # 9 Bi-directional Dimensions (70-90 traits)
    TRAIT_DIMENSIONS = [
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE)
    
    # Trait identification
    trait_dimension = models.CharField(max_length=20, choices=TRAIT_DIMENSIONS)
    trait_name = models.CharField(max_length=100)
    
    # Measurement values
    raw_score = models.FloatField()
    normalized_score = models.FloatField()
    confidence_interval = models.JSONField(default=dict)
    
    # Scientific validation
    reliability_coefficient = models.FloatField(default=0.0)
    validity_evidence = models.TextField(blank=True)
    
    # Metadata
    measurement_method = models.CharField(max_length=100)
    data_points_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'game_result', 'trait_name']
    
    def __str__(self):
        return f"{self.user.username} - {self.trait_name} - {self.normalized_score}"

class BehavioralEvent(models.Model):
    """Granular behavioral events for detailed analysis"""
    
    EVENT_TYPES = [
        ('user_action', 'User Action'),
        ('system_event', 'System Event'),
        ('performance_metric', 'Performance Metric'),
        ('learning_event', 'Learning Event'),
        ('emotional_response', 'Emotional Response'),
        ('decision_point', 'Decision Point'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE)
    
    # Event details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    timestamp_ms = models.BigIntegerField()
    
    # Event data
    event_data = models.JSONField(default=dict)
    context_data = models.JSONField(default=dict)
    
    # Performance metrics
    reaction_time = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.event_name} - {self.timestamp_ms}"
