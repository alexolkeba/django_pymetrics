"""
EventLogger Agent for Django Pymetrics

This module implements the EventLogger agent for capturing and processing
behavioral events in real-time with validation and storage.
"""

import logging
from typing import Dict, Any, Optional, List
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .base_agent import EventProcessingAgent
from behavioral_data.models import BehavioralSession, BehavioralEvent, BalloonRiskEvent
from behavioral_data.schemas import BalloonRiskSchema, SessionSchema
from behavioral_data.validators import BalloonRiskValidator, SessionValidator

User = get_user_model()


class EventLogger(EventProcessingAgent):
    """
    EventLogger agent for capturing and processing behavioral events.
    
    This agent handles real-time event capture, validation, and storage
    for all behavioral data in the system.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the EventLogger agent."""
        super().__init__('event_logger', config)
        self.logger = logging.getLogger('agents.event_logger')
        
        # Initialize validators
        self.balloon_validator = BalloonRiskValidator()
        self.session_validator = SessionValidator()
        
        # Initialize schemas
        self.balloon_schema = BalloonRiskSchema()
        self.session_schema = SessionSchema()
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process behavioral event data.
        
        Args:
            data: Event data to process
            
        Returns:
            Dict: Processing results
        """
        try:
            # Extract event information
            session_id = data.get('session_id')
            event_type = data.get('event_type')
            event_data = data.get('event_data', {})
            
            # Validate and store event based on type
            if event_type == 'balloon_risk':
                result = self._process_balloon_risk_event(session_id, event_data)
            elif event_type == 'session_start':
                result = self._process_session_start_event(session_id, event_data)
            elif event_type == 'session_end':
                result = self._process_session_end_event(session_id, event_data)
            else:
                result = self._process_generic_event(session_id, event_type, event_data)
            
            return {
                'processed': True,
                'session_id': session_id,
                'event_type': event_type,
                'timestamp': timezone.now().isoformat(),
                'result': result
            }
            
        except Exception as e:
            self.handle_error(e, {'event_data': data})
            raise
    
    def _process_balloon_risk_event(self, session_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process balloon risk game event.
        
        Args:
            session_id: Session identifier
            event_data: Balloon risk event data
            
        Returns:
            Dict: Processing result
        """
        try:
            # Get or create session
            session = self._get_or_create_session(session_id)
            
            # Validate event data
            validated_data = self._validate_balloon_event(event_data)
            
            # Create balloon risk event
            balloon_event = BalloonRiskEvent.objects.create(
                session=session,
                event_type=validated_data.get('event_type', 'pump'),
                balloon_id=validated_data.get('balloon_id'),
                balloon_index=validated_data.get('balloon_index'),
                balloon_color=validated_data.get('balloon_color'),
                timestamp=timezone.now(),
                timestamp_milliseconds=validated_data.get('timestamp_milliseconds', 0),
                pump_number=validated_data.get('pump_number'),
                time_since_prev_pump=validated_data.get('time_since_prev_pump'),
                balloon_size=validated_data.get('balloon_size'),
                current_earnings=validated_data.get('current_earnings'),
                total_earnings=validated_data.get('total_earnings'),
                outcome=validated_data.get('outcome'),
                earnings_lost=validated_data.get('earnings_lost'),
                is_new_personal_max=validated_data.get('is_new_personal_max'),
                is_rapid_pump=validated_data.get('is_rapid_pump'),
                hesitation_time=validated_data.get('hesitation_time'),
                device_info=validated_data.get('device_info', {}),
                user_context=validated_data.get('user_context', {})
            )
            
            self.log_activity(
                f"Processed balloon risk event: {balloon_event.event_type}",
                level='info',
                balloon_id=balloon_event.balloon_id,
                pump_number=balloon_event.pump_number
            )
            
            return {
                'event_id': str(balloon_event.id),
                'balloon_id': balloon_event.balloon_id,
                'event_type': balloon_event.event_type,
                'processed_at': timezone.now().isoformat()
            }
            
        except Exception as e:
            self.handle_error(e, {'session_id': session_id, 'event_data': event_data})
            raise
    
    def _process_session_start_event(self, session_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process session start event.
        
        Args:
            session_id: Session identifier
            event_data: Session start event data
            
        Returns:
            Dict: Processing result
        """
        try:
            # Validate session data
            validated_data = self.session_schema.validate_session_start(event_data)
            
            # Create or update session
            session, created = BehavioralSession.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'user': self._get_or_create_user(validated_data.get('user_id')),
                    'device_info': validated_data.get('device_info', {}),
                    'session_start_time': timezone.now(),
                    'consent_given': validated_data.get('consent_given', False),
                }
            )
            
            if not created:
                # Update existing session
                session.device_info.update(validated_data.get('device_info', {}))
                session.save()
            
            self.log_activity(
                f"Processed session start event: {session_id}",
                level='info',
                session_created=created,
                user_id=session.user_id
            )
            
            return {
                'session_id': session_id,
                'session_created': created,
                'processed_at': timezone.now().isoformat()
            }
            
        except Exception as e:
            self.handle_error(e, {'session_id': session_id, 'event_data': event_data})
            raise
    
    def _process_session_end_event(self, session_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process session end event.
        
        Args:
            session_id: Session identifier
            event_data: Session end event data
            
        Returns:
            Dict: Processing result
        """
        try:
            # Validate session data
            validated_data = self.session_schema.validate_session_end(event_data)
            
            # Get session and mark as completed
            try:
                session = BehavioralSession.objects.get(session_id=session_id)
                session.complete_session()
                session.total_duration = validated_data.get('total_duration', 0)
                session.total_games_played = validated_data.get('total_games_played', 0)
                session.save()
                
                self.log_activity(
                    f"Processed session end event: {session_id}",
                    level='info',
                    total_duration=session.total_duration,
                    total_games=session.total_games_played
                )
                
                return {
                    'session_id': session_id,
                    'session_completed': True,
                    'total_duration': session.total_duration,
                    'processed_at': timezone.now().isoformat()
                }
                
            except BehavioralSession.DoesNotExist:
                raise ValidationError(f"Session {session_id} not found")
            
        except Exception as e:
            self.handle_error(e, {'session_id': session_id, 'event_data': event_data})
            raise
    
    def _process_generic_event(self, session_id: str, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process generic behavioral event.
        
        Args:
            session_id: Session identifier
            event_type: Type of event
            event_data: Event data
            
        Returns:
            Dict: Processing result
        """
        try:
            # Get or create session
            session = self._get_or_create_session(session_id)
            
            # Create generic behavioral event
            event = BehavioralEvent.objects.create(
                session=session,
                event_type=event_type,
                event_name=event_data.get('event_name', event_type),
                timestamp=timezone.now(),
                timestamp_milliseconds=event_data.get('timestamp_milliseconds', 0),
                event_data=event_data,
                metadata=event_data.get('metadata', {}),
                validation_status='valid'
            )
            
            self.log_activity(
                f"Processed generic event: {event_type}",
                level='info',
                event_id=str(event.id),
                event_name=event.event_name
            )
            
            return {
                'event_id': str(event.id),
                'event_type': event_type,
                'processed_at': timezone.now().isoformat()
            }
            
        except Exception as e:
            self.handle_error(e, {'session_id': session_id, 'event_type': event_type, 'event_data': event_data})
            raise
    
    def _get_or_create_user(self, user_id: Optional[str] = None) -> User:
        """
        Get or create a user for the session.
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            User: User object
        """
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
        
        # Create anonymous user for testing
        user, created = User.objects.get_or_create(
            username=f'anonymous_{timezone.now().timestamp()}',
            defaults={
                'email': f'anonymous_{timezone.now().timestamp()}@example.com',
                'first_name': 'Anonymous',
                'last_name': 'User'
            }
        )
        
        if created:
            self.log_activity(
                f"Created anonymous user: {user.username}",
                level='info'
            )
        
        return user
    
    def _get_or_create_session(self, session_id: str) -> BehavioralSession:
        """
        Get or create a behavioral session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            BehavioralSession: Session object
        """
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
        except BehavioralSession.DoesNotExist:
            # Create new session with default values
            user = self._get_or_create_user()
            session = BehavioralSession.objects.create(
                session_id=session_id,
                user=user,
                device_info={},
                session_start_time=timezone.now()
            )
            
            self.log_activity(
                f"Created new session: {session_id}",
                level='info'
            )
        
        return session
    
    def _validate_balloon_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate balloon risk event data.
        
        Args:
            event_data: Balloon event data
            
        Returns:
            Dict: Validated data
        """
        event_type = event_data.get('event_type', 'pump')
        
        if event_type == 'pump':
            return self.balloon_schema.validate_pump_event(event_data)
        elif event_type == 'cash_out':
            return self.balloon_schema.validate_cash_out_event(event_data)
        elif event_type == 'pop':
            return self.balloon_schema.validate_pop_event(event_data)
        else:
            # For other event types, return as-is with basic validation
            return event_data
    
    def batch_process_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple events in a batch.
        
        Args:
            events: List of events to process
            
        Returns:
            Dict: Batch processing results
        """
        results = []
        errors = []
        
        with transaction.atomic():
            for event in events:
                try:
                    result = self.process(event)
                    results.append(result)
                except Exception as e:
                    error = {
                        'event': event,
                        'error': str(e),
                        'timestamp': timezone.now().isoformat()
                    }
                    errors.append(error)
                    self.handle_error(e, {'event': event})
        
        return {
            'processed_count': len(results),
            'error_count': len(errors),
            'results': results,
            'errors': errors,
            'batch_timestamp': timezone.now().isoformat()
        }
    
    def get_session_events(self, session_id: str, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get events for a specific session.
        
        Args:
            session_id: Session identifier
            event_type: Optional event type filter
            
        Returns:
            List: Session events
        """
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
            
            if event_type:
                events = BehavioralEvent.objects.filter(session=session, event_type=event_type)
            else:
                events = BehavioralEvent.objects.filter(session=session)
            
            return [
                {
                    'id': str(event.id),
                    'event_type': event.event_type,
                    'event_name': event.event_name,
                    'timestamp': event.timestamp.isoformat(),
                    'event_data': event.event_data
                }
                for event in events.order_by('timestamp')
            ]
            
        except BehavioralSession.DoesNotExist:
            raise ValidationError(f"Session {session_id} not found")
    
    def cleanup_old_events(self, days_old: int = 365) -> Dict[str, Any]:
        """
        Clean up old events based on retention policy.
        
        Args:
            days_old: Number of days old to consider for cleanup
            
        Returns:
            Dict: Cleanup results
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        
        # Count events to be deleted
        old_events_count = BehavioralEvent.objects.filter(
            timestamp__lt=cutoff_date
        ).count()
        
        old_sessions_count = BehavioralSession.objects.filter(
            session_start_time__lt=cutoff_date
        ).count()
        
        # Delete old events and sessions
        deleted_events = BehavioralEvent.objects.filter(
            timestamp__lt=cutoff_date
        ).delete()
        
        deleted_sessions = BehavioralSession.objects.filter(
            session_start_time__lt=cutoff_date
        ).delete()
        
        self.log_activity(
            f"Cleaned up old events: {deleted_events[0]} events, {deleted_sessions[0]} sessions",
            level='info',
            cutoff_date=cutoff_date.isoformat(),
            deleted_events=deleted_events[0],
            deleted_sessions=deleted_sessions[0]
        )
        
        return {
            'cutoff_date': cutoff_date.isoformat(),
            'deleted_events': deleted_events[0],
            'deleted_sessions': deleted_sessions[0],
            'cleanup_timestamp': timezone.now().isoformat()
        } 