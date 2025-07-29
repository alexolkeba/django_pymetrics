"""
Trait Mappings for Django Pymetrics

This module implements the core scientific logic for mapping behavioral metrics
to psychometric traits based on documented research and Pymetrics methodologies.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TraitDimension(Enum):
    """Psychometric trait dimensions based on scientific research."""
    RISK_TOLERANCE = "risk_tolerance"
    ATTENTION = "attention"
    EFFORT = "effort"
    FAIRNESS = "fairness"
    FOCUS = "focus"
    GENEROSITY = "generosity"
    LEARNING = "learning"
    PLANNING = "planning"
    DECISION_MAKING = "decision_making"
    EMOTION_REGULATION = "emotion_regulation"


@dataclass
class TraitMapping:
    """Configuration for mapping metrics to traits."""
    trait_dimension: TraitDimension
    source_metrics: List[str]
    weight_function: str
    normalization_method: str
    confidence_threshold: float
    scientific_basis: str


class TraitMapper:
    """
    Core trait mapping engine that converts behavioral metrics to trait scores.
    
    This class implements scientifically validated algorithms for inferring
    psychometric traits from behavioral data collected during game sessions.
    """
    
    def __init__(self):
        """Initialize the trait mapper with scientific configurations."""
        self.trait_mappings = self._initialize_trait_mappings()
        self.normalization_cache = {}
        
    def _initialize_trait_mappings(self) -> Dict[TraitDimension, TraitMapping]:
        """Initialize trait mapping configurations based on scientific research."""
        return {
            TraitDimension.RISK_TOLERANCE: TraitMapping(
                trait_dimension=TraitDimension.RISK_TOLERANCE,
                source_metrics=[
                    "balloon_risk_risk_tolerance_average_pumps",
                    "balloon_risk_risk_tolerance_risk_escalation",
                    "balloon_risk_consistency_behavioral_consistency",
                    "balloon_risk_learning_adaptation_rate"
                ],
                weight_function="weighted_average",
                normalization_method="z_score",
                confidence_threshold=0.7,
                scientific_basis="Based on Balloon Analogue Risk Task (BART) research"
            ),
            
            TraitDimension.ATTENTION: TraitMapping(
                trait_dimension=TraitDimension.ATTENTION,
                source_metrics=[
                    "reaction_timer_attention_reaction_time_consistency",
                    "reaction_timer_attention_sustained_attention",
                    "memory_cards_attention_focus_duration"
                ],
                weight_function="weighted_average",
                normalization_method="percentile",
                confidence_threshold=0.75,
                scientific_basis="Based on sustained attention and reaction time research"
            ),
            
            TraitDimension.LEARNING: TraitMapping(
                trait_dimension=TraitDimension.LEARNING,
                source_metrics=[
                    "balloon_risk_learning_learning_curve",
                    "balloon_risk_learning_adaptation_rate",
                    "balloon_risk_learning_feedback_response",
                    "memory_cards_learning_improvement_rate"
                ],
                weight_function="learning_curve_analysis",
                normalization_method="sigmoid",
                confidence_threshold=0.8,
                scientific_basis="Based on reinforcement learning and adaptation research"
            ),
            
            TraitDimension.EMOTION_REGULATION: TraitMapping(
                trait_dimension=TraitDimension.EMOTION_REGULATION,
                source_metrics=[
                    "balloon_risk_emotion_stress_response",
                    "balloon_risk_emotion_recovery_time",
                    "balloon_risk_emotion_post_loss_behavior"
                ],
                weight_function="emotion_regulation_model",
                normalization_method="robust_scaling",
                confidence_threshold=0.7,
                scientific_basis="Based on emotional regulation and stress response research"
            ),
            
            TraitDimension.DECISION_MAKING: TraitMapping(
                trait_dimension=TraitDimension.DECISION_MAKING,
                source_metrics=[
                    "balloon_risk_decision_making_decision_speed",
                    "balloon_risk_consistency_behavioral_consistency",
                    "reaction_timer_decision_making_response_accuracy"
                ],
                weight_function="decision_quality_model",
                normalization_method="min_max",
                confidence_threshold=0.75,
                scientific_basis="Based on decision-making and cognitive processing research"
            )
        }
    
    def map_session_traits(self, session_id: str) -> Dict[str, Any]:
        """
        Map all behavioral metrics for a session to trait scores.
        
        Args:
            session_id: The session to analyze
            
        Returns:
            Dict containing trait scores, confidence levels, and metadata
        """
        try:
            # Import models locally to avoid circular imports
            from behavioral_data.models import BehavioralSession
            
            session = BehavioralSession.objects.get(session_id=session_id)
            metrics = self._get_session_metrics(session)
            
            if not metrics:
                return {
                    'error': 'No metrics found for session',
                    'session_id': session_id
                }
            
            trait_scores = {}
            confidence_scores = {}
            
            for trait_dim, mapping in self.trait_mappings.items():
                score, confidence = self._calculate_trait_score(metrics, mapping)
                
                if confidence >= mapping.confidence_threshold:
                    trait_scores[trait_dim.value] = score
                    confidence_scores[trait_dim.value] = confidence
                else:
                    logger.warning(f"Low confidence for {trait_dim.value}: {confidence}")
            
            return {
                'session_id': session_id,
                'trait_scores': trait_scores,
                'confidence_scores': confidence_scores,
                'metadata': {
                    'total_metrics': len(metrics),
                    'traits_calculated': len(trait_scores),
                    'calculation_timestamp': session.updated_at.isoformat(),
                    'data_version': '1.0'
                }
            }
            
        except Exception as e:
            logger.error(f"Error mapping traits for session {session_id}: {str(e)}")
            return {
                'error': str(e),
                'session_id': session_id
            }
    
    def _get_session_metrics(self, session) -> Dict[str, float]:
        """Retrieve all calculated metrics for a session."""
        # Import models locally to avoid circular imports
        from behavioral_data.models import BehavioralMetric
        
        metrics = {}
        
        for metric in BehavioralMetric.objects.filter(session=session):
            metrics[metric.metric_name] = metric.metric_value
            
        return metrics
    
    def _calculate_trait_score(self, metrics: Dict[str, float], 
                             mapping: TraitMapping) -> Tuple[float, float]:
        """
        Calculate trait score and confidence for a specific trait dimension.
        
        Args:
            metrics: Dictionary of metric name -> value
            mapping: Trait mapping configuration
            
        Returns:
            Tuple of (trait_score, confidence_level)
        """
        # Extract relevant metrics
        relevant_metrics = {}
        for metric_name in mapping.source_metrics:
            if metric_name in metrics:
                relevant_metrics[metric_name] = metrics[metric_name]
        
        if not relevant_metrics:
            return 0.0, 0.0
        
        # Normalize metrics
        normalized_metrics = self._normalize_metrics(
            relevant_metrics, mapping.normalization_method
        )
        
        # Apply weight function
        trait_score = self._apply_weight_function(
            normalized_metrics, mapping.weight_function, mapping.trait_dimension
        )
        
        # Calculate confidence based on data completeness and consistency
        confidence = self._calculate_confidence(relevant_metrics, mapping)
        
        return trait_score, confidence
    
    def _normalize_metrics(self, metrics: Dict[str, float], 
                          method: str) -> Dict[str, float]:
        """Normalize metrics using specified method."""
        values = np.array(list(metrics.values()))
        
        if method == "z_score":
            if np.std(values) > 0:
                normalized = (values - np.mean(values)) / np.std(values)
            else:
                normalized = values
                
        elif method == "min_max":
            min_val, max_val = np.min(values), np.max(values)
            if max_val > min_val:
                normalized = (values - min_val) / (max_val - min_val)
            else:
                normalized = values
                
        elif method == "percentile":
            normalized = np.array([
                np.percentile(values, 50) for _ in values
            ]) / 100.0
            
        elif method == "robust_scaling":
            median = np.median(values)
            mad = np.median(np.abs(values - median))
            if mad > 0:
                normalized = (values - median) / mad
            else:
                normalized = values
                
        elif method == "sigmoid":
            normalized = 1 / (1 + np.exp(-values))
            
        else:
            normalized = values  # No normalization
        
        return dict(zip(metrics.keys(), normalized))
    
    def _apply_weight_function(self, metrics: Dict[str, float], 
                              function: str, trait_dim: TraitDimension) -> float:
        """Apply weighting function to calculate final trait score."""
        values = list(metrics.values())
        
        if function == "weighted_average":
            return self._weighted_average(values, trait_dim)
            
        elif function == "learning_curve_analysis":
            return self._learning_curve_analysis(metrics)
            
        elif function == "emotion_regulation_model":
            return self._emotion_regulation_model(metrics)
            
        elif function == "decision_quality_model":
            return self._decision_quality_model(metrics)
            
        else:
            # Simple average as fallback
            return np.mean(values) if values else 0.0
    
    def _weighted_average(self, values: List[float], 
                         trait_dim: TraitDimension) -> float:
        """Calculate weighted average based on trait dimension."""
        if not values:
            return 0.0
            
        # Define weights based on scientific research
        if trait_dim == TraitDimension.RISK_TOLERANCE:
            weights = [0.4, 0.3, 0.2, 0.1]  # Emphasize average pumps and escalation
        elif trait_dim == TraitDimension.ATTENTION:
            weights = [0.5, 0.3, 0.2]  # Emphasize consistency
        else:
            weights = [1.0 / len(values)] * len(values)  # Equal weights
        
        # Ensure weights match values length
        weights = weights[:len(values)]
        if len(weights) < len(values):
            weights.extend([0.1] * (len(values) - len(weights)))
        
        # Normalize weights
        weight_sum = sum(weights)
        if weight_sum > 0:
            weights = [w / weight_sum for w in weights]
        
        return sum(v * w for v, w in zip(values, weights))
    
    def _learning_curve_analysis(self, metrics: Dict[str, float]) -> float:
        """Analyze learning patterns for learning trait."""
        learning_indicators = []
        
        for metric_name, value in metrics.items():
            if "learning_curve" in metric_name:
                learning_indicators.append(value * 0.4)  # High weight for learning curve
            elif "adaptation_rate" in metric_name:
                learning_indicators.append(value * 0.3)  # Medium weight for adaptation
            elif "feedback_response" in metric_name:
                learning_indicators.append(value * 0.2)  # Lower weight for feedback
            else:
                learning_indicators.append(value * 0.1)  # Minimal weight for others
        
        return sum(learning_indicators) if learning_indicators else 0.0
    
    def _emotion_regulation_model(self, metrics: Dict[str, float]) -> float:
        """Model emotional regulation based on stress response patterns."""
        stress_response = 0.0
        recovery_ability = 0.0
        behavioral_stability = 0.0
        
        for metric_name, value in metrics.items():
            if "stress_response" in metric_name:
                stress_response = 1.0 - min(1.0, value)  # Lower stress = better regulation
            elif "recovery_time" in metric_name:
                recovery_ability = 1.0 - min(1.0, value / 10.0)  # Faster recovery = better
            elif "post_loss_behavior" in metric_name:
                behavioral_stability = value
        
        # Combine components with weights
        emotion_score = (
            stress_response * 0.4 +
            recovery_ability * 0.4 +
            behavioral_stability * 0.2
        )
        
        return max(0.0, min(1.0, emotion_score))
    
    def _decision_quality_model(self, metrics: Dict[str, float]) -> float:
        """Model decision-making quality based on speed and consistency."""
        decision_speed = 0.0
        consistency = 0.0
        accuracy = 0.0
        
        for metric_name, value in metrics.items():
            if "decision_speed" in metric_name:
                decision_speed = min(1.0, 1.0 / (1.0 + value))  # Faster = better (up to a point)
            elif "consistency" in metric_name:
                consistency = value
            elif "accuracy" in metric_name:
                accuracy = value
        
        # Balance speed, consistency, and accuracy
        decision_score = (
            decision_speed * 0.3 +
            consistency * 0.4 +
            accuracy * 0.3
        )
        
        return max(0.0, min(1.0, decision_score))
    
    def _calculate_confidence(self, metrics: Dict[str, float], 
                            mapping: TraitMapping) -> float:
        """Calculate confidence level for trait score."""
        # Base confidence on data completeness
        completeness = len(metrics) / len(mapping.source_metrics)
        
        # Adjust for metric quality (variance indicates consistency)
        if len(metrics) > 1:
            values = list(metrics.values())
            consistency = 1.0 - min(1.0, np.std(values) / (np.mean(values) + 1e-6))
        else:
            consistency = 0.5  # Moderate confidence with single metric
        
        # Combine factors
        confidence = (completeness * 0.6 + consistency * 0.4)
        
        return max(0.0, min(1.0, confidence))
    
    def get_trait_explanation(self, trait_dimension: TraitDimension, 
                            score: float) -> Dict[str, Any]:
        """
        Provide human-readable explanation of trait score.
        
        Args:
            trait_dimension: The trait being explained
            score: The calculated trait score (0-1)
            
        Returns:
            Dict with explanation, interpretation, and recommendations
        """
        mapping = self.trait_mappings.get(trait_dimension)
        if not mapping:
            return {'error': f'Unknown trait dimension: {trait_dimension}'}
        
        # Determine score interpretation
        if score >= 0.8:
            level = "Very High"
        elif score >= 0.6:
            level = "High"
        elif score >= 0.4:
            level = "Moderate"
        elif score >= 0.2:
            level = "Low"
        else:
            level = "Very Low"
        
        explanations = {
            TraitDimension.RISK_TOLERANCE: {
                "description": "Willingness to take risks for potential rewards",
                "high_interpretation": "Comfortable with uncertainty and willing to take calculated risks",
                "low_interpretation": "Prefers certainty and avoids risky situations",
                "scientific_basis": mapping.scientific_basis
            },
            TraitDimension.LEARNING: {
                "description": "Ability to adapt behavior based on experience and feedback",
                "high_interpretation": "Quickly learns from experience and adapts strategies",
                "low_interpretation": "Slower to adapt behavior based on new information",
                "scientific_basis": mapping.scientific_basis
            },
            TraitDimension.EMOTION_REGULATION: {
                "description": "Ability to manage emotional responses under stress",
                "high_interpretation": "Maintains composure and recovers quickly from setbacks",
                "low_interpretation": "May struggle with emotional responses to stress or failure",
                "scientific_basis": mapping.scientific_basis
            }
        }
        
        trait_info = explanations.get(trait_dimension, {
            "description": f"Trait dimension: {trait_dimension.value}",
            "high_interpretation": "High scores indicate strong performance in this area",
            "low_interpretation": "Low scores suggest areas for development",
            "scientific_basis": mapping.scientific_basis if mapping else "Research-based assessment"
        })
        
        return {
            'trait_dimension': trait_dimension.value,
            'score': score,
            'level': level,
            'description': trait_info['description'],
            'interpretation': trait_info['high_interpretation'] if score >= 0.5 else trait_info['low_interpretation'],
            'scientific_basis': trait_info['scientific_basis'],
            'source_metrics': mapping.source_metrics if mapping else [],
            'confidence_threshold': mapping.confidence_threshold if mapping else 0.7
        }
