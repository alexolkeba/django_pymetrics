"""
Celery Tasks for Report Generation

This module contains Celery tasks for generating comprehensive reports
and dashboards in the Django Pymetrics system.
"""

import logging
from typing import Dict, Any, List
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from agents.report_generator import ReportGenerator
from behavioral_data.models import BehavioralSession
from ai_model.models import TraitProfile

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='tasks.reporting.generate_session_report')
def generate_session_report(self, session_id: str) -> Dict[str, Any]:
    """
    Generate report for a single session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dict: Generated report with all sections
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        # Validate session exists
        session = BehavioralSession.objects.get(session_id=session_id)
        
        # Initialize ReportGenerator agent
        generator = ReportGenerator()
        
        # Generate report
        result = generator.generate_session_report(session_id)
        
        logger.info(f"Successfully generated report for session {session_id}")
        return result
        
    except BehavioralSession.DoesNotExist:
        error_msg = f"Session {session_id} not found"
        logger.error(error_msg)
        return {'processed': False, 'error': error_msg, 'session_id': session_id}
        
    except Exception as e:
        logger.error(f"Error generating report for session {session_id}: {str(e)}")
        # Retry with exponential backoff
        raise self.retry(countdown=240, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.reporting.generate_user_report')
def generate_user_report(self, user_id: str) -> Dict[str, Any]:
    """
    Generate comprehensive report for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dict: Generated user report with trends and analysis
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        # Initialize ReportGenerator agent
        generator = ReportGenerator()
        
        # Generate user report
        result = generator.generate_user_report(user_id)
        
        logger.info(f"Successfully generated user report for user {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error generating user report for user {user_id}: {str(e)}")
        raise self.retry(countdown=300, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.reporting.generate_batch_reports')
def generate_batch_reports(self, session_ids: List[str]) -> Dict[str, Any]:
    """
    Generate reports for multiple sessions in batch.
    
    Args:
        session_ids: List of session identifiers
        
    Returns:
        Dict: Batch report generation results
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        generator = ReportGenerator()
        results = {}
        
        for session_id in session_ids:
            try:
                result = generator.generate_session_report(session_id)
                results[session_id] = result
            except Exception as e:
                logger.error(f"Error processing session {session_id}: {str(e)}")
                results[session_id] = {'processed': False, 'error': str(e)}
        
        success_count = sum(1 for r in results.values() if r.get('processed', False))
        
        logger.info(f"Batch report generation completed: {success_count}/{len(session_ids)} successful")
        return {
            'processed': True,
            'total_sessions': len(session_ids),
            'successful_sessions': success_count,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Error in batch report generation: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.reporting.generate_pending_reports')
def generate_pending_reports(self) -> Dict[str, Any]:
    """
    Generate reports for all completed sessions without reports.
    
    Returns:
        Dict: Processing results
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        # Find completed sessions without reports
        # This would need to be implemented based on how reports are tracked
        completed_sessions = BehavioralSession.objects.filter(
            is_completed=True
        ).values_list('session_id', flat=True)[:50]  # Process 50 at a time
        
        if not completed_sessions:
            logger.info("No pending sessions for report generation")
            return {'processed_count': 0, 'message': 'No pending sessions'}
        
        # Process in batch
        result = generate_batch_reports.delay(list(completed_sessions))
        
        logger.info(f"Started report generation for {len(completed_sessions)} sessions")
        return {
            'processed_count': len(completed_sessions),
            'task_id': result.id,
            'message': 'Batch report generation started'
        }
        
    except Exception as e:
        logger.error(f"Error in pending report generation: {str(e)}")
        raise self.retry(countdown=600, max_retries=3, exc=e)


@shared_task(bind=True, name='tasks.reporting.generate_executive_summary')
def generate_executive_summary(self, user_id: str = None, date_range: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Generate executive summary report for high-level insights.
    
    Args:
        user_id: Optional user identifier for user-specific summary
        date_range: Optional date range for filtering
        
    Returns:
        Dict: Executive summary with key insights
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        generator = ReportGenerator()
        
        # Generate executive summary
        if user_id:
            result = generator.generate_user_report(user_id)
        else:
            # Generate system-wide summary
            result = {
                'report_type': 'executive_summary',
                'generated_at': timezone.now().isoformat(),
                'insights': {
                    'total_sessions': BehavioralSession.objects.count(),
                    'completed_sessions': BehavioralSession.objects.filter(is_completed=True).count(),
                    'active_users': BehavioralSession.objects.values('user').distinct().count(),
                    'average_session_duration': BehavioralSession.objects.aggregate(
                        avg_duration=models.Avg('total_duration')
                    )['avg_duration'] or 0
                }
            }
        
        logger.info(f"Successfully generated executive summary")
        return result
        
    except Exception as e:
        logger.error(f"Error generating executive summary: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)


@shared_task(bind=True, name='tasks.reporting.export_reports')
def export_reports(self, session_ids: List[str], format: str = 'json') -> Dict[str, Any]:
    """
    Export reports in various formats.
    
    Args:
        session_ids: List of session identifiers
        format: Export format (json, csv, pdf)
        
    Returns:
        Dict: Export results with file information
    """
    logger = logging.getLogger('tasks.reporting')
    
    try:
        generator = ReportGenerator()
        export_results = {}
        
        for session_id in session_ids:
            try:
                # Generate report
                report = generator.generate_session_report(session_id)
                
                # Export in specified format
                if format == 'json':
                    export_results[session_id] = report
                elif format == 'csv':
                    # Convert to CSV format
                    export_results[session_id] = self._convert_to_csv(report)
                elif format == 'pdf':
                    # Convert to PDF format
                    export_results[session_id] = self._convert_to_pdf(report)
                else:
                    export_results[session_id] = {'error': f'Unsupported format: {format}'}
                    
            except Exception as e:
                logger.error(f"Error exporting report for session {session_id}: {str(e)}")
                export_results[session_id] = {'error': str(e)}
        
        logger.info(f"Export completed for {len(session_ids)} sessions in {format} format")
        return {
            'processed': True,
            'format': format,
            'total_sessions': len(session_ids),
            'results': export_results
        }
        
    except Exception as e:
        logger.error(f"Error in report export: {str(e)}")
        raise self.retry(countdown=300, max_retries=2, exc=e)
    
    def _convert_to_csv(self, report: Dict[str, Any]) -> str:
        """Convert report to CSV format."""
        # Implementation would convert report to CSV
        return "csv_data_placeholder"
    
    def _convert_to_pdf(self, report: Dict[str, Any]) -> bytes:
        """Convert report to PDF format."""
        # Implementation would convert report to PDF
        return b"pdf_data_placeholder"
