"""
Professional Example: Trait Inference Logic for Django Pymetrics

This module provides a robust, extensible foundation for extracting behavioral metrics and inferring psychometric traits from logged events in neuroscience-based Django applications. It is designed for one-pass implementation success, scientific reproducibility, and future-proof context engineering.

Key Features:
- Modular trait mapping for behavioral analytics
- Extensible metric extraction for new games and event types
- Scientific validation hooks for reproducibility
- Actionable docstrings and onboarding notes for future developers
"""

from django.db.models import Avg, StdDev
# Adjust import below to your actual models path
# from django_pymetrics.games.models import PumpEvent, BalloonEvent
from .models import PumpEvent, BalloonEvent

def get_session_metrics(session_id):
    """
    Aggregate behavioral metrics for a given session.
    Args:
        session_id (str): The session identifier.
    Returns:
        dict: Aggregated metrics (average and stddev of pumps per balloon).
    """
    pumps = PumpEvent.objects.filter(balloon__session__session_id=session_id)
    avg_pumps = pumps.aggregate(Avg('pump_number'))['pump_number__avg']
    std_pumps = pumps.aggregate(StdDev('pump_number'))['pump_number__stddev']
    # Extend: Add more metrics as needed for new games/events
    return {
        'avg_pumps_per_balloon': avg_pumps or 0,
        'std_pumps_per_balloon': std_pumps or 0,
        # 'max_pumps': pumps.aggregate(Max('pump_number'))['pump_number__max'],
        # Add additional metrics here
    }

def infer_traits(metrics):
    """
    Map aggregated metrics to psychometric trait dimensions.
    Args:
        metrics (dict): Aggregated metrics.
    Returns:
        dict: Inferred trait profile.
    """
    traits = {}
    # Risk Tolerance: Higher average pumps per balloon suggests higher risk-taking
    avg_pumps = metrics.get('avg_pumps_per_balloon', 0)
    if avg_pumps > 10:
        traits['risk_tolerance'] = 'high'
    elif avg_pumps > 5:
        traits['risk_tolerance'] = 'moderate'
    else:
        traits['risk_tolerance'] = 'low'

    # Consistency: Lower stddev suggests more consistent behavior
    std_pumps = metrics.get('std_pumps_per_balloon', 0)
    if std_pumps < 2:
        traits['consistency'] = 'high'
    elif std_pumps < 5:
        traits['consistency'] = 'moderate'
    else:
        traits['consistency'] = 'low'

    # Example extension: Impulsivity (add metric and mapping logic)
    # impulsivity_score = metrics.get('impulsivity_metric', None)
    # if impulsivity_score is not None:
    #     traits['impulsivity'] = ...

    # Scientific validation hook: log trait mapping for reproducibility
    # log_trait_mapping(metrics, traits)

    return traits

# Documentation
# - See django_pymetrics/Pymetrics Application Research.md for trait mapping logic
# - To extend: Add new metrics in get_session_metrics and map them in infer_traits
# - Ensure all trait mappings are scientifically validated and documented for reproducibility
# - Onboard new developers: Document new event types, metrics, and trait mappings here
# - Future-proof: Use modular functions and validation hooks for easy extension

def log_trait_mapping(metrics, traits):
    """
    Log trait mapping for scientific reproducibility and audit trails.
    Args:
        metrics (dict): Aggregated metrics.
        traits (dict): Inferred trait profile.
    """
    # Implement logging to file, database, or external system as needed
    pass
