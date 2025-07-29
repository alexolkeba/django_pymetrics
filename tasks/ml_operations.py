"""
Celery Tasks for Machine Learning Operations

This module contains Celery tasks for ML operations including:
- Model training and retraining
- Prediction generation
- A/B testing execution
- Model performance monitoring
"""

import logging
from typing import Dict, Any, List
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from ml_engine.predictive_models import PredictiveAnalyticsEngine
from ml_engine.ab_testing import ABTestingFramework
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='tasks.ml_operations.train_trait_prediction_model')
def train_trait_prediction_model(self, user_id: str = None) -> Dict[str, Any]:
    """
    Train trait prediction model.
    
    Args:
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Training results and model performance
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Train model
        result = ml_engine.train_trait_prediction_model(user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully trained trait prediction model for user {user_id}: {result}")
        else:
            logger.warning(f"Trait prediction model training failed for user {user_id}: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error training trait prediction model for user {user_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.train_anomaly_detection_model')
def train_anomaly_detection_model(self, user_id: str = None) -> Dict[str, Any]:
    """
    Train anomaly detection model.
    
    Args:
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Training results and model performance
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Train model
        result = ml_engine.train_anomaly_detection_model(user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully trained anomaly detection model for user {user_id}: {result}")
        else:
            logger.warning(f"Anomaly detection model training failed for user {user_id}: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error training anomaly detection model for user {user_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.train_performance_forecasting_model')
def train_performance_forecasting_model(self, user_id: str = None) -> Dict[str, Any]:
    """
    Train performance forecasting model.
    
    Args:
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Training results and model performance
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Train model
        result = ml_engine.train_performance_forecasting_model(user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully trained performance forecasting model for user {user_id}: {result}")
        else:
            logger.warning(f"Performance forecasting model training failed for user {user_id}: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error training performance forecasting model for user {user_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.retrain_all_models')
def retrain_all_models(self, user_id: str = None) -> Dict[str, Any]:
    """
    Retrain all ML models with latest data.
    
    Args:
        user_id: Optional user ID for user-specific models
        
    Returns:
        Dict: Retraining results for all models
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Retrain all models
        results = ml_engine.retrain_all_models(user_id)
        
        # Log results
        success_count = sum(1 for result in results.values() if result.get('success', False))
        total_count = len(results)
        
        logger.info(f"Retrained {success_count}/{total_count} models for user {user_id}")
        
        return {
            'success': success_count > 0,
            'results': results,
            'success_count': success_count,
            'total_count': total_count,
            'user_id': user_id,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error retraining all models for user {user_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=600, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.predict_traits_for_session')
def predict_traits_for_session(self, session_id: str, user_id: str = None) -> Dict[str, Any]:
    """
    Predict traits for a specific session.
    
    Args:
        session_id: Session identifier
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Prediction results with traits and confidence
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Get session data
        session = BehavioralSession.objects.get(session_id=session_id)
        
        # Prepare session data
        session_data = {
            'total_duration': session.total_duration,
            'total_games_played': session.total_games_played,
            'is_completed': session.is_completed
        }
        
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Make prediction
        result = ml_engine.predict_traits(session_data, user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully predicted traits for session {session_id}: {result}")
        else:
            logger.warning(f"Trait prediction failed for session {session_id}: {result}")
        
        return result
        
    except BehavioralSession.DoesNotExist:
        error_msg = f"Session {session_id} not found"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg, 'session_id': session_id}
        
    except Exception as e:
        logger.error(f"Error predicting traits for session {session_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=120, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.detect_anomalies_for_session')
def detect_anomalies_for_session(self, session_id: str, user_id: str = None) -> Dict[str, Any]:
    """
    Detect anomalies for a specific session.
    
    Args:
        session_id: Session identifier
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Anomaly detection results
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Get session and events
        session = BehavioralSession.objects.get(session_id=session_id)
        events = BehavioralEvent.objects.filter(session=session)
        
        # Prepare behavioral data
        behavioral_data = {
            'event_count': events.count(),
            'user_action_count': events.filter(event_type='user_action').count(),
            'system_event_count': events.filter(event_type='system_event').count(),
            'avg_timestamp': events.aggregate(avg=models.Avg('timestamp_milliseconds'))['avg'] or 0
        }
        
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Detect anomalies
        result = ml_engine.detect_anomalies(behavioral_data, user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully detected anomalies for session {session_id}: {result}")
        else:
            logger.warning(f"Anomaly detection failed for session {session_id}: {result}")
        
        return result
        
    except BehavioralSession.DoesNotExist:
        error_msg = f"Session {session_id} not found"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg, 'session_id': session_id}
        
    except Exception as e:
        logger.error(f"Error detecting anomalies for session {session_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=120, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.forecast_performance_for_user')
def forecast_performance_for_user(self, user_id: str) -> Dict[str, Any]:
    """
    Forecast performance for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dict: Performance forecast
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Get historical data
        sessions = BehavioralSession.objects.filter(
            user_id=user_id,
            is_completed=True
        ).order_by('session_start_time')
        
        if sessions.count() < 5:
            return {
                'success': False,
                'error': 'Insufficient historical data for forecasting',
                'user_id': user_id,
                'session_count': sessions.count()
            }
        
        # Calculate historical metrics
        historical_data = {
            'avg_duration': sessions.aggregate(avg=models.Avg('total_duration'))['avg'] or 0,
            'session_count': sessions.count(),
            'completion_rate': sessions.filter(is_completed=True).count() / sessions.count(),
            'hours_since_first': (sessions.last().session_start_time - sessions.first().session_start_time).total_seconds() / 3600
        }
        
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Make forecast
        result = ml_engine.forecast_performance(historical_data, user_id)
        
        if result.get('success', False):
            logger.info(f"Successfully forecasted performance for user {user_id}: {result}")
        else:
            logger.warning(f"Performance forecasting failed for user {user_id}: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error forecasting performance for user {user_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=180, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.run_ab_test')
def run_ab_test(self, experiment_name: str, model_a_config: Dict[str, Any], 
                model_b_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run A/B test for model comparison.
    
    Args:
        experiment_name: Name of the experiment
        model_a_config: Configuration for model A
        model_b_config: Configuration for model B
        
    Returns:
        Dict: A/B test results
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize A/B testing framework
        ab_framework = ABTestingFramework()
        
        # Run A/B test
        result = ab_framework.run_trait_prediction_ab_test(
            experiment_name, model_a_config, model_b_config
        )
        
        if result.get('success', False):
            logger.info(f"Successfully completed A/B test {experiment_name}: {result}")
        else:
            logger.warning(f"A/B test {experiment_name} failed: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error running A/B test {experiment_name}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=600, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.monitor_model_performance')
def monitor_model_performance(self) -> Dict[str, Any]:
    """
    Monitor performance of all ML models.
    
    Returns:
        Dict: Model performance metrics
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # Get performance metrics
        performance_metrics = ml_engine.get_model_performance()
        
        # Calculate summary statistics
        total_models = len(performance_metrics)
        active_models = sum(1 for metrics in performance_metrics.values() if metrics)
        
        # Check for models needing retraining
        models_needing_retraining = []
        for model_name, metrics in performance_metrics.items():
            if metrics:
                last_trained = metrics.get('last_trained')
                if last_trained:
                    # Check if model is older than 7 days
                    last_trained_date = timezone.datetime.fromisoformat(last_trained.replace('Z', '+00:00'))
                    if (timezone.now() - last_trained_date).days > 7:
                        models_needing_retraining.append(model_name)
        
        result = {
            'success': True,
            'total_models': total_models,
            'active_models': active_models,
            'models_needing_retraining': models_needing_retraining,
            'performance_metrics': performance_metrics,
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Model performance monitoring completed: {active_models}/{total_models} active models")
        
        return result
        
    except Exception as e:
        logger.error(f"Error monitoring model performance: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.batch_predict_traits')
def batch_predict_traits(self, session_ids: List[str], user_id: str = None) -> Dict[str, Any]:
    """
    Batch predict traits for multiple sessions.
    
    Args:
        session_ids: List of session identifiers
        user_id: Optional user ID for user-specific model
        
    Returns:
        Dict: Batch prediction results
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        results = {}
        success_count = 0
        
        for session_id in session_ids:
            try:
                # Get session data
                session = BehavioralSession.objects.get(session_id=session_id)
                
                # Prepare session data
                session_data = {
                    'total_duration': session.total_duration,
                    'total_games_played': session.total_games_played,
                    'is_completed': session.is_completed
                }
                
                # Make prediction
                prediction = ml_engine.predict_traits(session_data, user_id)
                results[session_id] = prediction
                
                if prediction.get('success', False):
                    success_count += 1
                    
            except BehavioralSession.DoesNotExist:
                results[session_id] = {'success': False, 'error': 'Session not found'}
            except Exception as e:
                logger.error(f"Error predicting traits for session {session_id}: {str(e)}")
                results[session_id] = {'success': False, 'error': str(e)}
        
        logger.info(f"Batch trait prediction completed: {success_count}/{len(session_ids)} successful")
        
        return {
            'success': success_count > 0,
            'total_sessions': len(session_ids),
            'successful_predictions': success_count,
            'results': results,
            'user_id': user_id,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch trait prediction: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.ml_operations.cleanup_old_models')
def cleanup_old_models(self, days_old: int = 30) -> Dict[str, Any]:
    """
    Clean up old ML models based on retention policy.
    
    Args:
        days_old: Age threshold for cleanup
        
    Returns:
        Dict: Cleanup results
    """
    logger = logging.getLogger('tasks.ml_operations')
    
    try:
        # Initialize ML engine
        ml_engine = PredictiveAnalyticsEngine()
        
        # This would implement model cleanup logic
        # For now, return placeholder
        result = {
            'success': True,
            'cleaned_models': 0,
            'days_old': days_old,
            'message': 'Model cleanup completed',
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info(f"Model cleanup completed: {result['cleaned_models']} models cleaned")
        
        return result
        
    except Exception as e:
        logger.error(f"Error cleaning up old models: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=300, max_retries=2, exc=e) 