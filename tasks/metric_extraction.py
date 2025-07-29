"""
Celery Tasks for Metric Extraction

This module contains Celery tasks for extracting behavioral metrics
from raw events in the Django Pymetrics system.
"""

import logging
from typing import Dict, Any, List
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from agents.metric_extractor import MetricExtractor
from behavioral_data.models import BehavioralSession, BehavioralMetric

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='tasks.metric_extraction.extract_session_metrics')
def extract_session_metrics(self, session_id: str) -> Dict[str, Any]:
    """
    Extract metrics for a single session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Extraction results with metrics and validation
    """
    logger = logging.getLogger('tasks.metric_extraction')
    
    try:
        # Validate session exists
        session = BehavioralSession.objects.get(session_id=session_id)
        
        # Initialize MetricExtractor agent
        extractor = MetricExtractor()
        
        # Extract metrics
        result = extractor.extract_session_metrics(session_id)
        
        logger.info(f"Successfully extracted metrics for session {session_id}: {result}")
        return result
        
    except BehavioralSession.DoesNotExist:
        error_msg = f"Session {session_id} not found"
        logger.error(error_msg)
        return {'processed': False, 'error': error_msg, 'session_id': session_id}
        
    except Exception as e:
        logger.error(f"Error extracting metrics for session {session_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=120, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.metric_extraction.extract_batch_metrics')
def extract_batch_metrics(self, session_ids: List[str]) -> Dict[str, Any]:
    """
    Extract metrics for multiple sessions in batch.
    
    Args:
        session_ids: List of session identifiers
        
    Returns:
        Dict: Batch extraction results
    """
    logger = logging.getLogger('tasks.metric_extraction')
    
    try:
        extractor = MetricExtractor()
        results = {}
        
        for session_id in session_ids:
            try:
                result = extractor.extract_session_metrics(session_id)
                results[session_id] = result
            except Exception as e:
                logger.error(f"Error processing session {session_id}: {str(e)}")
                results[session_id] = {'processed': False, 'error': str(e)}
        
        success_count = sum(1 for r in results.values() if r.get('processed', False))
        
        logger.info(f"Batch extraction completed: {success_count}/{len(session_ids)} successful")
        return {
            'processed': True,
            'total_sessions': len(session_ids),
            'successful_sessions': success_count,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Error in batch metric extraction: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.metric_extraction.extract_pending_metrics')
def extract_pending_metrics(self) -> Dict[str, Any]:
    """
    Extract metrics for all sessions that don't have metrics yet.
    
    Returns:
        Dict: Processing results
    """
    logger = logging.getLogger('tasks.metric_extraction')
    
    try:
        # Find sessions without metrics
        sessions_without_metrics = BehavioralSession.objects.filter(
            is_completed=True,
            behavioralmetric__isnull=True
        ).values_list('session_id', flat=True)[:50]  # Process 50 at a time
        
        if not sessions_without_metrics:
            logger.info("No pending sessions for metric extraction")
            return {'processed_count': 0, 'message': 'No pending sessions'}
        
        # Process in batch
        result = extract_batch_metrics.delay(list(sessions_without_metrics))
        
        logger.info(f"Started metric extraction for {len(sessions_without_metrics)} sessions")
        return {
            'processed_count': len(sessions_without_metrics),
            'task_id': result.id,
            'message': 'Batch extraction started'
        }
        
    except Exception as e:
        logger.error(f"Error in pending metric extraction: {str(e)}")
        raise self.retry(countdown=600, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.metric_extraction.validate_metrics')
def validate_metrics(self, session_id: str) -> Dict[str, Any]:
    """
    Validate extracted metrics for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Validation results
    """
    logger = logging.getLogger('tasks.metric_extraction')
    
    try:
        metrics = BehavioralMetric.objects.filter(session__session_id=session_id)
        
        if not metrics.exists():
            return {
                'validated': False,
                'error': 'No metrics found for session',
                'session_id': session_id
            }
        
        # Validate metric quality
        quality_scores = []
        for metric in metrics:
            # Check for reasonable values
            if metric.metric_value is not None:
                if 0 <= metric.metric_value <= 1:  # Normalized metrics
                    quality_scores.append(1.0)
                else:
                    quality_scores.append(0.5)
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        validation_result = {
            'validated': True,
            'session_id': session_id,
            'metric_count': metrics.count(),
            'quality_score': avg_quality,
            'validation_timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Metrics validation completed for session {session_id}: {validation_result}")
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating metrics for session {session_id}: {str(e)}")
        raise self.retry(countdown=60, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.metric_extraction.cleanup_old_metrics')
def cleanup_old_metrics(self, days_old: int = 365) -> Dict[str, Any]:
    """
    Clean up old metrics based on retention policy.
    
    Args:
        days_old: Age threshold for cleanup
        
    Returns:
        Dict: Cleanup results
    """
    logger = logging.getLogger('tasks.metric_extraction')
    
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        
        # Find old metrics
        old_metrics = BehavioralMetric.objects.filter(
            calculation_timestamp__lt=cutoff_date
        )
        
        count = old_metrics.count()
        old_metrics.delete()
        
        logger.info(f"Cleaned up {count} old metrics older than {days_old} days")
        return {
            'cleaned_count': count,
            'cutoff_date': cutoff_date.isoformat(),
            'message': f'Cleaned up {count} old metrics'
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up old metrics: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)
