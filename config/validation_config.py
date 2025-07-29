"""
Validation Configuration Module

This module provides validation configuration settings and utilities
for the Django Pymetrics agentic framework.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union, Tuple


@dataclass
class ValidationRule:
    """
    A single validation rule configuration.
    """
    name: str
    description: str
    enabled: bool = True
    severity: str = 'error'  # 'error', 'warning', or 'info'
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled,
            'severity': self.severity,
            'parameters': self.parameters
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationRule':
        """Create rule from dictionary."""
        return cls(**data)


@dataclass
class ValidationConfig:
    """
    Validation configuration settings.
    
    This class holds validation rules and thresholds for data validation
    across the application.
    """
    # Data quality thresholds
    min_data_completeness: float = 95.0  # percentage
    max_null_percentage: float = 5.0  # percentage
    min_confidence_threshold: float = 0.7  # 0-1 scale
    
    # Validation rules
    rules: Dict[str, ValidationRule] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize with default rules if none provided."""
        if not self.rules:
            self.rules = {
                'required_fields': ValidationRule(
                    name='required_fields',
                    description='Check for required fields',
                    enabled=True,
                    severity='error'
                ),
                'data_type_validation': ValidationRule(
                    name='data_type_validation',
                    description='Validate data types',
                    enabled=True,
                    severity='error'
                ),
                'range_validation': ValidationRule(
                    name='range_validation',
                    description='Validate value ranges',
                    enabled=True,
                    severity='warning'
                ),
                'consistency_check': ValidationRule(
                    name='consistency_check',
                    description='Check data consistency',
                    enabled=True,
                    severity='warning'
                )
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'min_data_completeness': self.min_data_completeness,
            'max_null_percentage': self.max_null_percentage,
            'min_confidence_threshold': self.min_confidence_threshold,
            'rules': {k: v.to_dict() for k, v in self.rules.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationConfig':
        """Create configuration from dictionary."""
        rules_data = data.pop('rules', {})
        config = cls(**data)
        config.rules = {k: ValidationRule.from_dict(v) for k, v in rules_data.items()}
        return config
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add or update a validation rule."""
        self.rules[rule.name] = rule
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a validation rule by name."""
        if rule_name in self.rules:
            del self.rules[rule_name]
            return True
        return False
    
    def get_rule(self, rule_name: str) -> Optional[ValidationRule]:
        """Get a validation rule by name."""
        return self.rules.get(rule_name)
    
    def validate_configuration(self) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Validate the configuration itself.
        
        Returns:
            Tuple of (is_valid, errors_dict)
        """
        errors = {}
        
        if not (0 <= self.min_data_completeness <= 100):
            errors['min_data_completeness'] = ['Must be between 0 and 100']
            
        if not (0 <= self.max_null_percentage <= 100):
            errors['max_null_percentage'] = ['Must be between 0 and 100']
            
        if not (0 <= self.min_confidence_threshold <= 1):
            errors['min_confidence_threshold'] = ['Must be between 0 and 1']
        
        # Validate rules
        for rule_name, rule in self.rules.items():
            if not rule.name:
                errors.setdefault('rules', []).append(f'Rule name cannot be empty for rule: {rule_name}')
            if rule.severity not in ['error', 'warning', 'info']:
                errors.setdefault('rules', []).append(
                    f'Invalid severity "{rule.severity}" for rule: {rule_name}. Must be one of: error, warning, info'
                )
        
        return len(errors) == 0, errors
