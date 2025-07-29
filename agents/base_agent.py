"""
Base Agent Class for Django Pymetrics

This module provides the foundation for all agentic components in the system.
The base agent class includes common functionality for logging, error handling,
monitoring, and configuration management.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import traceback
import json


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Django Pymetrics system.
    
    Provides common functionality for logging, error handling, monitoring,
    and configuration management. All agents should inherit from this class.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name of the agent for logging and identification
            config: Optional configuration dictionary
        """
        self.agent_name = agent_name
        self.config = config or {}
        self.logger = logging.getLogger(f'agents.{agent_name}')
        self.start_time = timezone.now()
        self.processed_count = 0
        self.error_count = 0
        self.last_activity = timezone.now()
        
        # Initialize agent-specific configuration
        self._load_config()
        
        self.logger.info(f"Agent {agent_name} initialized with config: {self.config}")
    
    def _load_config(self):
        """Load agent-specific configuration from settings."""
        agent_config_key = f'{self.agent_name.upper()}_CONFIG'
        if hasattr(settings, agent_config_key):
            self.config.update(getattr(settings, agent_config_key))
    
    def _serialize_for_logging(self, obj: Any) -> Any:
        """
        Serialize object for JSON logging, handling non-serializable types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serializable representation of the object
        """
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self._serialize_for_logging(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): self._serialize_for_logging(v) for k, v in obj.items()}
        else:
            return str(obj)
    
    def log_activity(self, message: str, level: str = 'info', **kwargs):
        """
        Log agent activity with structured data.
        
        Args:
            message: Log message
            level: Log level (debug, info, warning, error)
            **kwargs: Additional structured data to log
        """
        log_data = {
            'agent': self.agent_name,
            'timestamp': timezone.now().isoformat(),
            'processed_count': self.processed_count,
            'error_count': self.error_count,
            'uptime_seconds': (timezone.now() - self.start_time).total_seconds(),
        }
        
        # Add additional kwargs, serializing them for JSON compatibility
        for key, value in kwargs.items():
            log_data[key] = self._serialize_for_logging(value)
        
        log_message = f"{message} | {json.dumps(log_data)}"
        
        if level == 'debug':
            self.logger.debug(log_message)
        elif level == 'info':
            self.logger.info(log_message)
        elif level == 'warning':
            self.logger.warning(log_message)
        elif level == 'error':
            self.logger.error(log_message)
        
        self.last_activity = timezone.now()
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Handle errors with structured logging and recovery.
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        self.error_count += 1
        error_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
        }
        
        self.log_activity(
            f"Error in {self.agent_name}: {str(error)}",
            level='error',
            **error_data
        )
        
        # Implement error recovery logic
        self._recover_from_error(error, context)
    
    def _recover_from_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Implement error recovery logic.
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        # Default recovery: log and continue
        self.log_activity(
            f"Recovering from error in {self.agent_name}",
            level='info',
            recovery_strategy='log_and_continue'
        )
    
    def validate_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate input data against a schema.
        
        Args:
            data: Input data to validate
            schema: Schema definition for validation
            
        Returns:
            bool: True if data is valid
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Basic validation - can be extended with more sophisticated validation
            for field, field_schema in schema.items():
                if field_schema.get('required', False) and field not in data:
                    raise ValidationError(f"Required field '{field}' is missing")
                
                if field in data:
                    field_type = field_schema.get('type')
                    if field_type and not isinstance(data[field], field_type):
                        raise ValidationError(f"Field '{field}' must be of type {field_type}")
            
            return True
        except Exception as e:
            self.handle_error(e, {'validation_data': data, 'schema': schema})
            raise
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get current performance metrics for the agent.
        
        Returns:
            Dict: Performance metrics
        """
        uptime = (timezone.now() - self.start_time).total_seconds()
        
        return {
            'agent_name': self.agent_name,
            'uptime_seconds': uptime,
            'processed_count': self.processed_count,
            'error_count': self.error_count,
            'success_rate': (self.processed_count - self.error_count) / max(self.processed_count, 1),
            'last_activity': self.last_activity.isoformat(),
            'config': self.config,
        }
    
    def update_processed_count(self, count: int = 1):
        """Update the processed count."""
        self.processed_count += count
        self.log_activity(f"Processed {count} items", level='debug')
    
    def get_processing_time(self) -> float:
        """
        Get the processing time for the last operation.
        
        Returns:
            float: Processing time in seconds
        """
        return (timezone.now() - self.start_time).total_seconds()
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data with the agent.
        
        Args:
            data: Input data to process
            
        Returns:
            Dict: Processed results
        """
        pass
    
    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate agent output.
        
        Args:
            output: Output data to validate
            
        Returns:
            bool: True if output is valid
        """
        pass
    
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent with error handling and monitoring.
        
        Args:
            data: Input data to process
            
        Returns:
            Dict: Processed results
        """
        start_time = time.time()
        
        try:
            # Validate input
            if hasattr(self, 'input_schema'):
                self.validate_input(data, self.input_schema)
            
            # Process data
            result = self.process(data)
            
            # Validate output
            if not self.validate_output(result):
                raise ValidationError("Agent output validation failed")
            
            # Update metrics
            processing_time = time.time() - start_time
            self.update_processed_count()
            
            self.log_activity(
                f"Successfully processed data in {processing_time:.2f}s",
                level='info',
                processing_time=processing_time,
                result_keys=list(result.keys())
            )
            
            return result
            
        except Exception as e:
            self.handle_error(e, {'input_data': data})
            raise
    
    def cleanup(self):
        """Cleanup resources when agent is stopped."""
        self.log_activity(
            f"Agent {self.agent_name} shutting down",
            level='info',
            final_metrics=self.get_performance_metrics()
        )


