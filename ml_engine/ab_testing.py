"""
A/B Testing Framework for Django Pymetrics

This module provides A/B testing capabilities for:
- Model versioning and comparison
- Performance evaluation
- Statistical validation
- Results analysis
"""

import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from scipy import stats
from sklearn.metrics import mean_squared_error, accuracy_score
import random

from django.utils import timezone
from django.conf import settings
from behavioral_data.models import BehavioralSession, BehavioralEvent
from ai_model.models import TraitProfile
from ml_engine.predictive_models import PredictiveAnalyticsEngine

logger = logging.getLogger(__name__)


class ABTestingFramework:
    """
    A/B testing framework for model comparison and validation.
    
    Provides capabilities for:
    - Model versioning and deployment
    - Statistical comparison of models
    - Performance evaluation
    - Results analysis and reporting
    """
    
    def __init__(self):
        """Initialize the A/B testing framework."""
        self.experiments = {}
        self.results = {}
        self.ml_engine = PredictiveAnalyticsEngine()
        
        # A/B testing configuration
        self.ab_config = {
            'traffic_split': 0.5,  # 50/50 split
            'confidence_level': 0.95,  # 95% confidence
            'minimum_sample_size': 100,  # Minimum samples per variant
            'test_duration_days': 7,  # Test duration in days
            'metrics': ['accuracy', 'precision', 'recall', 'f1_score']
        }
    
    def create_experiment(self, experiment_name: str, model_a: str, model_b: str, 
                         experiment_type: str = 'model_comparison') -> Dict[str, Any]:
        """
        Create a new A/B testing experiment.
        
        Args:
            experiment_name: Name of the experiment
            model_a: Model A identifier
            model_b: Model B identifier
            experiment_type: Type of experiment
            
        Returns:
            Dict: Experiment configuration
        """
        try:
            experiment_id = f"{experiment_name}_{int(timezone.now().timestamp())}"
            
            experiment_config = {
                'experiment_id': experiment_id,
                'experiment_name': experiment_name,
                'model_a': model_a,
                'model_b': model_b,
                'experiment_type': experiment_type,
                'traffic_split': self.ab_config['traffic_split'],
                'confidence_level': self.ab_config['confidence_level'],
                'start_time': timezone.now().isoformat(),
                'status': 'active',
                'results': {
                    'model_a': {'predictions': [], 'actual': [], 'metrics': {}},
                    'model_b': {'predictions': [], 'actual': [], 'metrics': {}}
                }
            }
            
            self.experiments[experiment_id] = experiment_config
            
            logger.info(f"Created A/B experiment: {experiment_id}")
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'config': experiment_config
            }
            
        except Exception as e:
            logger.error(f"Error creating experiment: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def assign_variant(self, user_id: str, experiment_id: str) -> str:
        """
        Assign user to A or B variant for an experiment.
        
        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            
        Returns:
            str: Variant assignment ('A' or 'B')
        """
        try:
            if experiment_id not in self.experiments:
                return 'A'  # Default to A if experiment not found
            
            # Use user_id hash for consistent assignment
            user_hash = hash(user_id) % 100
            traffic_split = self.experiments[experiment_id]['traffic_split']
            
            if user_hash < (traffic_split * 100):
                return 'A'
            else:
                return 'B'
                
        except Exception as e:
            logger.error(f"Error assigning variant: {str(e)}")
            return 'A'  # Default to A on error
    
    def record_prediction(self, experiment_id: str, variant: str, 
                         prediction: Dict[str, Any], actual: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Record prediction results for A/B testing.
        
        Args:
            experiment_id: Experiment identifier
            variant: Variant ('A' or 'B')
            prediction: Model prediction
            actual: Actual values (if available)
            
        Returns:
            Dict: Recording result
        """
        try:
            if experiment_id not in self.experiments:
                return {
                    'success': False,
                    'error': 'Experiment not found'
                }
            
            # Record prediction
            self.experiments[experiment_id]['results'][f'model_{variant.lower()}']['predictions'].append(prediction)
            
            if actual:
                self.experiments[experiment_id]['results'][f'model_{variant.lower()}']['actual'].append(actual)
            
            logger.info(f"Recorded prediction for experiment {experiment_id}, variant {variant}")
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'variant': variant
            }
            
        except Exception as e:
            logger.error(f"Error recording prediction: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_experiment_metrics(self, experiment_id: str) -> Dict[str, Any]:
        """
        Calculate metrics for A/B experiment.
        
        Args:
            experiment_id: Experiment identifier
            
        Returns:
            Dict: Calculated metrics and statistical analysis
        """
        try:
            if experiment_id not in self.experiments:
                return {
                    'success': False,
                    'error': 'Experiment not found'
                }
            
            experiment = self.experiments[experiment_id]
            results = experiment['results']
            
            metrics = {}
            
            for variant in ['a', 'b']:
                variant_key = f'model_{variant}'
                predictions = results[variant_key]['predictions']
                actuals = results[variant_key]['actual']
                
                if len(predictions) == 0:
                    continue
                
                # Calculate basic metrics
                variant_metrics = self._calculate_variant_metrics(predictions, actuals)
                metrics[variant_key] = variant_metrics
            
            # Calculate statistical significance
            significance_test = self._calculate_statistical_significance(experiment_id)
            
            # Determine winner
            winner = self._determine_winner(metrics, significance_test)
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'metrics': metrics,
                'statistical_significance': significance_test,
                'winner': winner,
                'sample_sizes': {
                    'model_a': len(results['model_a']['predictions']),
                    'model_b': len(results['model_b']['predictions'])
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating experiment metrics: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_trait_prediction_ab_test(self, experiment_name: str, 
                                   model_a_config: Dict[str, Any], 
                                   model_b_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run A/B test for trait prediction models.
        
        Args:
            experiment_name: Name of the experiment
            model_a_config: Configuration for model A
            model_b_config: Configuration for model B
            
        Returns:
            Dict: A/B test results
        """
        try:
            # Create experiment
            experiment_result = self.create_experiment(
                experiment_name=experiment_name,
                model_a=f"trait_prediction_{model_a_config.get('algorithm', 'random_forest')}",
                model_b=f"trait_prediction_{model_b_config.get('algorithm', 'linear_regression')}",
                experiment_type='trait_prediction'
            )
            
            if not experiment_result['success']:
                return experiment_result
            
            experiment_id = experiment_result['experiment_id']
            
            # Get test data
            test_sessions = BehavioralSession.objects.filter(
                is_completed=True
            ).order_by('?')[:1000]  # Random sample
            
            results = {
                'model_a': {'predictions': [], 'actual': [], 'metrics': {}},
                'model_b': {'predictions': [], 'actual': [], 'metrics': {}}
            }
            
            for session in test_sessions:
                # Assign variant
                variant = self.assign_variant(str(session.user.id), experiment_id)
                
                # Get session data
                session_data = {
                    'total_duration': session.total_duration,
                    'total_games_played': session.total_games_played,
                    'is_completed': session.is_completed
                }
                
                # Get actual traits if available
                actual_traits = None
                try:
                    trait_profile = TraitProfile.objects.get(session=session)
                    actual_traits = {
                        'risk_tolerance': trait_profile.risk_tolerance,
                        'consistency': trait_profile.consistency,
                        'learning_ability': trait_profile.learning_ability
                    }
                except TraitProfile.DoesNotExist:
                    pass
                
                # Make prediction with appropriate model
                if variant == 'A':
                    prediction = self.ml_engine.predict_traits(session_data)
                else:
                    # Use different model configuration for B
                    prediction = self._predict_with_alternative_model(session_data, model_b_config)
                
                # Record results
                self.record_prediction(experiment_id, variant, prediction, actual_traits)
                
                # Store in results
                results[f'model_{variant.lower()}']['predictions'].append(prediction)
                if actual_traits:
                    results[f'model_{variant.lower()}']['actual'].append(actual_traits)
            
            # Calculate metrics
            metrics = self.calculate_experiment_metrics(experiment_id)
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'results': metrics,
                'test_samples': len(test_sessions)
            }
            
        except Exception as e:
            logger.error(f"Error running trait prediction A/B test: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_variant_metrics(self, predictions: List[Dict[str, Any]], 
                                 actuals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate metrics for a variant."""
        try:
            if len(predictions) == 0:
                return {}
            
            metrics = {
                'sample_size': len(predictions),
                'success_rate': 0.0,
                'avg_confidence': 0.0,
                'prediction_accuracy': 0.0
            }
            
            # Calculate success rate
            successful_predictions = sum(1 for p in predictions if p.get('success', False))
            metrics['success_rate'] = successful_predictions / len(predictions)
            
            # Calculate average confidence
            confidences = [p.get('confidence', 0.0) for p in predictions if p.get('success', False)]
            if confidences:
                metrics['avg_confidence'] = np.mean(confidences)
            
            # Calculate prediction accuracy if actuals available
            if actuals and len(actuals) == len(predictions):
                accuracy_scores = []
                for pred, actual in zip(predictions, actuals):
                    if pred.get('success', False) and actual:
                        # Calculate accuracy for each trait
                        pred_traits = pred.get('predictions', {})
                        actual_traits = actual
                        
                        trait_accuracies = []
                        for trait in ['risk_tolerance', 'consistency', 'learning_ability']:
                            pred_val = pred_traits.get(trait, 0.5)
                            actual_val = actual_traits.get(trait, 0.5)
                            trait_accuracies.append(1 - abs(pred_val - actual_val))
                        
                        accuracy_scores.append(np.mean(trait_accuracies))
                
                if accuracy_scores:
                    metrics['prediction_accuracy'] = np.mean(accuracy_scores)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating variant metrics: {str(e)}")
            return {}
    
    def _calculate_statistical_significance(self, experiment_id: str) -> Dict[str, Any]:
        """Calculate statistical significance between variants."""
        try:
            experiment = self.experiments[experiment_id]
            results = experiment['results']
            
            # Extract accuracy scores for comparison
            a_scores = []
            b_scores = []
            
            for pred, actual in zip(results['model_a']['predictions'], results['model_a']['actual']):
                if pred.get('success', False) and actual:
                    pred_traits = pred.get('predictions', {})
                    actual_traits = actual
                    
                    trait_accuracies = []
                    for trait in ['risk_tolerance', 'consistency', 'learning_ability']:
                        pred_val = pred_traits.get(trait, 0.5)
                        actual_val = actual_traits.get(trait, 0.5)
                        trait_accuracies.append(1 - abs(pred_val - actual_val))
                    
                    a_scores.append(np.mean(trait_accuracies))
            
            for pred, actual in zip(results['model_b']['predictions'], results['model_b']['actual']):
                if pred.get('success', False) and actual:
                    pred_traits = pred.get('predictions', {})
                    actual_traits = actual
                    
                    trait_accuracies = []
                    for trait in ['risk_tolerance', 'consistency', 'learning_ability']:
                        pred_val = pred_traits.get(trait, 0.5)
                        actual_val = actual_traits.get(trait, 0.5)
                        trait_accuracies.append(1 - abs(pred_val - actual_val))
                    
                    b_scores.append(np.mean(trait_accuracies))
            
            if len(a_scores) < 10 or len(b_scores) < 10:
                return {
                    'significant': False,
                    'p_value': 1.0,
                    'reason': 'Insufficient sample size'
                }
            
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(a_scores, b_scores)
            
            confidence_level = experiment.get('confidence_level', 0.95)
            significant = p_value < (1 - confidence_level)
            
            return {
                'significant': significant,
                'p_value': p_value,
                't_statistic': t_stat,
                'confidence_level': confidence_level,
                'mean_a': np.mean(a_scores),
                'mean_b': np.mean(b_scores),
                'std_a': np.std(a_scores),
                'std_b': np.std(b_scores)
            }
            
        except Exception as e:
            logger.error(f"Error calculating statistical significance: {str(e)}")
            return {
                'significant': False,
                'p_value': 1.0,
                'error': str(e)
            }
    
    def _determine_winner(self, metrics: Dict[str, Any], 
                         significance_test: Dict[str, Any]) -> str:
        """Determine the winning variant."""
        try:
            if not significance_test.get('significant', False):
                return 'inconclusive'
            
            a_accuracy = metrics.get('model_a', {}).get('prediction_accuracy', 0.0)
            b_accuracy = metrics.get('model_b', {}).get('prediction_accuracy', 0.0)
            
            if a_accuracy > b_accuracy:
                return 'A'
            elif b_accuracy > a_accuracy:
                return 'B'
            else:
                return 'tie'
                
        except Exception as e:
            logger.error(f"Error determining winner: {str(e)}")
            return 'inconclusive'
    
    def _predict_with_alternative_model(self, session_data: Dict[str, Any], 
                                      model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction with alternative model configuration."""
        try:
            # This would implement alternative model logic
            # For now, return a modified prediction
            base_prediction = self.ml_engine.predict_traits(session_data)
            
            if base_prediction.get('success', False):
                # Modify predictions based on alternative configuration
                predictions = base_prediction.get('predictions', {})
                algorithm = model_config.get('algorithm', 'linear_regression')
                
                # Apply algorithm-specific modifications
                if algorithm == 'linear_regression':
                    # Linear regression tends to be more conservative
                    for trait in predictions:
                        predictions[trait] = max(0.1, min(0.9, predictions[trait] * 0.9))
                elif algorithm == 'neural_network':
                    # Neural network might be more extreme
                    for trait in predictions:
                        predictions[trait] = max(0.1, min(0.9, predictions[trait] * 1.1))
                
                base_prediction['predictions'] = predictions
                base_prediction['confidence'] = base_prediction.get('confidence', 0.5) * 0.9
            
            return base_prediction
            
        except Exception as e:
            logger.error(f"Error with alternative model prediction: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_experiment_status(self, experiment_id: str) -> Dict[str, Any]:
        """Get current status of an experiment."""
        try:
            if experiment_id not in self.experiments:
                return {
                    'success': False,
                    'error': 'Experiment not found'
                }
            
            experiment = self.experiments[experiment_id]
            results = experiment['results']
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'status': experiment['status'],
                'start_time': experiment['start_time'],
                'sample_sizes': {
                    'model_a': len(results['model_a']['predictions']),
                    'model_b': len(results['model_b']['predictions'])
                },
                'config': {
                    'traffic_split': experiment['traffic_split'],
                    'confidence_level': experiment['confidence_level']
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting experiment status: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_experiments(self) -> Dict[str, Any]:
        """List all experiments."""
        try:
            experiments_list = []
            
            for experiment_id, experiment in self.experiments.items():
                experiments_list.append({
                    'experiment_id': experiment_id,
                    'experiment_name': experiment['experiment_name'],
                    'status': experiment['status'],
                    'start_time': experiment['start_time'],
                    'model_a': experiment['model_a'],
                    'model_b': experiment['model_b']
                })
            
            return {
                'success': True,
                'experiments': experiments_list,
                'total_experiments': len(experiments_list)
            }
            
        except Exception as e:
            logger.error(f"Error listing experiments: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def stop_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Stop an active experiment."""
        try:
            if experiment_id not in self.experiments:
                return {
                    'success': False,
                    'error': 'Experiment not found'
                }
            
            self.experiments[experiment_id]['status'] = 'stopped'
            self.experiments[experiment_id]['end_time'] = timezone.now().isoformat()
            
            logger.info(f"Stopped experiment: {experiment_id}")
            
            return {
                'success': True,
                'experiment_id': experiment_id,
                'status': 'stopped'
            }
            
        except Exception as e:
            logger.error(f"Error stopping experiment: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 