"""
Enhanced Behavioral Data Collector for Django Pymetrics

This module implements comprehensive behavioral data collection that captures 1000+ data points
per session with granular event tracking, real-time processing, and detailed behavioral analysis
as specified in Pymetrics research.
"""

import numpy as np
import logging
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque

from behavioral_data.models import (
    BehavioralSession, BehavioralEvent, BehavioralMetric,
    BalloonRiskEvent, MemoryCardsEvent, ReactionTimerEvent
)
from games.models import GameResult, BehavioralEvent as GameBehavioralEvent

logger = logging.getLogger(__name__)


@dataclass
class BehavioralDataPoint:
    """Individual behavioral data point with comprehensive metadata."""
    timestamp_ms: int
    event_type: str
    event_name: str
    user_id: str
    session_id: str
    game_type: str
    
    # Core behavioral data
    raw_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    
    # Performance metrics
    reaction_time: Optional[float] = None
    accuracy: Optional[float] = None
    confidence: Optional[float] = None
    
    # Context data
    game_state: Dict[str, Any] = None
    user_context: Dict[str, Any] = None
    device_context: Dict[str, Any] = None
    
    # Quality metrics
    data_quality_score: float = 1.0
    validation_status: str = 'pending'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return asdict(self)


class BehavioralDataBuffer:
    """Buffer for real-time behavioral data collection."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.data_points = deque(maxlen=max_size)
        self.session_data = defaultdict(list)
        self.real_time_metrics = defaultdict(dict)
    
    def add_data_point(self, data_point: BehavioralDataPoint):
        """Add a data point to the buffer."""
        self.data_points.append(data_point)
        self.session_data[data_point.session_id].append(data_point)
        
        # Update real-time metrics
        self._update_real_time_metrics(data_point)
    
    def get_session_data(self, session_id: str) -> List[BehavioralDataPoint]:
        """Get all data points for a session."""
        return self.session_data.get(session_id, [])
    
    def get_recent_data(self, minutes: int = 5) -> List[BehavioralDataPoint]:
        """Get recent data points within specified minutes."""
        cutoff_time = int(time.time() * 1000) - (minutes * 60 * 1000)
        return [dp for dp in self.data_points if dp.timestamp_ms >= cutoff_time]
    
    def _update_real_time_metrics(self, data_point: BehavioralDataPoint):
        """Update real-time metrics for the session."""
        session_id = data_point.session_id
        game_type = data_point.game_type
        
        if session_id not in self.real_time_metrics:
            self.real_time_metrics[session_id] = defaultdict(dict)
        
        game_metrics = self.real_time_metrics[session_id][game_type]
        
        # Update event counts
        event_type = data_point.event_type
        if 'event_counts' not in game_metrics:
            game_metrics['event_counts'] = defaultdict(int)
        game_metrics['event_counts'][event_type] += 1
        
        # Update performance metrics
        if data_point.reaction_time is not None:
            if 'reaction_times' not in game_metrics:
                game_metrics['reaction_times'] = []
            game_metrics['reaction_times'].append(data_point.reaction_time)
        
        if data_point.accuracy is not None:
            if 'accuracies' not in game_metrics:
                game_metrics['accuracies'] = []
            game_metrics['accuracies'].append(data_point.accuracy)
        
        # Keep only recent metrics
        self._trim_old_metrics(game_metrics)
    
    def _trim_old_metrics(self, game_metrics: Dict[str, Any], max_age_minutes: int = 10):
        """Remove old metrics to prevent memory bloat."""
        cutoff_time = int(time.time() * 1000) - (max_age_minutes * 60 * 1000)
        
        # Trim reaction times and accuracies based on timestamp
        # This is a simplified version - in practice, you'd store timestamps with each metric
        if 'reaction_times' in game_metrics and len(game_metrics['reaction_times']) > 100:
            game_metrics['reaction_times'] = game_metrics['reaction_times'][-50:]
        
        if 'accuracies' in game_metrics and len(game_metrics['accuracies']) > 100:
            game_metrics['accuracies'] = game_metrics['accuracies'][-50:]


class EnhancedBehavioralCollector:
    """
    Enhanced behavioral data collector that captures 1000+ data points per session.
    
    This system provides comprehensive behavioral tracking with real-time processing,
    quality assessment, and detailed behavioral analysis.
    """
    
    def __init__(self):
        """Initialize the enhanced behavioral collector."""
        self.data_buffer = BehavioralDataBuffer()
        self.session_trackers = {}
        self.data_quality_assessors = {}
        self.real_time_processors = {}
        
        # Initialize data quality thresholds
        self.quality_thresholds = {
            'min_reaction_time': 50,  # milliseconds
            'max_reaction_time': 10000,  # milliseconds
            'min_accuracy': 0.0,
            'max_accuracy': 1.0,
            'min_confidence': 0.0,
            'max_confidence': 1.0,
            'max_session_duration': 7200000,  # 2 hours in milliseconds
        }
    
    def start_session_tracking(self, session_id: str, user_id: str, game_type: str):
        """Start tracking a new session."""
        session_tracker = {
            'session_id': session_id,
            'user_id': user_id,
            'game_type': game_type,
            'start_time': int(time.time() * 1000),
            'data_points_count': 0,
            'quality_score': 1.0,
            'last_activity': int(time.time() * 1000),
            'active': True
        }
        
        self.session_trackers[session_id] = session_tracker
        logger.info(f"Started tracking session {session_id} for user {user_id}")
    
    def collect_behavioral_event(self, session_id: str, event_type: str, event_name: str,
                               raw_data: Dict[str, Any], game_state: Dict[str, Any] = None,
                               user_context: Dict[str, Any] = None,
                               device_context: Dict[str, Any] = None) -> BehavioralDataPoint:
        """Collect a behavioral event with comprehensive data."""
        
        if session_id not in self.session_trackers:
            raise ValueError(f"Session {session_id} not being tracked")
        
        session_tracker = self.session_trackers[session_id]
        
        # Create timestamp
        timestamp_ms = int(time.time() * 1000)
        
        # Process raw data
        processed_data = self._process_raw_data(raw_data, event_type, event_name)
        
        # Extract performance metrics
        performance_metrics = self._extract_performance_metrics(raw_data, event_type)
        
        # Create data point
        data_point = BehavioralDataPoint(
            timestamp_ms=timestamp_ms,
            event_type=event_type,
            event_name=event_name,
            user_id=session_tracker['user_id'],
            session_id=session_id,
            game_type=session_tracker['game_type'],
            raw_data=raw_data,
            processed_data=processed_data,
            reaction_time=performance_metrics.get('reaction_time'),
            accuracy=performance_metrics.get('accuracy'),
            confidence=performance_metrics.get('confidence'),
            game_state=game_state or {},
            user_context=user_context or {},
            device_context=device_context or {},
            data_quality_score=self._assess_data_quality(raw_data, processed_data),
            validation_status='pending'
        )
        
        # Add to buffer
        self.data_buffer.add_data_point(data_point)
        
        # Update session tracker
        session_tracker['data_points_count'] += 1
        session_tracker['last_activity'] = timestamp_ms
        
        # Real-time processing
        self._process_real_time(data_point)
        
        logger.debug(f"Collected behavioral event: {event_type}/{event_name} for session {session_id}")
        
        return data_point
    
    def _process_raw_data(self, raw_data: Dict[str, Any], event_type: str, event_name: str) -> Dict[str, Any]:
        """Process raw behavioral data into structured format."""
        processed = {
            'event_type': event_type,
            'event_name': event_name,
            'timestamp': raw_data.get('timestamp', int(time.time() * 1000)),
            'processed_at': int(time.time() * 1000)
        }
        
        # Game-specific processing
        if event_type == 'balloon_risk':
            processed.update(self._process_balloon_risk_data(raw_data))
        elif event_type == 'memory_cards':
            processed.update(self._process_memory_cards_data(raw_data))
        elif event_type == 'reaction_timer':
            processed.update(self._process_reaction_timer_data(raw_data))
        else:
            # Generic processing
            processed.update(self._process_generic_data(raw_data))
        
        return processed
    
    def _process_balloon_risk_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process balloon risk game data."""
        return {
            'balloon_id': raw_data.get('balloon_id'),
            'pump_number': raw_data.get('pump_number'),
            'balloon_size': raw_data.get('balloon_size'),
            'current_earnings': raw_data.get('current_earnings'),
            'total_earnings': raw_data.get('total_earnings'),
            'time_since_prev_pump': raw_data.get('time_since_prev_pump'),
            'is_new_personal_max': raw_data.get('is_new_personal_max', False),
            'is_rapid_pump': raw_data.get('is_rapid_pump', False),
            'hesitation_time': raw_data.get('hesitation_time'),
            'risk_level': self._calculate_risk_level(raw_data),
            'learning_pattern': self._detect_learning_pattern(raw_data)
        }
    
    def _process_memory_cards_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process memory cards game data."""
        return {
            'card_id': raw_data.get('card_id'),
            'card_position': raw_data.get('card_position'),
            'card_value': raw_data.get('card_value'),
            'round_number': raw_data.get('round_number'),
            'cards_flipped': raw_data.get('cards_flipped'),
            'matches_found': raw_data.get('matches_found'),
            'is_correct_match': raw_data.get('is_correct_match'),
            'memory_accuracy': raw_data.get('memory_accuracy'),
            'strategy_pattern': self._detect_memory_strategy(raw_data)
        }
    
    def _process_reaction_timer_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process reaction timer game data."""
        return {
            'trial_number': raw_data.get('trial_number'),
            'block_number': raw_data.get('block_number'),
            'stimulus_type': raw_data.get('stimulus_type'),
            'stimulus_time': raw_data.get('stimulus_time'),
            'response_time': raw_data.get('response_time'),
            'is_correct': raw_data.get('is_correct'),
            'accuracy': raw_data.get('accuracy'),
            'attention_pattern': self._detect_attention_pattern(raw_data)
        }
    
    def _process_generic_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process generic game data."""
        return {
            'score': raw_data.get('score'),
            'duration': raw_data.get('duration'),
            'attempts': raw_data.get('attempts'),
            'errors': raw_data.get('errors'),
            'completion_status': raw_data.get('completion_status')
        }
    
    def _extract_performance_metrics(self, raw_data: Dict[str, Any], event_type: str) -> Dict[str, float]:
        """Extract performance metrics from raw data."""
        metrics = {}
        
        # Reaction time
        if 'reaction_time' in raw_data:
            metrics['reaction_time'] = float(raw_data['reaction_time'])
        elif 'response_time' in raw_data:
            metrics['reaction_time'] = float(raw_data['response_time'])
        
        # Accuracy
        if 'accuracy' in raw_data:
            metrics['accuracy'] = float(raw_data['accuracy'])
        elif 'is_correct' in raw_data:
            metrics['accuracy'] = 1.0 if raw_data['is_correct'] else 0.0
        
        # Confidence (if available)
        if 'confidence' in raw_data:
            metrics['confidence'] = float(raw_data['confidence'])
        
        return metrics
    
    def _assess_data_quality(self, raw_data: Dict[str, Any], processed_data: Dict[str, Any]) -> float:
        """Assess the quality of collected data."""
        quality_score = 1.0
        
        # Check for missing critical data
        if not raw_data:
            quality_score *= 0.5
        
        # Check timestamp validity
        timestamp = raw_data.get('timestamp')
        if timestamp:
            current_time = int(time.time() * 1000)
            time_diff = abs(current_time - timestamp)
            if time_diff > 60000:  # More than 1 minute difference
                quality_score *= 0.8
        
        # Check performance metrics validity
        if 'reaction_time' in processed_data:
            rt = processed_data['reaction_time']
            if rt < self.quality_thresholds['min_reaction_time'] or rt > self.quality_thresholds['max_reaction_time']:
                quality_score *= 0.7
        
        if 'accuracy' in processed_data:
            acc = processed_data['accuracy']
            if acc < self.quality_thresholds['min_accuracy'] or acc > self.quality_thresholds['max_accuracy']:
                quality_score *= 0.8
        
        return max(0.0, min(1.0, quality_score))
    
    def _calculate_risk_level(self, raw_data: Dict[str, Any]) -> str:
        """Calculate risk level for balloon risk game."""
        pump_number = raw_data.get('pump_number', 0)
        balloon_size = raw_data.get('balloon_size', 1.0)
        
        if pump_number <= 3:
            return 'low'
        elif pump_number <= 6:
            return 'medium'
        elif pump_number <= 10:
            return 'high'
        else:
            return 'very_high'
    
    def _detect_learning_pattern(self, raw_data: Dict[str, Any]) -> str:
        """Detect learning pattern in balloon risk game."""
        # This would analyze the sequence of decisions to detect learning
        return 'adaptive'  # Placeholder
    
    def _detect_memory_strategy(self, raw_data: Dict[str, Any]) -> str:
        """Detect memory strategy in memory cards game."""
        # This would analyze card selection patterns
        return 'systematic'  # Placeholder
    
    def _detect_attention_pattern(self, raw_data: Dict[str, Any]) -> str:
        """Detect attention pattern in reaction timer game."""
        # This would analyze response patterns
        return 'focused'  # Placeholder
    
    def _process_real_time(self, data_point: BehavioralDataPoint):
        """Process data point in real-time for immediate insights."""
        session_id = data_point.session_id
        
        # Update real-time metrics
        if session_id not in self.real_time_processors:
            self.real_time_processors[session_id] = {
                'event_counts': defaultdict(int),
                'performance_trends': defaultdict(list),
                'quality_metrics': defaultdict(list),
                'anomalies': []
            }
        
        processor = self.real_time_processors[session_id]
        
        # Count events
        processor['event_counts'][data_point.event_type] += 1
        
        # Track performance trends
        if data_point.reaction_time:
            processor['performance_trends']['reaction_times'].append(data_point.reaction_time)
        
        if data_point.accuracy is not None:
            processor['performance_trends']['accuracies'].append(data_point.accuracy)
        
        # Track quality metrics
        processor['quality_metrics']['quality_scores'].append(data_point.data_quality_score)
        
        # Detect anomalies
        if data_point.data_quality_score < 0.5:
            processor['anomalies'].append({
                'timestamp': data_point.timestamp_ms,
                'type': 'low_quality_data',
                'score': data_point.data_quality_score
            })
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of session data."""
        if session_id not in self.session_trackers:
            return {'error': 'Session not found'}
        
        session_tracker = self.session_trackers[session_id]
        session_data = self.data_buffer.get_session_data(session_id)
        
        if not session_data:
            return {'error': 'No data collected for session'}
        
        # Calculate comprehensive metrics
        total_events = len(session_data)
        event_types = defaultdict(int)
        performance_metrics = defaultdict(list)
        quality_scores = []
        
        for data_point in session_data:
            event_types[data_point.event_type] += 1
            
            if data_point.reaction_time:
                performance_metrics['reaction_times'].append(data_point.reaction_time)
            
            if data_point.accuracy is not None:
                performance_metrics['accuracies'].append(data_point.accuracy)
            
            quality_scores.append(data_point.data_quality_score)
        
        # Calculate statistics
        summary = {
            'session_id': session_id,
            'user_id': session_tracker['user_id'],
            'game_type': session_tracker['game_type'],
            'total_data_points': total_events,
            'session_duration_ms': session_data[-1].timestamp_ms - session_data[0].timestamp_ms,
            'event_distribution': dict(event_types),
            'average_quality_score': np.mean(quality_scores) if quality_scores else 0.0,
            'data_completeness': self._calculate_data_completeness(session_data),
            'performance_summary': self._calculate_performance_summary(performance_metrics),
            'real_time_insights': self.real_time_processors.get(session_id, {}),
            'collection_status': 'complete' if not session_tracker['active'] else 'active'
        }
        
        return summary
    
    def _calculate_data_completeness(self, session_data: List[BehavioralDataPoint]) -> float:
        """Calculate data completeness for the session."""
        if not session_data:
            return 0.0
        
        # Count high-quality data points
        high_quality_count = sum(1 for dp in session_data if dp.data_quality_score >= 0.7)
        return high_quality_count / len(session_data)
    
    def _calculate_performance_summary(self, performance_metrics: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculate performance summary statistics."""
        summary = {}
        
        if performance_metrics.get('reaction_times'):
            rt_data = performance_metrics['reaction_times']
            summary['reaction_time'] = {
                'mean': np.mean(rt_data),
                'std': np.std(rt_data),
                'min': np.min(rt_data),
                'max': np.max(rt_data),
                'count': len(rt_data)
            }
        
        if performance_metrics.get('accuracies'):
            acc_data = performance_metrics['accuracies']
            summary['accuracy'] = {
                'mean': np.mean(acc_data),
                'std': np.std(acc_data),
                'min': np.min(acc_data),
                'max': np.max(acc_data),
                'count': len(acc_data)
            }
        
        return summary
    
    def end_session_tracking(self, session_id: str) -> Dict[str, Any]:
        """End tracking for a session and return final summary."""
        if session_id not in self.session_trackers:
            return {'error': 'Session not found'}
        
        session_tracker = self.session_trackers[session_id]
        session_tracker['active'] = False
        session_tracker['end_time'] = int(time.time() * 1000)
        
        # Get final summary
        summary = self.get_session_summary(session_id)
        
        logger.info(f"Ended tracking session {session_id}. Collected {summary.get('total_data_points', 0)} data points")
        
        return summary
    
    def get_data_points_count(self, session_id: str) -> int:
        """Get the number of data points collected for a session."""
        if session_id not in self.session_trackers:
            return 0
        
        return self.session_trackers[session_id]['data_points_count']
    
    def is_session_active(self, session_id: str) -> bool:
        """Check if a session is currently being tracked."""
        if session_id not in self.session_trackers:
            return False
        
        return self.session_trackers[session_id]['active'] 