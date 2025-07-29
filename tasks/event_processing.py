"""
Celery Tasks for Event Processing

This module contains Celery tasks for processing behavioral events
and managing event data in the Django Pymetrics system.
"""

import logging
from typing import Dict, Any, List
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from agents.event_logger import EventLogger
from behavioral_data.models import BehavioralEvent, BehavioralSession

logger = logging.getLogger(__name__)

# Import the Celery app from the renamed config file
from celery_config import app


@shared_task(bind=True, name='tasks.event_processing.process_single_event')
def process_single_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single behavioral event.
    
    Args:
        event_data: Event data to process
        
    Returns:
        Dict: Processing results
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        # Process the event
        result = event_logger.run(event_data)
        
        logger.info(f"Successfully processed event: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=60, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.event_processing.process_batch_events')
def process_batch_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process multiple events in a batch.
    
    Args:
        events: List of events to process
        
    Returns:
        Dict: Batch processing results
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        # Process events in batch
        result = event_logger.batch_process_events(events)
        
        logger.info(f"Successfully processed batch: {len(events)} events")
        return result
        
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=120, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.event_processing.process_pending_events')
def process_pending_events(self) -> Dict[str, Any]:
    """
    Process all pending events in the system.
    
    Returns:
        Dict: Processing results
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Get pending events
        pending_events = BehavioralEvent.objects.filter(
            validation_status='pending'
        ).order_by('timestamp')[:100]  # Process in batches of 100
        
        if not pending_events:
            logger.info("No pending events to process")
            return {'processed_count': 0, 'message': 'No pending events'}
        
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        processed_count = 0
        error_count = 0
        
        for event in pending_events:
            try:
                # Convert event to processing format
                event_data = {
                    'session_id': event.session.session_id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp.isoformat(),
                    'event_data': event.event_data
                }
                
                # Process the event
                result = event_logger.process(event_data)
                
                # Mark as processed
                event.validation_status = 'valid'
                event.processing_time = result.get('processing_time', 0)
                event.save()
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing event {event.id}: {str(e)}")
                event.validation_status = 'invalid'
                event.save()
                error_count += 1
        
        result = {
            'processed_count': processed_count,
            'error_count': error_count,
            'total_events': len(pending_events),
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Processed {processed_count} events, {error_count} errors")
        return result
        
    except Exception as e:
        logger.error(f"Error in process_pending_events: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.event_processing.validate_session_events')
def validate_session_events(self, session_id: str) -> Dict[str, Any]:
    """
    Validate all events for a specific session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Validation results
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Get session events
        session = BehavioralSession.objects.get(session_id=session_id)
        events = BehavioralEvent.objects.filter(session=session)
        
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        valid_count = 0
        invalid_count = 0
        
        for event in events:
            try:
                # Validate event data
                event_data = {
                    'session_id': session_id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp.isoformat(),
                    'event_data': event.event_data
                }
                
                # Validate using agent
                event_logger.validate_input(event_data, event_logger.input_schema)
                
                # Mark as valid
                event.validation_status = 'valid'
                event.save()
                valid_count += 1
                
            except Exception as e:
                logger.error(f"Invalid event {event.id}: {str(e)}")
                event.validation_status = 'invalid'
                event.save()
                invalid_count += 1
        
        result = {
            'session_id': session_id,
            'valid_count': valid_count,
            'invalid_count': invalid_count,
            'total_events': len(events),
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Validated session {session_id}: {valid_count} valid, {invalid_count} invalid")
        return result
        
    except BehavioralSession.DoesNotExist:
        logger.error(f"Session {session_id} not found")
        return {'error': f'Session {session_id} not found'}
    except Exception as e:
        logger.error(f"Error validating session {session_id}: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=60, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.event_processing.cleanup_old_events')
def cleanup_old_events(self, days_old: int = 365) -> Dict[str, Any]:
    """
    Clean up old events based on retention policy.
    
    Args:
        days_old: Number of days old to consider for cleanup
        
    Returns:
        Dict: Cleanup results
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        # Perform cleanup
        result = event_logger.cleanup_old_events(days_old)
        
        logger.info(f"Cleaned up old events: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error cleaning up old events: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.event_processing.get_session_summary')
def get_session_summary(self, session_id: str) -> Dict[str, Any]:
    """
    Get a summary of events for a specific session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Session summary
    """
    logger = logging.getLogger('tasks.event_processing')
    
    try:
        # Initialize EventLogger agent
        event_logger = EventLogger()
        
        # Get session events
        events = event_logger.get_session_events(session_id)
        
        # Calculate summary statistics
        event_types = {}
        total_events = len(events)
        
        for event in events:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        result = {
            'session_id': session_id,
            'total_events': total_events,
            'event_types': event_types,
            'first_event': events[0] if events else None,
            'last_event': events[-1] if events else None,
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Generated summary for session {session_id}: {total_events} events")
        return result
        
    except Exception as e:
        logger.error(f"Error getting session summary for {session_id}: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(countdown=60, max_retries=3, exc=e) 