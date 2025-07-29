"""
Celery Tasks for Trait Inference

This module contains Celery tasks for inferring psychometric traits
from behavioral metrics in the Django Pymetrics system.
"""

import logging
from typing import Dict, Any, List
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from agents.trait_inferencer import TraitInferencer
from behavioral_data.models import BehavioralSession, BehavioralMetric
from ai_model.models import TraitProfile

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='tasks.trait_inference.infer_session_traits')
def infer_session_traits(self, session_id: str) -> Dict[str, Any]:
    """
    Infer traits for a single session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Trait inference results with confidence scores
    """
    logger = logging.getLogger('tasks.trait_inference')
    
    try:
        # Validate session exists and has metrics
        session = BehavioralSession.objects.get(session_id=session_id)
        metrics = BehavioralMetric.objects.filter(session=session)
        
        if not metrics.exists():
            return {
                'processed': False,
                'error': 'No metrics available for trait inference',
                'session_id': session_id
            }
        
        # Initialize TraitInferencer agent
        inferencer = TraitInferencer()
        
        # Infer traits
        result = inferencer.infer_session_traits(session_id)
        
        logger.info(f"Successfully inferred traits for session {session_id}: {result}")
        return result
        
    except BehavioralSession.DoesNotExist:
        error_msg = f"Session {session_id} not found"
        logger.error(error_msg)
        return {'processed': False, 'error': error_msg, 'session_id': session_id}
        
    except Exception as e:
        logger.error(f"Error inferring traits for session {session_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=180, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.trait_inference.infer_batch_traits')
def infer_batch_traits(self, session_ids: List[str]) -> Dict[str, Any]:
    """
    Infer traits for multiple sessions in batch.
    
    Args:
        session_ids: List of session identifiers
        
    Returns:
        Dict: Batch inference results
    """
    logger = logging.getLogger('tasks.trait_inference')
    
    try:
        inferencer = TraitInferencer()
        results = {}
        
        for session_id in session_ids:
            try:
                result = inferencer.infer_session_traits(session_id)
                results[session_id] = result
            except Exception as e:
                logger.error(f"Error processing session {session_id}: {str(e)}")
                results[session_id] = {'processed': False, 'error': str(e)}
        
        success_count = sum(1 for r in results.values() if r.get('processed', False))
        
        logger.info(f"Batch trait inference completed: {success_count}/{len(session_ids)} successful")
        return {
            'processed': True,
            'total_sessions': len(session_ids),
            'successful_sessions': success_count,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Error in batch trait inference: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.trait_inference.generate_trait_profiles')
def generate_trait_profiles(self) -> Dict[str, Any]:
    """
    Generate trait profiles for all sessions with metrics but no profiles.
    
    Returns:
        Dict: Processing results
    """
    logger = logging.getLogger('tasks.trait_inference')
    
    try:
        # Find sessions with metrics but no trait profiles
        sessions_with_metrics = BehavioralSession.objects.filter(
            is_completed=True,
            behavioralmetric__isnull=False
        ).exclude(
            ai_model__traitprofile__isnull=False
        ).values_list('session_id', flat=True)[:50]  # Process 50 at a time
        
        if not sessions_with_metrics:
            logger.info("No pending sessions for trait profile generation")
            return {'processed_count': 0, 'message': 'No pending sessions'}
        
        # Process in batch
        result = infer_batch_traits.delay(list(sessions_with_metrics))
        
        logger.info(f"Started trait profile generation for {len(sessions_with_metrics)} sessions")
        return {
            'processed_count': len(sessions_with_metrics),
            'task_id': result.id,
            'message': 'Batch trait inference started'
        }
        
    except Exception as e:
        logger.error(f"Error in trait profile generation: {str(e)}")
        raise self.retry(countdown=600, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.trait_inference.validate_trait_profiles')
def validate_trait_profiles(self, session_id: str) -> Dict[str, Any]:
    """
    Validate trait profiles for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Validation results
    """
    logger = logging.getLogger('tasks.trait_inference')
    
    try:
        trait_profiles = TraitProfile.objects.filter(session__session_id=session_id)
        
        if not trait_profiles.exists():
            return {
                'validated': False,
                'error': 'No trait profiles found for session',
                'session_id': session_id
            }
        
        # Validate trait profile quality
        validation_results = []
        for profile in trait_profiles:
            # Check confidence scores
            if hasattr(profile, 'confidence_interval') and profile.confidence_interval:
                if profile.confidence_interval >= 0.7:  # 70% confidence threshold
                    validation_results.append(True)
                else:
                    validation_results.append(False)
            else:
                validation_results.append(False)
        
        valid_count = sum(validation_results)
        total_count = len(validation_results)
        
        validation_result = {
            'validated': valid_count > 0,
            'session_id': session_id,
            'profile_count': total_count,
            'valid_profiles': valid_count,
            'validation_score': valid_count / total_count if total_count > 0 else 0,
            'validation_timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Trait profile validation completed for session {session_id}: {validation_result}")
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating trait profiles for session {session_id}: {str(e)}")
        raise self.retry(countdown=60, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.trait_inference.update_trait_mappings')
def update_trait_mappings(self) -> Dict[str, Any]:
    """
    Update trait mapping configurations and models.
    
    Returns:
        Dict: Update results
    """
    logger = logging.getLogger('tasks.trait_inference')
    
    try:
        # This would typically involve updating trait mapping weights,
        # recalibrating models, or updating scientific validation parameters
        # For now, we'll log the task execution
        
        logger.info("Trait mapping update task executed")
        return {
            'updated': True,
            'timestamp': timezone.now().isoformat(),
            'message': 'Trait mapping update completed'
        }
        
    except Exception as e:
        logger.error(f"Error updating trait mappings: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)
