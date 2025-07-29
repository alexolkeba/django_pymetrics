"""
TraitInferencer Agent for Django Pymetrics

This agent maps behavioral metrics to psychometric traits using scientifically
validated inference logic. It implements multi-dimensional trait assessment
for talent analytics and candidate matching.
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from agents.base_agent import TraitInferenceAgent
from behavioral_data.models import BehavioralSession, BehavioralMetric
from ai_model.models import TraitProfile, SuccessModel, TraitAssessment, AssessmentValidation

logger = logging.getLogger(__name__)


class TraitInferencer(TraitInferenceAgent):
    def infer_session_traits(self, session_id: str) -> Dict[str, Any]:
        """Alias for process for Celery task compatibility."""
        return self.process({'session_id': session_id})
    """
    Agent for inferring psychometric traits from behavioral metrics.
    
    This agent implements scientific trait inference for:
    - Risk tolerance and decision-making preferences
    - Cognitive abilities and processing speed
    - Emotional regulation and stress management
    - Learning patterns and adaptability
    - Social and interpersonal traits
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the TraitInferencer agent."""
        super().__init__('trait_inferencer', config)
        
        # Trait inference settings
        self.inference_settings = {
            'min_confidence_threshold': 0.7,
            'trait_normalization_range': (-1.0, 1.0),
            'assessment_version': '1.0',
            'data_schema_version': '1.0',
        }
        
        # Trait mapping weights and thresholds
        self.trait_mappings = {
            'risk_tolerance': {
                'balloon_risk_risk_tolerance_avg_pumps_per_balloon': 0.4,
                'balloon_risk_risk_tolerance_risk_escalation_rate': 0.3,
                'balloon_risk_risk_tolerance_pop_rate': 0.3,
            },
            'consistency': {
                'balloon_risk_consistency_behavioral_consistency_score': 0.6,
                'balloon_risk_consistency_pump_interval_cv': 0.4,
            },
            'learning_ability': {
                'balloon_risk_learning_patterns_adaptation_rate': 0.5,
                'balloon_risk_learning_patterns_learning_curve_slope': 0.3,
                'balloon_risk_learning_patterns_feedback_response': 0.2,
            },
            'decision_speed': {
                'balloon_risk_decision_speed_avg_decision_time': 0.6,
                'balloon_risk_decision_speed_rapid_decision_rate': 0.4,
            },
            'emotional_regulation': {
                'balloon_risk_emotional_regulation_stress_response': 0.5,
                'balloon_risk_emotional_regulation_recovery_time': 0.5,
            }
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process session metrics and infer psychometric traits.
        
        Args:
            data: Session data containing session_id and optional parameters
            
        Returns:
            Dict: Inferred traits and confidence scores
        """
        session_id = data.get('session_id')
        if not session_id:
            raise ValueError("session_id is required")
        
        try:
            # Get session and metrics
            session = BehavioralSession.objects.get(session_id=session_id)
            metrics = self._get_session_metrics(session)
            
            if not metrics:
                return {
                    'processed': False,
                    'error': 'No metrics available for trait inference',
                    'session_id': session_id
                }
            
            # Infer traits
            traits = self._infer_traits(metrics, session)
            
            # Create trait profile
            trait_profile = self._create_trait_profile(traits, session)
            
            # Validate assessment (only if trait_profile was created)
            validation_result = self._validate_assessment(trait_profile, session) if trait_profile else {
                'validation_score': 0.0,
                'validation_issues': ['Trait profile creation failed due to model relationship mismatch'],
                'validation_status': 'failed'
            }
            
            return {
                'processed': True,
                'session_id': session_id,
                'trait_profile': trait_profile,
                'traits': traits,
                'validation': validation_result,
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
    
    def _get_session_metrics(self, session: BehavioralSession) -> Dict[str, float]:
        """Get all metrics for a session."""
        metrics = BehavioralMetric.objects.filter(session=session)
        
        metric_dict = {}
        for metric in metrics:
            metric_dict[metric.metric_name] = metric.metric_value
        
        return metric_dict
    
    def _infer_traits(self, metrics: Dict[str, float], session: BehavioralSession) -> Dict[str, Any]:
        """Infer psychometric traits from behavioral metrics."""
        traits = {
            'risk_tolerance': self._infer_risk_tolerance(metrics),
            'consistency': self._infer_consistency(metrics),
            'learning_ability': self._infer_learning_ability(metrics),
            'decision_speed': self._infer_decision_speed(metrics),
            'emotional_regulation': self._infer_emotional_regulation(metrics),
            'cognitive_processing': self._infer_cognitive_processing(metrics),
            'social_perception': self._infer_social_perception(metrics),
            'persistence': self._infer_persistence(metrics),
            'impulsivity': self._infer_impulsivity(metrics),
            'stress_management': self._infer_stress_management(metrics)
        }
        
        return traits
    
    def _infer_risk_tolerance(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer risk tolerance trait."""
        risk_score = 0.0
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate risk tolerance from balloon risk metrics
        avg_pumps = metrics.get('balloon_risk_risk_tolerance_avg_pumps_per_balloon', 0)
        escalation_rate = metrics.get('balloon_risk_risk_tolerance_risk_escalation_rate', 0)
        pop_rate = metrics.get('balloon_risk_risk_tolerance_pop_rate', 0)
        
        # Normalize and weight the metrics
        if avg_pumps > 0:
            # Higher pumps = higher risk tolerance
            normalized_pumps = min(avg_pumps / 10.0, 1.0)  # Normalize to 0-1
            risk_score += normalized_pumps * 0.4
            contributing_metrics.append(('avg_pumps_per_balloon', normalized_pumps))
        
        if escalation_rate != 0:
            # Positive escalation = higher risk tolerance
            normalized_escalation = max(-1.0, min(1.0, escalation_rate))
            risk_score += (normalized_escalation + 1) / 2 * 0.3  # Convert to 0-1
            contributing_metrics.append(('risk_escalation_rate', normalized_escalation))
        
        if pop_rate > 0:
            # Higher pop rate = higher risk tolerance
            risk_score += pop_rate * 0.3
            contributing_metrics.append(('pop_rate', pop_rate))
        
        # Calculate confidence based on available metrics
        confidence = min(len(contributing_metrics) / 3.0, 1.0)
        
        return {
            'score': risk_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_risk_tolerance(risk_score)
        }
    
    def _infer_consistency(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer consistency trait."""
        consistency_score = 0.0
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate consistency from behavioral patterns
        behavioral_consistency = metrics.get('balloon_risk_consistency_behavioral_consistency_score', 0)
        interval_cv = metrics.get('balloon_risk_consistency_pump_interval_cv', 0)
        
        if behavioral_consistency > 0:
            consistency_score += behavioral_consistency * 0.6
            contributing_metrics.append(('behavioral_consistency', behavioral_consistency))
        
        if interval_cv > 0:
            # Lower CV = higher consistency
            normalized_cv = max(0, 1 - min(interval_cv, 1.0))
            consistency_score += normalized_cv * 0.4
            contributing_metrics.append(('interval_consistency', normalized_cv))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': consistency_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_consistency(consistency_score)
        }
    
    def _infer_learning_ability(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer learning ability trait."""
        learning_score = 0.0
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate learning ability from adaptation patterns
        adaptation_rate = metrics.get('balloon_risk_learning_patterns_adaptation_rate', 0)
        learning_curve = metrics.get('balloon_risk_learning_patterns_learning_curve_slope', 0)
        feedback_response = metrics.get('balloon_risk_learning_patterns_feedback_response', 0)
        
        if adaptation_rate != 0:
            # Positive adaptation = better learning
            normalized_adaptation = max(-1.0, min(1.0, adaptation_rate))
            learning_score += (normalized_adaptation + 1) / 2 * 0.5
            contributing_metrics.append(('adaptation_rate', normalized_adaptation))
        
        if learning_curve != 0:
            # Positive slope = better learning
            normalized_curve = max(-1.0, min(1.0, learning_curve))
            learning_score += (normalized_curve + 1) / 2 * 0.3
            contributing_metrics.append(('learning_curve', normalized_curve))
        
        if feedback_response != 0:
            # Positive response to feedback = better learning
            normalized_response = max(-1.0, min(1.0, feedback_response))
            learning_score += (normalized_response + 1) / 2 * 0.2
            contributing_metrics.append(('feedback_response', normalized_response))
        
        confidence = min(len(contributing_metrics) / 3.0, 1.0)
        
        return {
            'score': learning_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_learning_ability(learning_score)
        }
    
    def _infer_decision_speed(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer decision speed trait."""
        speed_score = 0.0
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate decision speed from response times
        avg_decision_time = metrics.get('balloon_risk_decision_speed_avg_decision_time', 0)
        rapid_decision_rate = metrics.get('balloon_risk_decision_speed_rapid_decision_rate', 0)
        
        if avg_decision_time > 0:
            # Faster decisions = higher speed score
            normalized_time = max(0, 1 - min(avg_decision_time / 5000.0, 1.0))  # 5 seconds max
            speed_score += normalized_time * 0.6
            contributing_metrics.append(('decision_time', normalized_time))
        
        if rapid_decision_rate > 0:
            speed_score += rapid_decision_rate * 0.4
            contributing_metrics.append(('rapid_decisions', rapid_decision_rate))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': speed_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_decision_speed(speed_score)
        }
    
    def _infer_emotional_regulation(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer emotional regulation trait."""
        regulation_score = 0.5  # Default neutral score
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate emotional regulation from stress responses
        stress_response = metrics.get('balloon_risk_emotional_regulation_stress_response', 0)
        recovery_time = metrics.get('balloon_risk_emotional_regulation_recovery_time', 0)
        
        if stress_response != 0:
            # Lower stress response = better regulation
            normalized_stress = max(0, 1 - abs(stress_response))
            regulation_score += normalized_stress * 0.5
            contributing_metrics.append(('stress_response', normalized_stress))
        
        if recovery_time > 0:
            # Faster recovery = better regulation
            normalized_recovery = max(0, 1 - min(recovery_time / 60000.0, 1.0))  # 1 minute max
            regulation_score += normalized_recovery * 0.5
            contributing_metrics.append(('recovery_time', normalized_recovery))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': regulation_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_emotional_regulation(regulation_score)
        }
    
    def _infer_cognitive_processing(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer cognitive processing trait (placeholder)."""
        return {
            'score': 0.5,
            'confidence': 0.0,
            'contributing_metrics': [],
            'interpretation': 'Insufficient data for cognitive processing assessment'
        }
    
    def _infer_social_perception(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer social perception trait (placeholder)."""
        return {
            'score': 0.5,
            'confidence': 0.0,
            'contributing_metrics': [],
            'interpretation': 'Insufficient data for social perception assessment'
        }
    
    def _infer_persistence(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer persistence trait."""
        persistence_score = 0.5
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate persistence from session completion and engagement
        session_duration = metrics.get('session_session_duration_ms', 0)
        completion_rate = metrics.get('session_completion_rate', 0)
        
        if session_duration > 0:
            # Longer sessions = higher persistence
            normalized_duration = min(session_duration / 300000.0, 1.0)  # 5 minutes max
            persistence_score += normalized_duration * 0.5
            contributing_metrics.append(('session_duration', normalized_duration))
        
        if completion_rate > 0:
            persistence_score += completion_rate * 0.5
            contributing_metrics.append(('completion_rate', completion_rate))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': persistence_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_persistence(persistence_score)
        }
    
    def _infer_impulsivity(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer impulsivity trait."""
        impulsivity_score = 0.5
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate impulsivity from rapid decisions and risk-taking
        rapid_decision_rate = metrics.get('balloon_risk_decision_speed_rapid_decision_rate', 0)
        pop_rate = metrics.get('balloon_risk_risk_tolerance_pop_rate', 0)
        
        if rapid_decision_rate > 0:
            # Higher rapid decision rate = higher impulsivity
            impulsivity_score += rapid_decision_rate * 0.5
            contributing_metrics.append(('rapid_decisions', rapid_decision_rate))
        
        if pop_rate > 0:
            # Higher pop rate = higher impulsivity
            impulsivity_score += pop_rate * 0.5
            contributing_metrics.append(('pop_rate', pop_rate))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': impulsivity_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_impulsivity(impulsivity_score)
        }
    
    def _infer_stress_management(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Infer stress management trait."""
        stress_score = 0.5
        confidence = 0.0
        contributing_metrics = []
        
        # Calculate stress management from emotional regulation
        stress_response = metrics.get('balloon_risk_emotional_regulation_stress_response', 0)
        recovery_time = metrics.get('balloon_risk_emotional_regulation_recovery_time', 0)
        
        if stress_response != 0:
            # Lower stress response = better stress management
            normalized_stress = max(0, 1 - abs(stress_response))
            stress_score += normalized_stress * 0.5
            contributing_metrics.append(('stress_response', normalized_stress))
        
        if recovery_time > 0:
            # Faster recovery = better stress management
            normalized_recovery = max(0, 1 - min(recovery_time / 60000.0, 1.0))
            stress_score += normalized_recovery * 0.5
            contributing_metrics.append(('recovery_time', normalized_recovery))
        
        confidence = min(len(contributing_metrics) / 2.0, 1.0)
        
        return {
            'score': stress_score,
            'confidence': confidence,
            'contributing_metrics': contributing_metrics,
            'interpretation': self._interpret_stress_management(stress_score)
        }
    
    def _create_trait_profile(self, traits: Dict[str, Any], session: BehavioralSession) -> Optional[TraitProfile]:
        """Create a trait profile from inferred traits."""
        try:
            with transaction.atomic():
                # Calculate average trait score
                trait_scores = [trait['score'] for trait in traits.values()]
                avg_trait_score = np.mean(trait_scores) if trait_scores else 0.5
                
                # Note: TraitProfile is linked to GameSession, not BehavioralSession
                # For now, we'll return None and let the calling code handle it
                # In a real implementation, you would create a GameSession or modify the model relationship
                
                logger.warning(f"Cannot create TraitProfile for BehavioralSession {session.session_id} - model relationship mismatch")
                return None
                
        except Exception as e:
            logger.error(f"Error creating trait profile: {e}")
            return None
    
    def _validate_assessment(self, trait_profile: Optional[TraitProfile], session: BehavioralSession) -> Dict[str, Any]:
        """Validate the trait assessment."""
        if not trait_profile:
            return {
                'validation_score': 0.0,
                'validation_issues': ['No trait profile available for validation'],
                'validation_status': 'failed'
            }
        
        validation_score = 0.0
        validation_issues = []
        
        # Check data quality
        data_quality = session.metrics.filter(metric_name__contains='data_quality').first()
        if data_quality and data_quality.metric_value < 0.8:
            validation_issues.append(f"Low data quality: {data_quality.metric_value:.2f}")
        
        # Check confidence levels
        if trait_profile.confidence_level < self.inference_settings['min_confidence_threshold'] * 100:
            validation_issues.append(f"Low confidence: {trait_profile.confidence_level:.2f}")
        
        # Check session duration
        session_duration = session.metrics.filter(metric_name__contains='session_duration').first()
        if session_duration and session_duration.metric_value < 30000:  # 30 seconds
            validation_issues.append("Short session duration")
        
        # Calculate validation score
        validation_score = max(0, 1 - len(validation_issues) * 0.2)
        
        # Update trait profile validation status
        trait_profile.validation_status = 'valid' if validation_score > 0.8 else 'invalid'
        trait_profile.save()
        
        return {
            'validation_score': validation_score,
            'validation_issues': validation_issues,
            'validation_status': trait_profile.validation_status
        }
    
    # Interpretation methods
    def _interpret_risk_tolerance(self, score: float) -> str:
        if score < 0.3:
            return "Conservative risk-taker"
        elif score < 0.7:
            return "Moderate risk-taker"
        else:
            return "High risk-taker"
    
    def _interpret_consistency(self, score: float) -> str:
        if score < 0.3:
            return "Variable behavior patterns"
        elif score < 0.7:
            return "Moderately consistent"
        else:
            return "Highly consistent behavior"
    
    def _interpret_learning_ability(self, score: float) -> str:
        if score < 0.3:
            return "Slow to adapt"
        elif score < 0.7:
            return "Moderate learning ability"
        else:
            return "Quick learner"
    
    def _interpret_decision_speed(self, score: float) -> str:
        if score < 0.3:
            return "Deliberate decision-maker"
        elif score < 0.7:
            return "Moderate decision speed"
        else:
            return "Rapid decision-maker"
    
    def _interpret_emotional_regulation(self, score: float) -> str:
        if score < 0.3:
            return "Emotionally reactive"
        elif score < 0.7:
            return "Moderate emotional control"
        else:
            return "Emotionally stable"
    
    def _interpret_persistence(self, score: float) -> str:
        if score < 0.3:
            return "Low persistence"
        elif score < 0.7:
            return "Moderate persistence"
        else:
            return "Highly persistent"
    
    def _interpret_impulsivity(self, score: float) -> str:
        if score < 0.3:
            return "Reflective and cautious"
        elif score < 0.7:
            return "Moderate impulsivity"
        else:
            return "Highly impulsive"
    
    def _interpret_stress_management(self, score: float) -> str:
        if score < 0.3:
            return "Poor stress management"
        elif score < 0.7:
            return "Moderate stress management"
        else:
            return "Excellent stress management"
    
    def infer_session_traits(self, session_id: str) -> Dict[str, Any]:
        """Infer traits for a specific session."""
        return self.process({'session_id': session_id})
    
    def batch_infer_traits(self, session_ids: List[str]) -> Dict[str, Any]:
        """Infer traits for multiple sessions."""
        results = {}
        for session_id in session_ids:
            try:
                result = self.infer_session_traits(session_id)
                results[session_id] = result
            except Exception as e:
                results[session_id] = {'error': str(e)}
        
        return results 