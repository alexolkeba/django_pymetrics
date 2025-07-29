"""
Dynamic Difficulty Adaptation System for Django Pymetrics

This module implements real-time difficulty adjustment for all games based on player performance,
ensuring optimal challenge levels and maximum data collection as specified in Pymetrics research.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DifficultyLevel(Enum):
    """Difficulty levels for games."""
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"


@dataclass
class DifficultyConfig:
    """Configuration for difficulty adaptation."""
    game_type: str
    base_difficulty: DifficultyLevel
    adaptation_rate: float
    performance_threshold: float
    min_difficulty: DifficultyLevel
    max_difficulty: DifficultyLevel
    adaptation_window: int  # Number of recent scores to consider


class PerformanceMetrics:
    """Performance metrics for difficulty adaptation."""
    
    def __init__(self):
        self.scores = []
        self.reaction_times = []
        self.accuracy_rates = []
        self.completion_times = []
        self.error_rates = []
        self.timestamps = []
    
    def add_performance(self, score: float, reaction_time: float = None, 
                       accuracy: float = None, completion_time: float = None,
                       error_rate: float = None):
        """Add a new performance measurement."""
        self.scores.append(score)
        if reaction_time is not None:
            self.reaction_times.append(reaction_time)
        if accuracy is not None:
            self.accuracy_rates.append(accuracy)
        if completion_time is not None:
            self.completion_times.append(completion_time)
        if error_rate is not None:
            self.error_rates.append(error_rate)
        self.timestamps.append(datetime.now())
        
        # Keep only recent performance data
        self._trim_old_data()
    
    def _trim_old_data(self, max_age_minutes: int = 30):
        """Remove old performance data."""
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        
        # Find indices to keep
        keep_indices = [i for i, ts in enumerate(self.timestamps) if ts > cutoff_time]
        
        # Trim all lists
        self.scores = [self.scores[i] for i in keep_indices]
        self.reaction_times = [self.reaction_times[i] for i in keep_indices if i < len(self.reaction_times)]
        self.accuracy_rates = [self.accuracy_rates[i] for i in keep_indices if i < len(self.accuracy_rates)]
        self.completion_times = [self.completion_times[i] for i in keep_indices if i < len(self.completion_times)]
        self.error_rates = [self.error_rates[i] for i in keep_indices if i < len(self.error_rates)]
        self.timestamps = [self.timestamps[i] for i in keep_indices]
    
    def get_recent_performance(self, window_size: int = 5) -> Dict[str, float]:
        """Get recent performance metrics."""
        if not self.scores:
            return {}
        
        recent_scores = self.scores[-window_size:]
        recent_reaction_times = self.reaction_times[-window_size:] if self.reaction_times else []
        recent_accuracy = self.accuracy_rates[-window_size:] if self.accuracy_rates else []
        recent_completion = self.completion_times[-window_size:] if self.completion_times else []
        recent_errors = self.error_rates[-window_size:] if self.error_rates else []
        
        return {
            'average_score': np.mean(recent_scores),
            'score_trend': self._calculate_trend(recent_scores),
            'score_consistency': np.std(recent_scores) if len(recent_scores) > 1 else 0,
            'average_reaction_time': np.mean(recent_reaction_times) if recent_reaction_times else None,
            'average_accuracy': np.mean(recent_accuracy) if recent_accuracy else None,
            'average_completion_time': np.mean(recent_completion) if recent_completion else None,
            'average_error_rate': np.mean(recent_errors) if recent_errors else None,
            'performance_count': len(recent_scores)
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend in values (positive = improving, negative = declining)."""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return slope


