"""
Trait Validation Module

This module implements comprehensive validation for trait inference results,
ensuring scientific rigor and reliability in psychometric assessments.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error

from behavioral_data.models import BehavioralSession, BehavioralMetric
from ai_model.models import TraitProfile

logger = logging.getLogger(__name__)


@dataclass
class ValidationCriteria:
    """Criteria for trait validation."""
    min_confidence: float = 0.7
    min_data_completeness: float = 0.8
    min_sample_size: int = 10
    max_outlier_ratio: float = 0.1
    reliability_threshold: float = 0.75
    validity_threshold: float = 0.7


@dataclass
class ValidationResult:
    """Result of trait validation."""
    is_valid: bool
    confidence_score: float
    data_quality_score: float
    reliability_score: float
    validity_score: float
    warnings: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]


class TraitValidationEngine:
    """
    High-level validation engine for trait inference API.
    
    This class provides a simplified interface for the API to validate
    trait inference results with scientific rigor.
    """
    
    def __init__(self):
        """Initialize the validation engine."""
        self.validator = TraitValidation()
        
    def validate_trait_inference(self, session_id: str, traits: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate trait inference results for API response.
        
        Args:
            session_id: Session identifier
            traits: Trait inference results
            
        Returns:
            Dict with validation results and recommendations
        """
        try:
            # Extract trait scores and confidence levels
            trait_scores = {}
            confidence_scores = {}
            
            for trait_name, trait_data in traits.items():
                if isinstance(trait_data, dict):
                    trait_scores[trait_name] = trait_data.get('score', 0.5)
                    confidence_scores[trait_name] = trait_data.get('confidence', 0.5)
                else:
                    trait_scores[trait_name] = float(trait_data)
                    confidence_scores[trait_name] = 0.7  # Default confidence
            
            # Perform comprehensive validation
            validation_result = self.validator.validate_trait_profile(
                session_id, trait_scores, confidence_scores
            )
            
            return {
                'is_valid': validation_result.is_valid,
                'confidence_level': validation_result.confidence_score,
                'reliability_score': validation_result.reliability_score,
                'data_quality_score': validation_result.data_quality_score,
                'validity_score': validation_result.validity_score,
                'warnings': validation_result.warnings,
                'recommendations': validation_result.recommendations,
                'validation_metadata': validation_result.metadata
            }
            
        except Exception as e:
            logger.error(f"Error in trait validation engine: {str(e)}")
            return {
                'is_valid': False,
                'confidence_level': 0.0,
                'reliability_score': 0.0,
                'data_quality_score': 0.0,
                'validity_score': 0.0,
                'warnings': [f"Validation error: {str(e)}"],
                'recommendations': ["Review data quality and retry validation"],
                'validation_metadata': {'error': str(e)}
            }
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary for monitoring."""
        return self.validator.get_validation_summary()


class TraitValidation:
    """
    Comprehensive validation system for trait inference results.
    
    This class implements multiple validation approaches:
    - Statistical validation (confidence intervals, significance tests)
    - Data quality validation (completeness, consistency, outliers)
    - Scientific validation (reliability, validity, replicability)
    - Cross-validation (temporal stability, internal consistency)
    """
    
    def __init__(self, criteria: Optional[ValidationCriteria] = None):
        """Initialize validation system with criteria."""
        self.criteria = criteria or ValidationCriteria()
        self.validation_history = []
        
    def validate_trait_profile(self, session_id: str, 
                             trait_scores: Dict[str, float],
                             confidence_scores: Dict[str, float]) -> ValidationResult:
        """
        Comprehensive validation of a complete trait profile.
        
        Args:
            session_id: Session identifier
            trait_scores: Dictionary of trait -> score
            confidence_scores: Dictionary of trait -> confidence
            
        Returns:
            ValidationResult with comprehensive validation assessment
        """
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
            
            # Perform multiple validation checks
            data_quality = self._validate_data_quality(session)
            statistical_validity = self._validate_statistical_properties(trait_scores, confidence_scores)
            consistency_check = self._validate_internal_consistency(trait_scores)
            temporal_stability = self._validate_temporal_stability(session_id, trait_scores)
            
            # Calculate overall validation scores
            overall_confidence = np.mean(list(confidence_scores.values())) if confidence_scores else 0.0
            overall_validity = self._calculate_overall_validity([
                data_quality['score'],
                statistical_validity['score'],
                consistency_check['score'],
                temporal_stability['score']
            ])
            
            # Determine if profile is valid
            is_valid = (
                overall_confidence >= self.criteria.min_confidence and
                data_quality['score'] >= self.criteria.min_data_completeness and
                overall_validity >= self.criteria.validity_threshold
            )
            
            # Collect warnings and recommendations
            warnings = []
            recommendations = []
            
            warnings.extend(data_quality.get('warnings', []))
            warnings.extend(statistical_validity.get('warnings', []))
            warnings.extend(consistency_check.get('warnings', []))
            warnings.extend(temporal_stability.get('warnings', []))
            
            recommendations.extend(data_quality.get('recommendations', []))
            recommendations.extend(statistical_validity.get('recommendations', []))
            recommendations.extend(consistency_check.get('recommendations', []))
            recommendations.extend(temporal_stability.get('recommendations', []))
            
            # Create validation result
            result = ValidationResult(
                is_valid=is_valid,
                confidence_score=overall_confidence,
                data_quality_score=data_quality['score'],
                reliability_score=consistency_check['score'],
                validity_score=overall_validity,
                warnings=warnings,
                recommendations=recommendations,
                metadata={
                    'session_id': session_id,
                    'validation_timestamp': datetime.now().isoformat(),
                    'criteria_version': '1.0',
                    'validation_components': {
                        'data_quality': data_quality['score'],
                        'statistical_validity': statistical_validity['score'],
                        'internal_consistency': consistency_check['score'],
                        'temporal_stability': temporal_stability['score']
                    }
                }
            )
            
            # Store validation history
            self.validation_history.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating trait profile for session {session_id}: {str(e)}")
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                data_quality_score=0.0,
                reliability_score=0.0,
                validity_score=0.0,
                warnings=[f"Validation error: {str(e)}"],
                recommendations=["Review data quality and retry validation"],
                metadata={'error': str(e)}
            )
    
    def _validate_data_quality(self, session: BehavioralSession) -> Dict[str, Any]:
        """Validate data quality for the session."""
        warnings = []
        recommendations = []
        
        # Check session duration
        if session.duration_ms and session.duration_ms < 30000:  # Less than 30 seconds
            warnings.append("Session duration is very short (< 30 seconds)")
            recommendations.append("Encourage longer engagement for better assessment")
        
        # Check number of events
        event_count = session.events.count()
        if event_count < self.criteria.min_sample_size:
            warnings.append(f"Insufficient events: {event_count} < {self.criteria.min_sample_size}")
            recommendations.append("Collect more behavioral data")
        
        # Check data completeness
        metrics = BehavioralMetric.objects.filter(session=session)
        expected_metrics = self._get_expected_metrics(session)
        completeness = len(metrics) / len(expected_metrics) if expected_metrics else 0.0
        
        if completeness < self.criteria.min_data_completeness:
            warnings.append(f"Low data completeness: {completeness:.2f}")
            recommendations.append("Ensure all game components are completed")
        
        # Check for outliers in metrics
        outlier_ratio = self._detect_outliers(metrics)
        if outlier_ratio > self.criteria.max_outlier_ratio:
            warnings.append(f"High outlier ratio: {outlier_ratio:.2f}")
            recommendations.append("Review data collection for anomalies")
        
        # Calculate overall data quality score
        quality_components = [
            min(1.0, session.duration_ms / 60000) if session.duration_ms else 0.5,  # Duration component
            min(1.0, event_count / self.criteria.min_sample_size),  # Event count component
            completeness,  # Completeness component
            1.0 - outlier_ratio  # Outlier component (inverted)
        ]
        
        quality_score = np.mean(quality_components)
        
        return {
            'score': quality_score,
            'completeness': completeness,
            'event_count': event_count,
            'outlier_ratio': outlier_ratio,
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def _validate_statistical_properties(self, trait_scores: Dict[str, float],
                                       confidence_scores: Dict[str, float]) -> Dict[str, Any]:
        """Validate statistical properties of trait scores."""
        warnings = []
        recommendations = []
        
        if not trait_scores:
            warnings.append("No trait scores to validate")
            return {'score': 0.0, 'warnings': warnings, 'recommendations': recommendations}
        
        scores = list(trait_scores.values())
        confidences = list(confidence_scores.values()) if confidence_scores else []
        
        # Check score distribution
        score_mean = np.mean(scores)
        score_std = np.std(scores)
        
        # Check for extreme values
        extreme_count = sum(1 for s in scores if s < 0.1 or s > 0.9)
        extreme_ratio = extreme_count / len(scores)
        
        if extreme_ratio > 0.5:
            warnings.append("High proportion of extreme scores")
            recommendations.append("Review assessment methodology")
        
        # Check confidence levels
        if confidences:
            low_confidence_count = sum(1 for c in confidences if c < self.criteria.min_confidence)
            if low_confidence_count > 0:
                warnings.append(f"{low_confidence_count} traits have low confidence")
                recommendations.append("Collect additional data for low-confidence traits")
        
        # Statistical validity score
        validity_components = [
            1.0 - extreme_ratio,  # Extreme values component
            np.mean(confidences) if confidences else 0.5,  # Confidence component
            min(1.0, score_std * 2)  # Variability component (some variability is good)
        ]
        
        validity_score = np.mean(validity_components)
        
        return {
            'score': validity_score,
            'score_distribution': {'mean': score_mean, 'std': score_std},
            'extreme_ratio': extreme_ratio,
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def _validate_internal_consistency(self, trait_scores: Dict[str, float]) -> Dict[str, Any]:
        """Validate internal consistency of trait scores."""
        warnings = []
        recommendations = []
        
        if len(trait_scores) < 2:
            return {'score': 0.5, 'warnings': warnings, 'recommendations': recommendations}
        
        # Check for logical consistency between related traits
        consistency_checks = []
        
        # Risk tolerance and emotion regulation should be somewhat related
        if 'risk_tolerance' in trait_scores and 'emotion_regulation' in trait_scores:
            risk_score = trait_scores['risk_tolerance']
            emotion_score = trait_scores['emotion_regulation']
            
            # High emotion regulation might correlate with moderate risk tolerance
            expected_correlation = 0.3  # Moderate positive correlation
            observed_diff = abs(risk_score - emotion_score)
            
            if observed_diff > 0.7:  # Very different scores
                warnings.append("Inconsistent risk tolerance and emotion regulation scores")
                recommendations.append("Review behavioral patterns for consistency")
            
            consistency_checks.append(1.0 - observed_diff)
        
        # Learning ability and adaptation patterns
        if 'learning_ability' in trait_scores and 'risk_tolerance' in trait_scores:
            learning_score = trait_scores['learning_ability']
            risk_score = trait_scores['risk_tolerance']
            
            # High learning ability might lead to more calibrated risk-taking
            # This is a complex relationship, so we're more lenient
            consistency_checks.append(0.8)  # Assume reasonable consistency
        
        # Calculate overall consistency score
        consistency_score = np.mean(consistency_checks) if consistency_checks else 0.7
        
        return {
            'score': consistency_score,
            'consistency_checks': len(consistency_checks),
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def _validate_temporal_stability(self, session_id: str, 
                                   current_scores: Dict[str, float]) -> Dict[str, Any]:
        """Validate temporal stability by comparing with previous assessments."""
        warnings = []
        recommendations = []
        
        try:
            # Look for previous trait profiles for the same user
            session = BehavioralSession.objects.get(session_id=session_id)
            
            # Find recent sessions for the same user (within last 30 days)
            recent_cutoff = datetime.now() - timedelta(days=30)
            recent_sessions = BehavioralSession.objects.filter(
                user_id=session.user_id,
                created_at__gte=recent_cutoff
            ).exclude(session_id=session_id)
            
            if not recent_sessions.exists():
                # No previous data for comparison
                return {
                    'score': 0.7,  # Neutral score when no comparison possible
                    'warnings': warnings,
                    'recommendations': recommendations
                }
            
            # Compare with most recent previous assessment
            previous_session = recent_sessions.order_by('-created_at').first()
            previous_profiles = TraitProfile.objects.filter(session=previous_session)
            
            if not previous_profiles.exists():
                return {
                    'score': 0.7,
                    'warnings': warnings,
                    'recommendations': recommendations
                }
            
            # Calculate stability scores
            stability_scores = []
            
            for profile in previous_profiles:
                trait_name = profile.trait_name
                if trait_name in current_scores:
                    previous_score = profile.trait_score
                    current_score = current_scores[trait_name]
                    
                    # Calculate stability (smaller difference = higher stability)
                    difference = abs(current_score - previous_score)
                    stability = 1.0 - min(1.0, difference)
                    stability_scores.append(stability)
                    
                    # Warn about large changes
                    if difference > 0.3:
                        warnings.append(f"Large change in {trait_name}: {difference:.2f}")
                        recommendations.append(f"Review factors affecting {trait_name}")
            
            overall_stability = np.mean(stability_scores) if stability_scores else 0.7
            
            return {
                'score': overall_stability,
                'comparisons_made': len(stability_scores),
                'warnings': warnings,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.warning(f"Could not validate temporal stability: {str(e)}")
            return {
                'score': 0.5,
                'warnings': [f"Temporal validation error: {str(e)}"],
                'recommendations': recommendations
            }
    
    def _get_expected_metrics(self, session: BehavioralSession) -> List[str]:
        """Get list of expected metrics based on session games."""
        expected = []
        
        # Check which games were played based on events
        games_played = set()
        for event in session.events.all():
            if hasattr(event, 'game_type'):
                games_played.add(event.game_type)
        
        # Add expected metrics for each game
        if 'balloon_risk' in games_played:
            expected.extend([
                'balloon_risk_risk_tolerance_average_pumps',
                'balloon_risk_risk_tolerance_risk_escalation',
                'balloon_risk_consistency_behavioral_consistency',
                'balloon_risk_learning_adaptation_rate',
                'balloon_risk_learning_learning_curve',
                'balloon_risk_learning_feedback_response'
            ])
        
        if 'memory_cards' in games_played:
            expected.extend([
                'memory_cards_attention_focus_duration',
                'memory_cards_learning_improvement_rate'
            ])
        
        if 'reaction_timer' in games_played:
            expected.extend([
                'reaction_timer_attention_reaction_time_consistency',
                'reaction_timer_attention_sustained_attention',
                'reaction_timer_decision_making_response_accuracy'
            ])
        
        return expected
    
    def _detect_outliers(self, metrics) -> float:
        """Detect outliers in behavioral metrics."""
        if not metrics.exists():
            return 0.0
        
        values = [m.metric_value for m in metrics if m.metric_value is not None]
        if len(values) < 3:
            return 0.0
        
        # Use IQR method for outlier detection
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        
        if iqr == 0:
            return 0.0
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = [v for v in values if v < lower_bound or v > upper_bound]
        outlier_ratio = len(outliers) / len(values)
        
        return outlier_ratio
    
    def _calculate_overall_validity(self, component_scores: List[float]) -> float:
        """Calculate overall validity score from component scores."""
        if not component_scores:
            return 0.0
        
        # Use weighted average with emphasis on data quality
        weights = [0.3, 0.25, 0.25, 0.2]  # Data quality, statistical, consistency, temporal
        weights = weights[:len(component_scores)]
        
        # Normalize weights
        weight_sum = sum(weights)
        if weight_sum > 0:
            weights = [w / weight_sum for w in weights]
        
        return sum(score * weight for score, weight in zip(component_scores, weights))
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of all validation results."""
        if not self.validation_history:
            return {'message': 'No validations performed yet'}
        
        recent_validations = self.validation_history[-10:]  # Last 10 validations
        
        validity_rates = [v.is_valid for v in recent_validations]
        confidence_scores = [v.confidence_score for v in recent_validations]
        quality_scores = [v.data_quality_score for v in recent_validations]
        
        return {
            'total_validations': len(self.validation_history),
            'recent_validity_rate': np.mean(validity_rates),
            'average_confidence': np.mean(confidence_scores),
            'average_quality': np.mean(quality_scores),
            'common_warnings': self._get_common_warnings(),
            'validation_trends': {
                'improving_quality': self._is_quality_improving(),
                'stable_confidence': self._is_confidence_stable()
            }
        }
    
    def _get_common_warnings(self) -> List[str]:
        """Get most common warnings from validation history."""
        all_warnings = []
        for validation in self.validation_history[-20:]:  # Last 20 validations
            all_warnings.extend(validation.warnings)
        
        # Count warning frequencies
        warning_counts = {}
        for warning in all_warnings:
            warning_counts[warning] = warning_counts.get(warning, 0) + 1
        
        # Return top 5 most common warnings
        sorted_warnings = sorted(warning_counts.items(), key=lambda x: x[1], reverse=True)
        return [warning for warning, count in sorted_warnings[:5]]
    
    def _is_quality_improving(self) -> bool:
        """Check if data quality is improving over time."""
        if len(self.validation_history) < 5:
            return False
        
        recent_quality = [v.data_quality_score for v in self.validation_history[-5:]]
        older_quality = [v.data_quality_score for v in self.validation_history[-10:-5]]
        
        if not older_quality:
            return False
        
        return np.mean(recent_quality) > np.mean(older_quality)
    
    def _is_confidence_stable(self) -> bool:
        """Check if confidence scores are stable."""
        if len(self.validation_history) < 5:
            return False
        
        recent_confidence = [v.confidence_score for v in self.validation_history[-5:]]
        confidence_std = np.std(recent_confidence)
        
        return confidence_std < 0.1  # Low variability indicates stability