class EventProcessingAgent(BaseAgent):
    """
    Base class for event processing agents.
    
    Provides common functionality for processing behavioral events
    with validation and error handling.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name, config)
        self.input_schema = {
            'session_id': {'type': str, 'required': True},
            'event_type': {'type': str, 'required': True},
            'timestamp': {'type': str, 'required': False},  # Made optional for flexibility
            'event_data': {'type': dict, 'required': True},
        }
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate event processing output."""
        required_fields = ['processed', 'session_id']
        return all(field in output for field in required_fields)


class MetricExtractionAgent(BaseAgent):
    """
    Base class for metric extraction agents.
    
    Provides common functionality for extracting metrics from behavioral data
    with scientific validation.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name, config)
        self.input_schema = {
            'session_id': {'type': str, 'required': True},
            'game_type': {'type': str, 'required': True},
            'events': {'type': list, 'required': True},
        }
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate metric extraction output."""
        required_fields = ['session_id', 'metrics', 'calculation_timestamp']
        return all(field in output for field in required_fields)


class TraitInferenceAgent(BaseAgent):
    """
    Base class for trait inference agents.
    
    Provides common functionality for inferring traits from metrics
    with scientific validation.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name, config)
        self.input_schema = {
            'session_id': {'type': str, 'required': True},
            'metrics': {'type': dict, 'required': True},
            'success_model_id': {'type': str, 'required': False},
        }
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate trait inference output."""
        required_fields = ['session_id', 'traits', 'confidence_level', 'recommendation_band']
        return all(field in output for field in required_fields)


class ReportGenerationAgent(BaseAgent):
    """
    Base class for report generation agents.
    
    Provides common functionality for generating reports and dashboards
    with data aggregation and visualization.
    """
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name, config)
        self.input_schema = {
            'user_id': {'type': str, 'required': True},
            'report_type': {'type': str, 'required': True},
            'date_range': {'type': dict, 'required': False},
        }
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate report generation output."""
        required_fields = ['user_id', 'report_type', 'generated_at', 'data']
        return all(field in output for field in required_fields) 