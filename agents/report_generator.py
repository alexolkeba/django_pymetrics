"""
ReportGenerator Agent for Django Pymetrics

This agent creates comprehensive reports and dashboards from behavioral data
and trait profiles. It implements scientific reporting with insights and
recommendations for talent analytics.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.db import transaction

from agents.base_agent import ReportGenerationAgent
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile, SuccessModel, TraitAssessment

logger = logging.getLogger(__name__)


class ReportGenerator(ReportGenerationAgent):
    def generate_session_report(self, session_id: str) -> Dict[str, Any]:
        """Alias for process for Celery task compatibility."""
        return self.process({'session_id': session_id})
    """
    Agent for generating comprehensive reports and dashboards.
    
    This agent creates:
    - Individual assessment reports
    - Comparative analysis reports
    - Trend analysis and insights
    - Success model matching reports
    - Executive summaries and recommendations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the ReportGenerator agent."""
        super().__init__('report_generator', config)
        
        # Report generation settings
        self.report_settings = {
            'report_version': '1.0',
            'include_charts': True,
            'include_recommendations': True,
            'confidence_threshold': 0.7,
            'max_comparison_profiles': 100,
        }
        
        # Report templates and sections
        self.report_sections = [
            'executive_summary',
            'behavioral_analysis',
            'trait_assessment',
            'comparative_analysis',
            'insights_and_recommendations',
            'methodology_and_validation'
        ]
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive report for session or user.
        
        Args:
            data: Report data containing session_id or user_id and report type
            
        Returns:
            Dict: Generated report with all sections and insights
        """
        session_id = data.get('session_id')
        user_id = data.get('user_id')
        report_type = data.get('report_type', 'individual_assessment')
        
        if not session_id and not user_id:
            raise ValueError("Either session_id or user_id is required")
        
        try:
            if session_id:
                return self._generate_session_report(session_id, report_type)
            else:
                return self._generate_user_report(user_id, report_type)
                
        except Exception as e:
            self.handle_error(e, context={'session_id': session_id, 'user_id': user_id})
            return {
                'processed': False,
                'error': str(e),
                'session_id': session_id,
                'user_id': user_id
            }
    
    def _generate_session_report(self, session_id: str, report_type: str) -> Dict[str, Any]:
        """Generate report for a specific session."""
        try:
            session = BehavioralSession.objects.get(session_id=session_id)
            # Note: TraitProfile is linked to GameSession, not BehavioralSession
            # For now, we'll create a placeholder report without trait profile
            trait_profile = None
            
            # Generate report sections
            report = {
                'report_id': f"report_{session_id}_{int(timezone.now().timestamp())}",
                'session_id': session_id,
                'user_id': session.user.id,
                'report_type': report_type,
                'generated_at': timezone.now().isoformat(),
                'report_version': self.report_settings['report_version'],
                'sections': {}
            }
            
            # Executive Summary
            report['sections']['executive_summary'] = self._generate_executive_summary(session, trait_profile)
            
            # Behavioral Analysis
            report['sections']['behavioral_analysis'] = self._generate_behavioral_analysis(session)
            
            # Trait Assessment (placeholder since no trait profile)
            report['sections']['trait_assessment'] = {
                'message': 'No trait profile available for this session',
                'available': False
            }
            
            # Comparative Analysis (placeholder)
            report['sections']['comparative_analysis'] = {
                'message': 'No trait profile available for comparison',
                'comparison_available': False
            }
            
            # Insights and Recommendations
            report['sections']['insights_and_recommendations'] = {
                'message': 'No trait profile available for insights',
                'insights': [],
                'recommendations': []
            }
            
            # Methodology and Validation
            report['sections']['methodology_and_validation'] = self._generate_methodology_section(session, trait_profile)
            
            return {
                'processed': True,
                'report': report,
                'timestamp': timezone.now().isoformat(),
                'processing_time': self.get_processing_time()
            }
            
        except BehavioralSession.DoesNotExist:
            return {
                'processed': False,
                'error': f'Session {session_id} not found',
                'session_id': session_id
            }
    
    def _generate_user_report(self, user_id: str, report_type: str) -> Dict[str, Any]:
        """Generate report for a specific user (multiple sessions)."""
        try:
            # Get user's sessions and trait profiles
            sessions = BehavioralSession.objects.filter(user_id=user_id).order_by('-session_start_time')
            trait_profiles = TraitProfile.objects.filter(user_id=user_id).order_by('-calculation_timestamp')
            
            if not trait_profiles.exists():
                return {
                    'processed': False,
                    'error': 'No trait profiles found for user',
                    'user_id': user_id
                }
            
            # Generate comprehensive user report
            report = {
                'report_id': f"user_report_{user_id}_{int(timezone.now().timestamp())}",
                'user_id': user_id,
                'report_type': report_type,
                'generated_at': timezone.now().isoformat(),
                'report_version': self.report_settings['report_version'],
                'sections': {}
            }
            
            # User Overview
            report['sections']['user_overview'] = self._generate_user_overview(sessions, trait_profiles)
            
            # Trend Analysis
            report['sections']['trend_analysis'] = self._generate_trend_analysis(trait_profiles)
            
            # Performance Summary
            report['sections']['performance_summary'] = self._generate_performance_summary(sessions, trait_profiles)
            
            # Comparative Analysis
            report['sections']['comparative_analysis'] = self._generate_user_comparative_analysis(trait_profiles)
            
            # Recommendations
            report['sections']['recommendations'] = self._generate_user_recommendations(trait_profiles)
            
            return {
                'processed': True,
                'report': report,
                'timestamp': timezone.now().isoformat(),
                'processing_time': self.get_processing_time()
            }
            
        except Exception as e:
            return {
                'processed': False,
                'error': str(e),
                'user_id': user_id
            }
    
    def _generate_executive_summary(self, session: BehavioralSession, trait_profile: TraitProfile) -> Dict[str, Any]:
        """Generate executive summary section."""
        # Calculate key metrics
        total_events = session.events.count()
        session_duration = (session.session_end_time - session.session_start_time).total_seconds() if session.session_end_time else 0
        
        if trait_profile:
            # Get top traits
            trait_scores = {
                'Risk Tolerance': trait_profile.risk_tolerance,
                'Consistency': trait_profile.consistency,
                'Learning Ability': trait_profile.learning_agility,
                'Decision Speed': trait_profile.decision_speed,
                'Emotional Regulation': trait_profile.emotional_regulation
            }
            
            top_traits = sorted(trait_scores.items(), key=lambda x: x[1] or 0, reverse=True)[:3]
            
            return {
                'session_summary': {
                    'total_events': total_events,
                    'session_duration_minutes': round(session_duration / 60, 2),
                    'completion_status': 'Completed' if session.is_completed else 'Incomplete',
                    'data_quality_score': trait_profile.confidence_level
                },
                'key_insights': [
                    f"Primary strength: {top_traits[0][0]} ({top_traits[0][1]:.2f})",
                    f"Assessment confidence: {trait_profile.confidence_level:.1%}",
                    f"Data quality: {'High' if trait_profile.confidence_level > 0.8 else 'Moderate' if trait_profile.confidence_level > 0.6 else 'Low'}"
                ],
                'recommendations': self._generate_key_recommendations(trait_profile)
            }
        else:
            return {
                'session_summary': {
                    'total_events': total_events,
                    'session_duration_minutes': round(session_duration / 60, 2),
                    'completion_status': 'Completed' if session.is_completed else 'Incomplete',
                    'data_quality_score': 0.0
                },
                'key_insights': [
                    "No trait profile available for analysis",
                    "Session data collected successfully",
                    "Trait inference pending"
                ],
                'recommendations': ["Complete trait inference to generate insights"]
            }
    
    def _generate_behavioral_analysis(self, session: BehavioralSession) -> Dict[str, Any]:
        """Generate behavioral analysis section."""
        events = session.events.all().order_by('timestamp')
        
        # Analyze event patterns
        event_types = {}
        for event in events:
            event_type = event.event_type
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Calculate engagement metrics
        engagement_score = len(events) / max(session.total_duration / 60000, 1)  # events per minute
        
        return {
            'event_analysis': {
                'total_events': len(events),
                'event_types': event_types,
                'engagement_score': engagement_score,
                'session_completion': session.is_completed
            },
            'behavioral_patterns': {
                'event_frequency': self._calculate_event_frequency(events),
                'response_times': self._calculate_response_times(events),
                'interaction_patterns': self._analyze_interaction_patterns(events)
            },
            'data_quality': {
                'valid_events': events.filter(validation_status='valid').count(),
                'invalid_events': events.filter(validation_status='invalid').count(),
                'completeness_score': len(events) / max(session.total_games_played * 10, 1)
            }
        }
    
    def _generate_trait_assessment(self, trait_profile: TraitProfile) -> Dict[str, Any]:
        """Generate trait assessment section."""
        traits = {
            'Risk Tolerance': {
                'score': trait_profile.risk_tolerance,
                'interpretation': self._interpret_trait_score(trait_profile.risk_tolerance, 'risk_tolerance'),
                'description': 'Willingness to take risks in decision-making'
            },
            'Consistency': {
                'score': trait_profile.consistency,
                'interpretation': self._interpret_trait_score(trait_profile.consistency, 'consistency'),
                'description': 'Stability of behavioral patterns'
            },
            'Learning Ability': {
                'score': trait_profile.learning_ability,
                'interpretation': self._interpret_trait_score(trait_profile.learning_ability, 'learning'),
                'description': 'Ability to adapt and learn from feedback'
            },
            'Decision Speed': {
                'score': trait_profile.decision_speed,
                'interpretation': self._interpret_trait_score(trait_profile.decision_speed, 'speed'),
                'description': 'Speed of decision-making processes'
            },
            'Emotional Regulation': {
                'score': trait_profile.emotional_regulation,
                'interpretation': self._interpret_trait_score(trait_profile.emotional_regulation, 'emotional'),
                'description': 'Ability to manage emotional responses'
            }
        }
        
        # Calculate trait strengths and areas for improvement
        strengths = [trait for trait, data in traits.items() if data['score'] > 0.7]
        improvements = [trait for trait, data in traits.items() if data['score'] < 0.3]
        
        return {
            'traits': traits,
            'overall_assessment': {
                'average_score': trait_profile.get_average_trait_score(),
                'confidence_level': trait_profile.confidence_level,
                'validation_status': trait_profile.validation_status
            },
            'strengths': strengths,
            'areas_for_improvement': improvements,
            'trait_summary': trait_profile.get_trait_summary()
        }
    
    def _generate_comparative_analysis(self, trait_profile: TraitProfile) -> Dict[str, Any]:
        """Generate comparative analysis section."""
        # Get comparison data from similar profiles
        similar_profiles = TraitProfile.objects.filter(
            confidence_level__gte=self.report_settings['confidence_threshold']
        ).exclude(id=trait_profile.id)[:self.report_settings['max_comparison_profiles']]
        
        if not similar_profiles:
            return {
                'comparison_available': False,
                'message': 'Insufficient data for comparative analysis'
            }
        
        # Calculate percentile rankings
        percentiles = {}
        for trait_name in ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']:
            trait_scores = [getattr(profile, trait_name) for profile in similar_profiles]
            user_score = getattr(trait_profile, trait_name)
            
            # Calculate percentile
            below_count = sum(1 for score in trait_scores if score < user_score)
            percentile = (below_count / len(trait_scores)) * 100 if trait_scores else 50
            
            percentiles[trait_name] = {
                'percentile': percentile,
                'interpretation': self._interpret_percentile(percentile)
            }
        
        return {
            'comparison_available': True,
            'comparison_group_size': len(similar_profiles),
            'percentile_rankings': percentiles,
            'relative_strengths': [trait for trait, data in percentiles.items() if data['percentile'] > 75],
            'relative_weaknesses': [trait for trait, data in percentiles.items() if data['percentile'] < 25]
        }
    
    def _generate_insights_and_recommendations(self, trait_profile: TraitProfile) -> Dict[str, Any]:
        """Generate insights and recommendations section."""
        insights = []
        recommendations = []
        
        # Generate insights based on trait combinations
        if trait_profile.risk_tolerance > 0.7 and trait_profile.consistency < 0.3:
            insights.append("High risk tolerance combined with low consistency suggests impulsive decision-making")
            recommendations.append("Consider implementing decision-making frameworks to improve consistency")
        
        if trait_profile.learning_ability > 0.7 and trait_profile.emotional_regulation > 0.7:
            insights.append("Strong learning ability with good emotional regulation indicates high adaptability")
            recommendations.append("Leverage adaptability for roles requiring quick learning and change management")
        
        if trait_profile.decision_speed < 0.3:
            insights.append("Deliberate decision-making style suggests thorough analysis")
            recommendations.append("Consider roles requiring careful analysis and strategic thinking")
        
        # Default insights if no specific patterns
        if not insights:
            insights.append("Balanced trait profile with moderate scores across dimensions")
            recommendations.append("Continue development across all trait dimensions")
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'development_priorities': self._generate_development_priorities(trait_profile),
            'role_suggestions': self._generate_role_suggestions(trait_profile)
        }
    
    def _generate_methodology_section(self, session: BehavioralSession, trait_profile: TraitProfile) -> Dict[str, Any]:
        """Generate methodology and validation section."""
        return {
            'assessment_methodology': {
                'data_collection': 'Granular behavioral event logging with millisecond precision',
                'metric_extraction': 'Scientific aggregation of raw events into validated metrics',
                'trait_inference': 'Multi-dimensional trait mapping using documented logic',
                'validation_approach': 'Statistical validation with confidence intervals'
            },
            'data_quality': {
                'session_duration': session.total_duration,
                'event_count': session.events.count(),
                'validation_status': trait_profile.validation_status if trait_profile else 'pending',
                'confidence_level': trait_profile.confidence_level if trait_profile else 0.0
            },
            'scientific_validation': {
                'assessment_version': trait_profile.assessment_version if trait_profile else '1.0',
                'data_schema_version': trait_profile.data_schema_version if trait_profile else '1.0',
                'calculation_timestamp': trait_profile.calculation_timestamp.isoformat() if trait_profile else timezone.now().isoformat(),
                'reproducibility': 'All calculations are versioned and documented'
            }
        }
    
    def _generate_user_overview(self, sessions: List[BehavioralSession], trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Generate user overview for multi-session reports."""
        latest_profile = trait_profiles.first()
        
        return {
            'user_summary': {
                'total_sessions': sessions.count(),
                'total_assessments': trait_profiles.count(),
                'first_assessment': trait_profiles.last().calculation_timestamp.isoformat(),
                'latest_assessment': latest_profile.calculation_timestamp.isoformat(),
                'average_confidence': trait_profiles.aggregate(Avg('confidence_level'))['confidence_level__avg']
            },
            'current_profile': {
                'traits': {
                    'risk_tolerance': latest_profile.risk_tolerance,
                    'consistency': latest_profile.consistency,
                    'learning_ability': latest_profile.learning_ability,
                    'decision_speed': latest_profile.decision_speed,
                    'emotional_regulation': latest_profile.emotional_regulation
                },
                'overall_score': latest_profile.get_average_trait_score()
            }
        }
    
    def _generate_trend_analysis(self, trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Generate trend analysis for user's trait development."""
        if len(trait_profiles) < 2:
            return {
                'trend_available': False,
                'message': 'Insufficient data for trend analysis (need at least 2 assessments)'
            }
        
        # Calculate trends for each trait
        trends = {}
        for trait_name in ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']:
            scores = [getattr(profile, trait_name) for profile in trait_profiles]
            
            # Simple trend calculation
            if len(scores) >= 2:
                trend_direction = 'increasing' if scores[-1] > scores[0] else 'decreasing' if scores[-1] < scores[0] else 'stable'
                trend_magnitude = abs(scores[-1] - scores[0])
                
                trends[trait_name] = {
                    'trend_direction': trend_direction,
                    'trend_magnitude': trend_magnitude,
                    'current_score': scores[-1],
                    'initial_score': scores[0]
                }
        
        return {
            'trend_available': True,
            'trends': trends,
            'overall_trend': self._calculate_overall_trend(trait_profiles)
        }
    
    def _generate_performance_summary(self, sessions: List[BehavioralSession], trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Generate performance summary for user."""
        return {
            'session_performance': {
                'total_sessions': sessions.count(),
                'completed_sessions': sessions.filter(is_completed=True).count(),
                'average_session_duration': sessions.aggregate(Avg('total_duration'))['total_duration__avg'],
                'engagement_trend': self._calculate_engagement_trend(sessions)
            },
            'assessment_performance': {
                'total_assessments': trait_profiles.count(),
                'valid_assessments': trait_profiles.filter(validation_status='valid').count(),
                'average_confidence': trait_profiles.aggregate(Avg('confidence_level'))['confidence_level__avg']
            }
        }
    
    def _generate_user_comparative_analysis(self, trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Generate comparative analysis for user across time."""
        if len(trait_profiles) < 2:
            return {
                'comparison_available': False,
                'message': 'Insufficient data for comparative analysis'
            }
        
        latest_profile = trait_profiles.first()
        earliest_profile = trait_profiles.last()
        
        # Calculate improvements
        improvements = {}
        for trait_name in ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']:
            initial_score = getattr(earliest_profile, trait_name)
            current_score = getattr(latest_profile, trait_name)
            improvement = current_score - initial_score
            
            improvements[trait_name] = {
                'improvement': improvement,
                'improvement_percentage': (improvement / initial_score * 100) if initial_score > 0 else 0,
                'direction': 'improved' if improvement > 0 else 'declined' if improvement < 0 else 'stable'
            }
        
        return {
            'comparison_available': True,
            'improvements': improvements,
            'most_improved_trait': max(improvements.items(), key=lambda x: x[1]['improvement'])[0] if improvements else None,
            'time_span': (latest_profile.calculation_timestamp - earliest_profile.calculation_timestamp).days
        }
    
    def _generate_user_recommendations(self, trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Generate recommendations for user development."""
        latest_profile = trait_profiles.first()
        
        recommendations = []
        development_areas = []
        
        # Identify areas for development
        for trait_name in ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']:
            score = getattr(latest_profile, trait_name)
            if score < 0.4:
                development_areas.append(trait_name)
        
        if development_areas:
            recommendations.append(f"Focus on developing: {', '.join(development_areas)}")
        
        # Trend-based recommendations
        if len(trait_profiles) >= 2:
            trends = self._calculate_trends(trait_profiles)
            if trends['overall_trend'] == 'improving':
                recommendations.append("Continue current development approach - showing positive trends")
            elif trends['overall_trend'] == 'declining':
                recommendations.append("Consider reviewing development strategies - showing declining trends")
        
        return {
            'recommendations': recommendations,
            'development_areas': development_areas,
            'next_steps': self._generate_next_steps(latest_profile)
        }
    
    # Helper methods
    def _interpret_trait_score(self, score: float, trait_type: str) -> str:
        """Interpret trait score with context."""
        if score < 0.3:
            return f"Low {trait_type}"
        elif score < 0.7:
            return f"Moderate {trait_type}"
        else:
            return f"High {trait_type}"
    
    def _interpret_percentile(self, percentile: float) -> str:
        """Interpret percentile ranking."""
        if percentile >= 90:
            return "Exceptional"
        elif percentile >= 75:
            return "Above Average"
        elif percentile >= 50:
            return "Average"
        elif percentile >= 25:
            return "Below Average"
        else:
            return "Needs Development"
    
    def _generate_key_recommendations(self, trait_profile: TraitProfile) -> List[str]:
        """Generate key recommendations based on trait profile."""
        if not trait_profile:
            return ["Complete trait inference to generate personalized recommendations"]
        
        recommendations = []
        
        if trait_profile.risk_tolerance and trait_profile.risk_tolerance < 30:
            recommendations.append("Consider opportunities to develop risk-taking in controlled environments")
        
        if trait_profile.consistency and trait_profile.consistency < 30:
            recommendations.append("Focus on developing consistent behavioral patterns")
        
        if trait_profile.learning_agility and trait_profile.learning_agility > 70:
            recommendations.append("Leverage strong learning ability for rapid skill development")
        
        return recommendations
    
    def _generate_development_priorities(self, trait_profile: TraitProfile) -> List[str]:
        """Generate development priorities."""
        priorities = []
        
        if trait_profile.risk_tolerance < 0.4:
            priorities.append("Risk tolerance development")
        
        if trait_profile.consistency < 0.4:
            priorities.append("Behavioral consistency improvement")
        
        if trait_profile.emotional_regulation < 0.4:
            priorities.append("Emotional regulation skills")
        
        return priorities
    
    def _generate_role_suggestions(self, trait_profile: TraitProfile) -> List[str]:
        """Generate role suggestions based on trait profile."""
        suggestions = []
        
        if trait_profile.risk_tolerance > 0.7 and trait_profile.decision_speed > 0.7:
            suggestions.append("Trading or investment roles")
        
        if trait_profile.consistency > 0.7 and trait_profile.emotional_regulation > 0.7:
            suggestions.append("Quality assurance or compliance roles")
        
        if trait_profile.learning_ability > 0.7:
            suggestions.append("Research or innovation roles")
        
        return suggestions
    
    def _calculate_event_frequency(self, events) -> Dict[str, Any]:
        """Calculate event frequency patterns."""
        if not events:
            return {}
        
        # Calculate events per minute
        total_duration = (events.last().timestamp - events.first().timestamp).total_seconds() / 60
        events_per_minute = len(events) / max(total_duration, 1)
        
        return {
            'events_per_minute': events_per_minute,
            'total_duration_minutes': total_duration
        }
    
    def _calculate_response_times(self, events) -> Dict[str, Any]:
        """Calculate response time metrics."""
        # Implementation would calculate response times from events
        return {
            'average_response_time': 0.0,
            'response_time_std': 0.0
        }
    
    def _analyze_interaction_patterns(self, events) -> Dict[str, Any]:
        """Analyze interaction patterns."""
        # Implementation would analyze interaction patterns
        return {
            'pattern_type': 'standard',
            'complexity_score': 0.5
        }
    
    def _calculate_overall_trend(self, trait_profiles: List[TraitProfile]) -> str:
        """Calculate overall trend direction."""
        if len(trait_profiles) < 2:
            return 'insufficient_data'
        
        first_avg = trait_profiles.last().get_average_trait_score()
        last_avg = trait_profiles.first().get_average_trait_score()
        
        if last_avg > first_avg + 0.1:
            return 'improving'
        elif last_avg < first_avg - 0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_engagement_trend(self, sessions) -> str:
        """Calculate engagement trend."""
        if len(sessions) < 2:
            return 'insufficient_data'
        
        # Implementation would calculate engagement trend
        return 'stable'
    
    def _calculate_trends(self, trait_profiles: List[TraitProfile]) -> Dict[str, Any]:
        """Calculate trends for all traits."""
        trends = {}
        for trait_name in ['risk_tolerance', 'consistency', 'learning_ability', 'decision_speed', 'emotional_regulation']:
            scores = [getattr(profile, trait_name) for profile in trait_profiles]
            if len(scores) >= 2:
                trend = 'improving' if scores[-1] > scores[0] else 'declining' if scores[-1] < scores[0] else 'stable'
                trends[trait_name] = trend
        
        return trends
    
    def _generate_next_steps(self, trait_profile: TraitProfile) -> List[str]:
        """Generate next steps for development."""
        return [
            "Schedule follow-up assessment in 3 months",
            "Focus on identified development areas",
            "Consider role-specific training programs"
        ]
    
    def generate_session_report(self, session_id: str) -> Dict[str, Any]:
        """Generate report for a specific session."""
        return self.process({'session_id': session_id, 'report_type': 'individual_assessment'})
    
    def generate_user_report(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive report for a user."""
        return self.process({'user_id': user_id, 'report_type': 'user_comprehensive'})
    
    def batch_generate_reports(self, session_ids: List[str]) -> Dict[str, Any]:
        """Generate reports for multiple sessions."""
        results = {}
        for session_id in session_ids:
            try:
                result = self.generate_session_report(session_id)
                results[session_id] = result
            except Exception as e:
                results[session_id] = {'error': str(e)}
        
        return results 