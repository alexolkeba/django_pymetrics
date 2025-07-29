"""
Celery Configuration for Django Pymetrics

This module configures Celery for background task processing of behavioral data,
metric extraction, and trait inference.
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')

app = Celery('pymetric')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery configuration."""
    print(f'Request: {self.request!r}')


# Configure Celery Beat schedule (simplified for now)
app.conf.beat_schedule = {
    'process-pending-events': {
        'task': 'tasks.event_processing.process_pending_events',
        'schedule': 60.0,  # Every minute
    },
}

# Configure task routes (simplified for now)
app.conf.task_routes = {
    'tasks.event_processing.*': {'queue': 'events'},
}

# Configure task serialization
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Configure result backend
app.conf.result_backend = 'redis://localhost:6379/0'

# Configure task execution
app.conf.task_always_eager = False  # Set to True for testing
app.conf.task_eager_propagates = True

# Configure worker settings
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_max_tasks_per_child = 1000
app.conf.worker_disable_rate_limits = False

# Configure task timeouts
app.conf.task_soft_time_limit = 300  # 5 minutes
app.conf.task_time_limit = 600  # 10 minutes

# Configure retry settings
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

# Configure monitoring
app.conf.worker_send_task_events = True
app.conf.task_send_sent_event = True 