class DynamicDifficultyAdapter:
    """
    Dynamic difficulty adaptation system that adjusts game difficulty in real-time.
    
    This system ensures players are challenged at their optimal level, maximizing
    both engagement and data collection quality.
    """
    
    def __init__(self):
        """Initialize the dynamic difficulty adapter."""
        self.difficulty_configs = self._initialize_difficulty_configs()
        self.performance_trackers = {}  # user_id -> game_type -> PerformanceMetrics
        self.difficulty_history = {}    # user_id -> game_type -> List[DifficultyLevel]
    
    def _initialize_difficulty_configs(self) -> Dict[str, DifficultyConfig]:
        """Initialize difficulty configurations for all games."""
        return {
            'balloon_risk': DifficultyConfig(
                game_type='balloon_risk',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.15,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=5
            ),
            'memory_cards': DifficultyConfig(
                game_type='memory_cards',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.12,
                performance_threshold=0.75,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=5
            ),
            'reaction_timer': DifficultyConfig(
                game_type='reaction_timer',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.10,
                performance_threshold=0.8,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=8
            ),
            'tower_of_hanoi': DifficultyConfig(
                game_type='tower_of_hanoi',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.18,
                performance_threshold=0.65,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=3
            ),
            'emotional_faces': DifficultyConfig(
                game_type='emotional_faces',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.12,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=6
            ),
            'trust_game': DifficultyConfig(
                game_type='trust_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.14,
                performance_threshold=0.6,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=4
            ),
            'stop_signal': DifficultyConfig(
                game_type='stop_signal',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.13,
                performance_threshold=0.75,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=7
            ),
            'digit_span': DifficultyConfig(
                game_type='digit_span',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.16,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=5
            ),
            'fairness_game': DifficultyConfig(
                game_type='fairness_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.11,
                performance_threshold=0.65,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=5
            ),
            'money_exchange_1': DifficultyConfig(
                game_type='money_exchange_1',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.13,
                performance_threshold=0.6,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=4
            ),
            'money_exchange_2': DifficultyConfig(
                game_type='money_exchange_2',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.13,
                performance_threshold=0.6,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=4
            ),
            'easy_or_hard': DifficultyConfig(
                game_type='easy_or_hard',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.15,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=5
            ),
            'cards_game': DifficultyConfig(
                game_type='cards_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.14,
                performance_threshold=0.65,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=5
            ),
            'arrows_game': DifficultyConfig(
                game_type='arrows_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.12,
                performance_threshold=0.75,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=6
            ),
            'lengths_game': DifficultyConfig(
                game_type='lengths_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.11,
                performance_threshold=0.8,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=7
            ),
            'keypresses': DifficultyConfig(
                game_type='keypresses',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.10,
                performance_threshold=0.8,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=8
            ),
            'faces_game': DifficultyConfig(
                game_type='faces_game',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.12,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=6
            ),
            'letters': DifficultyConfig(
                game_type='letters',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.16,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.VERY_HARD,
                adaptation_window=5
            ),
            'magnitudes': DifficultyConfig(
                game_type='magnitudes',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.13,
                performance_threshold=0.75,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=6
            ),
            'sequences': DifficultyConfig(
                game_type='sequences',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.15,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=5
            ),
            'shapes': DifficultyConfig(
                game_type='shapes',
                base_difficulty=DifficultyLevel.MEDIUM,
                adaptation_rate=0.14,
                performance_threshold=0.7,
                min_difficulty=DifficultyLevel.EASY,
                max_difficulty=DifficultyLevel.HARD,
                adaptation_window=5
            )
        }
    
    def get_initial_difficulty(self, user_id: str, game_type: str) -> DifficultyLevel:
        """Get initial difficulty for a user starting a game."""
        config = self.difficulty_configs.get(game_type)
        if not config:
            return DifficultyLevel.MEDIUM
        
        # Check if user has history with this game
        if user_id in self.performance_trackers and game_type in self.performance_trackers[user_id]:
            # Use last known difficulty or base difficulty
            if user_id in self.difficulty_history and game_type in self.difficulty_history[user_id]:
                return self.difficulty_history[user_id][game_type][-1]
        
        return config.base_difficulty
    
    def update_performance(self, user_id: str, game_type: str, score: float,
                          reaction_time: float = None, accuracy: float = None,
                          completion_time: float = None, error_rate: float = None):
        """Update performance data for a user in a specific game."""
        if user_id not in self.performance_trackers:
            self.performance_trackers[user_id] = {}
        
        if game_type not in self.performance_trackers[user_id]:
            self.performance_trackers[user_id][game_type] = PerformanceMetrics()
        
        tracker = self.performance_trackers[user_id][game_type]
        tracker.add_performance(score, reaction_time, accuracy, completion_time, error_rate)
        
        logger.info(f"Updated performance for user {user_id} in {game_type}: score={score}")
    
    def calculate_new_difficulty(self, user_id: str, game_type: str) -> Tuple[DifficultyLevel, Dict[str, Any]]:
        """Calculate new difficulty level based on recent performance."""
        config = self.difficulty_configs.get(game_type)
        if not config:
            return DifficultyLevel.MEDIUM, {'reason': 'No configuration found'}
        
        # Get current difficulty
        current_difficulty = self.get_current_difficulty(user_id, game_type)
        
        # Get recent performance
        if user_id not in self.performance_trackers or game_type not in self.performance_trackers[user_id]:
            return current_difficulty, {'reason': 'No performance data available'}
        
        performance = self.performance_trackers[user_id][game_type].get_recent_performance(
            config.adaptation_window
        )
        
        if not performance or performance['performance_count'] < 2:
            return current_difficulty, {'reason': 'Insufficient performance data'}
        
        # Calculate difficulty adjustment
        adjustment = self._calculate_difficulty_adjustment(performance, config)
        new_difficulty = self._apply_difficulty_adjustment(current_difficulty, adjustment, config)
        
        # Store difficulty history
        if user_id not in self.difficulty_history:
            self.difficulty_history[user_id] = {}
        if game_type not in self.difficulty_history[user_id]:
            self.difficulty_history[user_id][game_type] = []
        
        self.difficulty_history[user_id][game_type].append(new_difficulty)
        
        # Limit history size
        if len(self.difficulty_history[user_id][game_type]) > 20:
            self.difficulty_history[user_id][game_type] = self.difficulty_history[user_id][game_type][-10:]
        
        return new_difficulty, {
            'reason': 'Performance-based adaptation',
            'performance_metrics': performance,
            'adjustment': adjustment,
            'previous_difficulty': current_difficulty
        }
    
    def _calculate_difficulty_adjustment(self, performance: Dict[str, float], 
                                       config: DifficultyConfig) -> float:
        """Calculate difficulty adjustment based on performance."""
        average_score = performance.get('average_score', 0.5)
        score_trend = performance.get('score_trend', 0.0)
        score_consistency = performance.get('score_consistency', 0.0)
        
        # Base adjustment on score performance
        if average_score > config.performance_threshold + 0.1:
            # High performance - increase difficulty
            base_adjustment = config.adaptation_rate
        elif average_score < config.performance_threshold - 0.1:
            # Low performance - decrease difficulty
            base_adjustment = -config.adaptation_rate
        else:
            # Good performance range - small adjustment based on trend
            base_adjustment = score_trend * config.adaptation_rate * 0.5
        
        # Adjust based on consistency
        if score_consistency < 0.1:
            # Very consistent - can handle more challenge
            base_adjustment *= 1.2
        elif score_consistency > 0.3:
            # Inconsistent - be more conservative
            base_adjustment *= 0.8
        
        # Adjust based on trend
        if abs(score_trend) > 0.05:
            # Clear trend - amplify adjustment
            base_adjustment *= 1.1
        
        return base_adjustment
    
    def _apply_difficulty_adjustment(self, current_difficulty: DifficultyLevel, 
                                   adjustment: float, config: DifficultyConfig) -> DifficultyLevel:
        """Apply difficulty adjustment within bounds."""
        difficulty_levels = list(DifficultyLevel)
        current_index = difficulty_levels.index(current_difficulty)
        
        # Calculate new index
        if adjustment > 0:
            # Increase difficulty
            new_index = min(current_index + 1, difficulty_levels.index(config.max_difficulty))
        elif adjustment < 0:
            # Decrease difficulty
            new_index = max(current_index - 1, difficulty_levels.index(config.min_difficulty))
        else:
            # No change
            new_index = current_index
        
        return difficulty_levels[new_index]
    
    def get_current_difficulty(self, user_id: str, game_type: str) -> DifficultyLevel:
        """Get current difficulty for a user in a specific game."""
        if (user_id in self.difficulty_history and 
            game_type in self.difficulty_history[user_id] and 
            self.difficulty_history[user_id][game_type]):
            return self.difficulty_history[user_id][game_type][-1]
        
        config = self.difficulty_configs.get(game_type)
        return config.base_difficulty if config else DifficultyLevel.MEDIUM
    
    def get_difficulty_parameters(self, game_type: str, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Get game-specific parameters for a difficulty level."""
        # Game-specific difficulty parameters
        difficulty_params = {
            'balloon_risk': {
                DifficultyLevel.VERY_EASY: {'max_pumps': 8, 'pop_probability_base': 0.05},
                DifficultyLevel.EASY: {'max_pumps': 12, 'pop_probability_base': 0.08},
                DifficultyLevel.MEDIUM: {'max_pumps': 16, 'pop_probability_base': 0.12},
                DifficultyLevel.HARD: {'max_pumps': 20, 'pop_probability_base': 0.18},
                DifficultyLevel.VERY_HARD: {'max_pumps': 25, 'pop_probability_base': 0.25}
            },
            'memory_cards': {
                DifficultyLevel.VERY_EASY: {'grid_size': 4, 'time_limit': 120},
                DifficultyLevel.EASY: {'grid_size': 6, 'time_limit': 100},
                DifficultyLevel.MEDIUM: {'grid_size': 8, 'time_limit': 80},
                DifficultyLevel.HARD: {'grid_size': 10, 'time_limit': 60},
                DifficultyLevel.VERY_HARD: {'grid_size': 12, 'time_limit': 45}
            },
            'reaction_timer': {
                DifficultyLevel.VERY_EASY: {'min_interval': 2000, 'max_interval': 4000},
                DifficultyLevel.EASY: {'min_interval': 1500, 'max_interval': 3500},
                DifficultyLevel.MEDIUM: {'min_interval': 1000, 'max_interval': 3000},
                DifficultyLevel.HARD: {'min_interval': 800, 'max_interval': 2500},
                DifficultyLevel.VERY_HARD: {'min_interval': 600, 'max_interval': 2000}
            },
            'tower_of_hanoi': {
                DifficultyLevel.VERY_EASY: {'disk_count': 3, 'time_limit': 300},
                DifficultyLevel.EASY: {'disk_count': 4, 'time_limit': 240},
                DifficultyLevel.MEDIUM: {'disk_count': 5, 'time_limit': 180},
                DifficultyLevel.HARD: {'disk_count': 6, 'time_limit': 120},
                DifficultyLevel.VERY_HARD: {'disk_count': 7, 'time_limit': 90}
            }
        }
        
        game_params = difficulty_params.get(game_type, {})
        return game_params.get(difficulty, {})
    
    def get_adaptation_summary(self, user_id: str, game_type: str) -> Dict[str, Any]:
        """Get summary of difficulty adaptation for a user."""
        if user_id not in self.performance_trackers or game_type not in self.performance_trackers[user_id]:
            return {'error': 'No performance data available'}
        
        performance = self.performance_trackers[user_id][game_type]
        recent_performance = performance.get_recent_performance()
        
        difficulty_history = self.difficulty_history.get(user_id, {}).get(game_type, [])
        
        return {
            'current_difficulty': self.get_current_difficulty(user_id, game_type).value,
            'difficulty_history': [d.value for d in difficulty_history[-10:]],
            'recent_performance': recent_performance,
            'total_performance_count': len(performance.scores),
            'adaptation_active': len(difficulty_history) > 1
        } 