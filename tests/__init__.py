"""
Comprehensive Test Suite for Django Pymetrics Agentic Framework

This test suite provides comprehensive coverage for all components of the
Django Pymetrics framework including agents, trait mapping, configuration,
and API endpoints.
"""

import os
import django
from django.test import TestCase
from django.conf import settings

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')
    django.setup()

__all__ = [
    'TestCase'
]
