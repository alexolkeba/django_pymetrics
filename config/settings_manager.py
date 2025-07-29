"""
Settings Manager for Django Pymetrics

Centralized configuration management system that handles all application settings,
scientific parameters, and deployment configurations with validation and versioning.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


@dataclass
class ConfigSection:
    """Base class for configuration sections."""
    version: str = "1.0"
    last_updated: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary."""
        return cls(**data)


class SettingsManager:
    """
    Centralized settings management for the Django Pymetrics framework.
    
    This class provides a unified interface for managing all configuration
    aspects including scientific parameters, validation thresholds, API settings,
    and deployment configurations.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings manager.
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config_data = {}
        self.config_cache = {}
        self._load_configuration()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        base_dir = getattr(settings, 'BASE_DIR', Path.cwd())
        return str(base_dir / 'config' / 'pymetrics_config.json')
    
    def _load_configuration(self) -> None:
        """Load configuration from file and Django settings."""
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Could not load config file {self.config_file}: {e}")
                self.config_data = {}
        
        # Merge with Django settings
        self._merge_django_settings()
        
        # Apply defaults
        self._apply_defaults()
    
    def _merge_django_settings(self) -> None:
        """Merge relevant Django settings into configuration."""
        django_mappings = {
            'BEHAVIORAL_DATA_SETTINGS': 'behavioral_data',
            'SCIENTIFIC_VALIDATION_SETTINGS': 'scientific_validation',
            'CELERY_TASK_ROUTES': 'celery.task_routes',
            'CELERY_BEAT_SCHEDULE': 'celery.beat_schedule',
            'REST_FRAMEWORK': 'api.rest_framework'
        }
        
        for django_setting, config_path in django_mappings.items():
            if hasattr(settings, django_setting):
                self._set_nested_value(config_path, getattr(settings, django_setting))
    
    def _apply_defaults(self) -> None:
        """Apply default configuration values."""
        defaults = {
            'behavioral_data': {
                'data_retention_days': 365,
                'anonymization_enabled': True,
                'min_session_duration_ms': 30000,
                'max_session_duration_ms': 7200000,
                'event_batch_size': 100,
                'metric_calculation_interval': 300,
                'trait_inference_interval': 600
            },
            'scientific_validation': {
                'min_data_completeness': 80.0,
                'min_quality_score': 70.0,
                'min_reliability_score': 75.0,
                'confidence_interval_level': 0.95,
                'min_sample_size': 10,
                'outlier_threshold': 2.5,
                'validation_enabled': True
            },
            'trait_mapping': {
                'risk_tolerance': {
                    'enabled': True,
                    'confidence_threshold': 0.7,
                    'weight_function': 'weighted_average',
                    'normalization_method': 'z_score'
                },
                'learning_ability': {
                    'enabled': True,
                    'confidence_threshold': 0.75,
                    'weight_function': 'learning_curve_analysis',
                    'normalization_method': 'sigmoid'
                },
                'emotion_regulation': {
                    'enabled': True,
                    'confidence_threshold': 0.7,
                    'weight_function': 'emotion_regulation_model',
                    'normalization_method': 'robust_scaling'
                }
            },
            'agents': {
                'event_logger': {
                    'enabled': True,
                    'batch_size': 50,
                    'validation_level': 'strict',
                    'retry_attempts': 3
                },
                'metric_extractor': {
                    'enabled': True,
                    'min_events_for_metrics': 10,
                    'confidence_interval_level': 0.95,
                    'outlier_threshold': 2.5
                },
                'trait_inferencer': {
                    'enabled': True,
                    'min_confidence_threshold': 0.7,
                    'enable_cross_validation': True,
                    'temporal_stability_check': True
                },
                'report_generator': {
                    'enabled': True,
                    'include_confidence_intervals': True,
                    'include_recommendations': True,
                    'format': 'comprehensive'
                }
            },
            'api': {
                'rate_limiting': {
                    'enabled': True,
                    'anon_rate': '100/hour',
                    'user_rate': '1000/hour',
                    'event_ingestion_rate': '1000/minute'
                },
                'authentication': {
                    'required': True,
                    'session_timeout': 3600,
                    'token_expiry': 86400
                },
                'response_format': {
                    'include_metadata': True,
                    'include_confidence': True,
                    'include_explanations': True
                }
            },
            'deployment': {
                'environment': 'development',
                'debug_mode': True,
                'log_level': 'INFO',
                'monitoring': {
                    'enabled': False,
                    'metrics_collection': False,
                    'error_reporting': False
                }
            }
        }
        
        # Apply defaults only for missing keys
        for key, default_value in defaults.items():
            if key not in self.config_data:
                self.config_data[key] = default_value
            else:
                # Recursively apply defaults for nested dictionaries
                self._apply_nested_defaults(self.config_data[key], default_value)
    
    def _apply_nested_defaults(self, current: Dict[str, Any], defaults: Dict[str, Any]) -> None:
        """Apply default values recursively for nested dictionaries."""
        for key, default_value in defaults.items():
            if key not in current:
                current[key] = default_value
            elif isinstance(default_value, dict) and isinstance(current[key], dict):
                self._apply_nested_defaults(current[key], default_value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation for nested values)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        # Check cache first
        if key in self.config_cache:
            return self.config_cache[key]
        
        # Get value using dot notation
        value = self._get_nested_value(key, default)
        
        # Cache the result
        self.config_cache[key] = value
        
        return value
    
    def set(self, key: str, value: Any, persist: bool = False) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
            persist: Whether to persist to file
        """
        # Set value using dot notation
        self._set_nested_value(key, value)
        
        # Clear cache for this key
        if key in self.config_cache:
            del self.config_cache[key]
        
        # Persist if requested
        if persist:
            self.save_configuration()
    
    def _get_nested_value(self, key: str, default: Any = None) -> Any:
        """Get nested value using dot notation."""
        keys = key.split('.')
        current = self.config_data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def _set_nested_value(self, key: str, value: Any) -> None:
        """Set nested value using dot notation."""
        keys = key.split('.')
        current = self.config_data
        
        # Navigate to parent dictionary
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the final value
        current[keys[-1]] = value
    
    def save_configuration(self) -> None:
        """Save current configuration to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2, default=str)
            
            logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise
    
    def reload_configuration(self) -> None:
        """Reload configuration from file and Django settings."""
        self.config_cache.clear()
        self._load_configuration()
        logger.info("Configuration reloaded")
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate current configuration.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'sections_validated': []
        }
        
        # Validate behavioral data settings
        behavioral_validation = self._validate_behavioral_data_settings()
        validation_results['sections_validated'].append('behavioral_data')
        validation_results['errors'].extend(behavioral_validation.get('errors', []))
        validation_results['warnings'].extend(behavioral_validation.get('warnings', []))
        
        # Validate scientific validation settings
        scientific_validation = self._validate_scientific_settings()
        validation_results['sections_validated'].append('scientific_validation')
        validation_results['errors'].extend(scientific_validation.get('errors', []))
        validation_results['warnings'].extend(scientific_validation.get('warnings', []))
        
        # Validate agent settings
        agent_validation = self._validate_agent_settings()
        validation_results['sections_validated'].append('agents')
        validation_results['errors'].extend(agent_validation.get('errors', []))
        validation_results['warnings'].extend(agent_validation.get('warnings', []))
        
        # Set overall validity
        validation_results['valid'] = len(validation_results['errors']) == 0
        
        return validation_results
    
    def _validate_behavioral_data_settings(self) -> Dict[str, Any]:
        """Validate behavioral data configuration."""
        errors = []
        warnings = []
        
        behavioral_config = self.get('behavioral_data', {})
        
        # Check required settings
        required_settings = [
            'data_retention_days',
            'min_session_duration_ms',
            'max_session_duration_ms',
            'event_batch_size'
        ]
        
        for setting in required_settings:
            if setting not in behavioral_config:
                errors.append(f"Missing required behavioral data setting: {setting}")
        
        # Validate ranges
        if 'min_session_duration_ms' in behavioral_config and 'max_session_duration_ms' in behavioral_config:
            min_duration = behavioral_config['min_session_duration_ms']
            max_duration = behavioral_config['max_session_duration_ms']
            
            if min_duration >= max_duration:
                errors.append("min_session_duration_ms must be less than max_session_duration_ms")
            
            if min_duration < 1000:  # Less than 1 second
                warnings.append("min_session_duration_ms is very short (< 1 second)")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_scientific_settings(self) -> Dict[str, Any]:
        """Validate scientific validation configuration."""
        errors = []
        warnings = []
        
        scientific_config = self.get('scientific_validation', {})
        
        # Check percentage values are in valid range
        percentage_settings = [
            'min_data_completeness',
            'min_quality_score',
            'min_reliability_score'
        ]
        
        for setting in percentage_settings:
            if setting in scientific_config:
                value = scientific_config[setting]
                if not (0 <= value <= 100):
                    errors.append(f"{setting} must be between 0 and 100")
        
        # Check confidence interval level
        if 'confidence_interval_level' in scientific_config:
            ci_level = scientific_config['confidence_interval_level']
            if not (0.5 <= ci_level <= 0.99):
                errors.append("confidence_interval_level must be between 0.5 and 0.99")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_agent_settings(self) -> Dict[str, Any]:
        """Validate agent configuration."""
        errors = []
        warnings = []
        
        agents_config = self.get('agents', {})
        
        # Check that all required agents are configured
        required_agents = ['event_logger', 'metric_extractor', 'trait_inferencer', 'report_generator']
        
        for agent in required_agents:
            if agent not in agents_config:
                warnings.append(f"Agent {agent} not configured, using defaults")
            elif not agents_config[agent].get('enabled', True):
                warnings.append(f"Agent {agent} is disabled")
        
        return {'errors': errors, 'warnings': warnings}
    
    def get_section(self, section_name: str) -> Dict[str, Any]:
        """Get entire configuration section."""
        return self.get(section_name, {})
    
    def update_section(self, section_name: str, section_data: Dict[str, Any], persist: bool = False) -> None:
        """Update entire configuration section."""
        self.set(section_name, section_data, persist)
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration."""
        environment = self.get('deployment.environment', 'development')
        
        env_configs = {
            'development': {
                'debug': True,
                'log_level': 'DEBUG',
                'database_pool_size': 5,
                'cache_timeout': 300,
                'rate_limiting_strict': False
            },
            'testing': {
                'debug': False,
                'log_level': 'INFO',
                'database_pool_size': 3,
                'cache_timeout': 60,
                'rate_limiting_strict': True
            },
            'production': {
                'debug': False,
                'log_level': 'WARNING',
                'database_pool_size': 20,
                'cache_timeout': 3600,
                'rate_limiting_strict': True
            }
        }
        
        return env_configs.get(environment, env_configs['development'])
    
    def export_configuration(self, file_path: str) -> None:
        """Export current configuration to specified file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config_data, f, indent=2, default=str)
            logger.info(f"Configuration exported to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")
            raise
    
    def import_configuration(self, file_path: str, merge: bool = True, persist: bool = True) -> None:
        """
        Import configuration from specified file.
        
        Args:
            file_path: Path to the configuration file to import
            merge: If True, merge with existing configuration. If False, replace entirely.
            persist: If True, save the imported configuration to the main config file.
        """
        try:
            with open(file_path, 'r') as f:
                imported_config = json.load(f)
            
            if merge:
                # Merge with existing configuration
                self._deep_merge(self.config_data, imported_config)
            else:
                # Replace entire configuration
                self.config_data = imported_config
            
            # Clear cache
            self.config_cache.clear()
            
            # Persist to main config file if requested
            if persist:
                self.save_configuration()
            
            logger.info(f"Configuration imported from {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")
            raise
    
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Deep merge source dictionary into target dictionary."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value


# Global settings manager instance
settings_manager = SettingsManager()
