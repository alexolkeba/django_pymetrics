"""
WebSocket Routing Configuration for Django Pymetrics

This module defines the routing configuration for WebSocket connections,
including event streams, trait updates, and dashboard data.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Event stream WebSocket
    re_path(
        r'ws/events/(?P<room_name>\w+)/$',
        consumers.EventStreamConsumer.as_asgi()
    ),
    
    # Trait stream WebSocket
    re_path(
        r'ws/traits/(?P<room_name>\w+)/$',
        consumers.TraitStreamConsumer.as_asgi()
    ),
    
    # Dashboard WebSocket
    re_path(
        r'ws/dashboard/(?P<room_name>\w+)/$',
        consumers.DashboardConsumer.as_asgi()
    ),
] 