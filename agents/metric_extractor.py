"""
MetricExtractor Agent for Django Pymetrics

This agent aggregates raw behavioral events into scientifically valid metrics
for trait inference and analysis. It implements statistical calculations and
scientific validation for behavioral data.
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, StdDev, Count, Min, Max
from django.db import transaction

from agents.base_agent import MetricExtractionAgent
from behavioral_data.models import BehavioralSession, BehavioralEvent, BalloonRiskEvent, BehavioralMetric
from behavioral_data.schemas import BalloonRiskSchema
from behavioral_data.validators import BalloonRiskValidator

logger = logging.getLogger(__name__)


class MetricExtractor(MetricExtractionAgent):
    def extract_metrics(self, session_id: str) -> Dict[str, Any]:
        """Alias for extract_session_metrics for Celery task compatibility."""
        return self.extract_session_metrics(session_id)
    """
    Agent for extracting and calculating behavioral metrics from raw events.
    
    This agent implements scientific metric extraction for:
    - Risk tolerance and decision-making patterns
    - Consistency and behavioral stability
    - Learning and adaptation patterns
    - Response time and cognitive processing
    - Emotional regulation and stress responses
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the MetricExtractor agent."""
        super().__init__('metric_extractor', config)
        self.balloon_schema = BalloonRiskSchema()
        self.balloon_validator = BalloonRiskValidator()
        
        # Metric calculation settings
        self.metric_settings = {
            'min_events_for_metrics': 10,
            'confidence_interval_level': 0.95,
            'outlier_threshold': 2.5,  # Standard deviations
            'min_session_duration_ms': 30000,  # 30 seconds
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process session data and extract metrics.
        
        Args:
            data: Session data containing session_id and optional parameters
            
        Returns:
            Dict: Extracted metrics and validation results
        """
        session_id = data.get('session_id')
        if not session_id:
            raise ValueError("session_id is required")
        
        try:
            # Get session and events
            session = BehavioralSession.objects.get(session_id=session_id)
            events = self._get_session_events(session)
            
            if len(events) < self.metric_settings['min_events_for_metrics']:
                return {
                    'processed': False,
                    'error': f'Insufficient events: {len(events)} < {self.metric_settings["min_events_for_metrics"]}',
                    'session_id': session_id
                }
            
            # Extract metrics by game type
            metrics = {}
            
            # Balloon Risk metrics
            balloon_events = [e for e in events if e.get('event_type') == 'balloon_risk']
            if balloon_events:
                metrics['balloon_risk'] = self._extract_balloon_risk_metrics(balloon_events, session)
            
            # Memory Cards metrics (placeholder for future implementation)
            memory_events = [e for e in events if e.get('event_type') == 'memory_cards']
            if memory_events:
                metrics['memory_cards'] = self._extract_memory_cards_metrics(memory_events, session)
            
            # Reaction Timer metrics (placeholder for future implementation)
            reaction_events = [e for e in events if e.get('event_type') == 'reaction_timer']
            if reaction_events:
                metrics['reaction_timer'] = self._extract_reaction_timer_metrics(reaction_events, session)
            
            # Session-level metrics
            metrics['session'] = self._extract_session_metrics(events, session)
            
            # Store metrics in database
            self._store_metrics(metrics, session)
            
            return {
                'processed': True,
                'session_id': session_id,
                'metrics': metrics,
                'timestamp': timezone.now().isoformat(),
                'processing_time': self.get_processing_time()
            }
            
        except BehavioralSession.DoesNotExist:
            return {
                'processed': False,
                'error': f'Session {session_id} not found',
                'session_id': session_id
            }
        except Exception as e:
            self.handle_error(e, context={'session_id': session_id})
            return {
                'processed': False,
                'error': str(e),
                'session_id': session_id
            }
    
    def _get_session_events(self, session: BehavioralSession) -> List[Dict[str, Any]]:
        """Get all events for a session in chronological order."""
        events = BehavioralEvent.objects.filter(session=session).order_by('timestamp')
        
        event_list = []
        for event in events:
            event_data = {
                'event_id': str(event.id),
                'event_type': event.event_type,
                'event_name': event.event_name,
                'timestamp': event.timestamp.isoformat(),
                'timestamp_milliseconds': event.timestamp_milliseconds,
                'event_data': event.event_data,
                'validation_status': event.validation_status
            }
            event_list.append(event_data)
        
        return event_list
    
    def _extract_balloon_risk_metrics(self, events: List[Dict[str, Any]], session: BehavioralSession) -> Dict[str, Any]:
        """Extract metrics from balloon risk game events."""
        metrics = {
            'risk_tolerance': {},
            'consistency': {},
            'learning_patterns': {},
            'decision_speed': {},
            'emotional_regulation': {}
        }
        
        # Extract pump events
        pump_events = []
        cash_out_events = []
        pop_events = []
        
        for event in events:
            event_data = event.get('event_data', {})
            if event_data.get('pump_number') is not None:
                pump_events.append(event_data)
            elif event_data.get('earnings_collected') is not None:
                cash_out_events.append(event_data)
            elif event_data.get('pumps_at_pop') is not None:
                pop_events.append(event_data)
        
        # Risk Tolerance Metrics
        if pump_events:
            pumps_per_balloon = [e.get('pump_number', 0) for e in pump_events]
            metrics['risk_tolerance'] = {
                'avg_pumps_per_balloon': np.mean(pumps_per_balloon),
                'max_pumps_per_balloon': np.max(pumps_per_balloon),
                'risk_escalation_rate': self._calculate_risk_escalation(pump_events),
                'total_balloons_popped': len(pop_events),
                'total_balloons_cashed': len(cash_out_events),
                'pop_rate': len(pop_events) / (len(pop_events) + len(cash_out_events)) if (len(pop_events) + len(cash_out_events)) > 0 else 0
            }
        
        # Consistency Metrics
        if len(pump_events) > 1:
            pump_intervals = [e.get('time_since_prev_pump', 0) for e in pump_events if e.get('time_since_prev_pump')]
            metrics['consistency'] = {
                'pump_interval_std': np.std(pump_intervals) if pump_intervals else 0,
                'pump_interval_cv': np.std(pump_intervals) / np.mean(pump_intervals) if pump_intervals and np.mean(pump_intervals) > 0 else 0,
                'behavioral_consistency_score': self._calculate_behavioral_consistency(pump_events)
            }
        
        # Learning Patterns
        if len(pump_events) > 5:
            metrics['learning_patterns'] = {
                'adaptation_rate': self._calculate_adaptation_rate(pump_events),
                'learning_curve_slope': self._calculate_learning_curve(pump_events),
                'feedback_response': self._calculate_feedback_response(pump_events, pop_events)
            }
        
        # Decision Speed
        if pump_events:
            decision_times = [e.get('time_since_prev_pump', 0) for e in pump_events if e.get('time_since_prev_pump')]
            metrics['decision_speed'] = {
                'avg_decision_time': np.mean(decision_times) if decision_times else 0,
                'decision_time_std': np.std(decision_times) if decision_times else 0,
                'rapid_decision_rate': len([t for t in decision_times if t < 1000]) / len(decision_times) if decision_times else 0
            }
        
        # Emotional Regulation
        if pop_events:
            metrics['emotional_regulation'] = {
                'post_loss_behavior': self._analyze_post_loss_behavior(pump_events, pop_events),
                'stress_response': self._calculate_stress_response(pump_events, pop_events),
                'recovery_time': self._calculate_recovery_time(pump_events, pop_events)
            }
        
        return metrics
    
    def _extract_memory_cards_metrics(self, events: List[Dict[str, Any]], session: BehavioralSession) -> Dict[str, Any]:
        """Extract metrics from memory cards game events (placeholder)."""
        return {
            'memory_accuracy': 0.0,
            'reaction_time': 0.0,
            'learning_rate': 0.0,
            'error_patterns': {}
        }
    
    def _extract_reaction_timer_metrics(self, events: List[Dict[str, Any]], session: BehavioralSession) -> Dict[str, Any]:
        """Extract metrics from reaction timer game events (placeholder)."""
        return {
            'avg_reaction_time': 0.0,
            'reaction_time_std': 0.0,
            'accuracy_rate': 0.0,
            'attention_consistency': 0.0
        }
    
    def _extract_session_metrics(self, events: List[Dict[str, Any]], session: BehavioralSession) -> Dict[str, Any]:
        """Extract session-level metrics."""
        session_duration = (session.session_end_time - session.session_start_time).total_seconds() * 1000 if session.session_end_time else 0
        
        return {
            'total_events': len(events),
            'session_duration_ms': session_duration,
            'events_per_minute': len(events) / (session_duration / 60000) if session_duration > 0 else 0,
            'completion_rate': 1.0 if session.is_completed else 0.0,
            'data_quality_score': self._calculate_data_quality(events)
        }
    
    def _calculate_risk_escalation(self, pump_events: List[Dict[str, Any]]) -> float:
        """Calculate risk escalation rate over time."""
        if len(pump_events) < 2:
            return 0.0
        
        pumps = [e.get('pump_number', 0) for e in pump_events]
        # Calculate if later pumps are higher than earlier ones
        early_pumps = pumps[:len(pumps)//2]
        late_pumps = pumps[len(pumps)//2:]
        
        if not early_pumps or not late_pumps:
            return 0.0
        
        return (np.mean(late_pumps) - np.mean(early_pumps)) / max(np.mean(early_pumps), 1)
    
    def _calculate_behavioral_consistency(self, pump_events: List[Dict[str, Any]]) -> float:
        """Calculate behavioral consistency score."""
        if len(pump_events) < 2:
            return 0.0
        
        pumps = [e.get('pump_number', 0) for e in pump_events]
        intervals = [e.get('time_since_prev_pump', 0) for e in pump_events if e.get('time_since_prev_pump')]
        
        # Consistency based on pump number variance and interval consistency
        pump_cv = np.std(pumps) / np.mean(pumps) if np.mean(pumps) > 0 else 0
        interval_cv = np.std(intervals) / np.mean(intervals) if intervals and np.mean(intervals) > 0 else 0
        
        # Higher consistency = lower coefficients of variation
        consistency_score = max(0, 1 - (pump_cv + interval_cv) / 2)
        return consistency_score
    
    def _calculate_adaptation_rate(self, pump_events: List[Dict[str, Any]]) -> float:
        """Calculate adaptation rate based on learning patterns."""
        if len(pump_events) < 5:
            return 0.0
        
        pumps = [e.get('pump_number', 0) for e in pump_events]
        
        # Split into thirds to analyze adaptation
        third = len(pumps) // 3
        early = pumps[:third]
        middle = pumps[third:2*third]
        late = pumps[2*third:]
        
        if not all([early, middle, late]):
            return 0.0
        
        # Adaptation = improvement in performance over time
        early_avg = np.mean(early)
        late_avg = np.mean(late)
        
        if early_avg == 0:
            return 0.0
        
        adaptation_rate = (late_avg - early_avg) / early_avg
        return max(-1, min(1, adaptation_rate))  # Clamp between -1 and 1
    
    def _calculate_learning_curve(self, pump_events: List[Dict[str, Any]]) -> float:
        """Calculate learning curve slope."""
        if len(pump_events) < 3:
            return 0.0
        
        pumps = [e.get('pump_number', 0) for e in pump_events]
        x = np.arange(len(pumps))
        
        # Linear regression slope
        slope = np.polyfit(x, pumps, 1)[0]
        return slope
    
    def _calculate_feedback_response(self, pump_events: List[Dict[str, Any]], pop_events: List[Dict[str, Any]]) -> float:
        """Calculate response to negative feedback (pops)."""
        if not pop_events:
            return 0.0
        
        # Analyze behavior after pops
        pop_timestamps = [e.get('timestamp_milliseconds', 0) for e in pop_events]
        post_pop_pumps = []
        
        for pump_event in pump_events:
            pump_time = pump_event.get('timestamp_milliseconds', 0)
            # Check if this pump was after a pop
            for pop_time in pop_timestamps:
                if pump_time > pop_time and pump_time < pop_time + 30000:  # Within 30 seconds
                    post_pop_pumps.append(pump_event.get('pump_number', 0))
                    break
        
        if not post_pop_pumps:
            return 0.0
        
        # Calculate if behavior changed after negative feedback
        all_pumps = [e.get('pump_number', 0) for e in pump_events]
        avg_all = np.mean(all_pumps)
        avg_post_pop = np.mean(post_pop_pumps)
        
        if avg_all == 0:
            return 0.0
        
        response_rate = (avg_all - avg_post_pop) / avg_all  # Conservative response
        return max(-1, min(1, response_rate))
    
    def _analyze_post_loss_behavior(self, pump_events: List[Dict[str, Any]], pop_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze behavior after losses."""
        if not pop_events:
            return {'conservative_shift': 0.0, 'recovery_time': 0.0}
        
        # Implementation would analyze behavior changes after pops
        return {'conservative_shift': 0.0, 'recovery_time': 0.0}
    
    def _calculate_stress_response(self, pump_events: List[Dict[str, Any]], pop_events: List[Dict[str, Any]]) -> float:
        """Calculate stress response to losses."""
        if not pop_events:
            return 0.0
        
        # Implementation would measure stress indicators
        return 0.0
    
    def _calculate_recovery_time(self, pump_events: List[Dict[str, Any]], pop_events: List[Dict[str, Any]]) -> float:
        """Calculate time to recover from losses."""
        if not pop_events:
            return 0.0
        
        # Implementation would measure recovery time
        return 0.0
    
    def _calculate_data_quality(self, events: List[Dict[str, Any]]) -> float:
        """Calculate data quality score."""
        if not events:
            return 0.0
        
        valid_events = [e for e in events if e.get('validation_status') == 'valid']
        quality_score = len(valid_events) / len(events)
        
        return quality_score
    
    def _store_metrics(self, metrics: Dict[str, Any], session: BehavioralSession):
        """Store calculated metrics in the database."""
        with transaction.atomic():
            for game_type, game_metrics in metrics.items():
                for metric_category, metric_data in game_metrics.items():
                    if isinstance(metric_data, dict):
                        for metric_name, metric_value in metric_data.items():
                            if isinstance(metric_value, (int, float)):
                                BehavioralMetric.objects.create(
                                    session=session,
                                    metric_type='game_level',
                                    metric_name=f"{game_type}_{metric_category}_{metric_name}",
                                    game_type=game_type,
                                    metric_value=float(metric_value),
                                    metric_unit='score',
                                    sample_size=len(session.events.all()),
                                    calculation_method='MetricExtractor Agent',
                                    calculation_timestamp=timezone.now(),
                                    data_version='1.0'
                                )
    
    def extract_session_metrics(self, session_id: str) -> Dict[str, Any]:
        """Extract metrics for a specific session."""
        return self.process({'session_id': session_id})
    
    def batch_extract_metrics(self, session_ids: List[str]) -> Dict[str, Any]:
        """Extract metrics for multiple sessions."""
        results = {}
        for session_id in session_ids:
            try:
                result = self.extract_session_metrics(session_id)
                results[session_id] = result
            except Exception as e:
                results[session_id] = {'error': str(e)}
        
        return results 