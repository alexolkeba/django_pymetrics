"""
Trait Mapping Module for Django Pymetrics

This module contains the scientific logic for mapping behavioral metrics
to psychometric traits. It implements the core algorithms for trait inference
based on documented scientific research and Pymetrics methodologies.
"""

# Import these lazily to avoid circular imports
__all__ = [
    'TraitMapper',
    'ScientificTraitModel', 
    'TraitValidation'
]
