"""
Deployment Configuration Module

This module provides deployment-specific configuration settings and utilities
for the Django Pymetrics agentic framework.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class DeploymentConfig:
    """
    Deployment configuration settings.
    
    This class holds deployment-specific configuration including environment settings,
    feature flags, and other deployment-related parameters.
    """
    environment: str = 'development'
    debug: bool = False
    allowed_hosts: List[str] = field(default_factory=lambda: ['localhost', '127.0.0.1'])
    cors_allowed_origins: List[str] = field(default_factory=list)
    
    # Feature flags
    enable_maintenance_mode: bool = False
    enable_rate_limiting: bool = True
    enable_analytics: bool = False
    
    # Performance settings
    cache_timeout: int = 300  # seconds
    database_pool_size: int = 5
    
    # Logging and monitoring
    log_level: str = 'INFO'
    enable_sentry: bool = False
    sentry_dsn: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'environment': self.environment,
            'debug': self.debug,
            'allowed_hosts': self.allowed_hosts,
            'cors_allowed_origins': self.cors_allowed_origins,
            'enable_maintenance_mode': self.enable_maintenance_mode,
            'enable_rate_limiting': self.enable_rate_limiting,
            'enable_analytics': self.enable_analytics,
            'cache_timeout': self.cache_timeout,
            'database_pool_size': self.database_pool_size,
            'log_level': self.log_level,
            'enable_sentry': self.enable_sentry,
            'sentry_dsn': self.sentry_dsn
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeploymentConfig':
        """Create configuration from dictionary."""
        return cls(**data)
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def validate(self) -> Dict[str, List[str]]:
        """
        Validate configuration values.
        
        Returns:
            Dictionary with validation errors (empty if valid)
        """
        errors = {}
        
        if self.environment not in ['development', 'staging', 'production']:
            errors['environment'] = ["Must be one of: 'development', 'staging', 'production'"]
        
        if self.log_level.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            errors['log_level'] = ["Invalid log level. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"]
        
        if self.enable_sentry and not self.sentry_dsn:
            errors['sentry_dsn'] = ["Sentry DSN is required when Sentry is enabled"]
        
        if self.database_pool_size < 1 or self.database_pool_size > 100:
            errors['database_pool_size'] = ["Must be between 1 and 100"]
        
        return errors
