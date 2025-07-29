"""
WebSocket Consumers for Django Pymetrics

This module provides WebSocket consumers for real-time data streaming,
including live event streaming, real-time trait updates, and interactive dashboards.
"""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from behavioral_data.models import BehavioralSession, BehavioralEvent
from ai_model.models import TraitProfile
from agents.event_logger import EventLogger
from agents.trait_inferencer import TraitInferencer

User = get_user_model()
logger = logging.getLogger(__name__)


class EventStreamConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time behavioral event streaming.
    
    Handles live streaming of behavioral events, session updates,
    and real-time metrics for interactive dashboards.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None
        self.session_id = None
    
    async def connect(self):
        """Handle WebSocket connection."""
        try:
            # Extract connection parameters
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'events_{self.room_name}'
            
            # Get user from scope
            if self.scope['user'].is_authenticated:
                self.user = self.scope['user']
            else:
                await self.close(code=4001)  # Unauthorized
                return
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'room_name': self.room_name,
                'timestamp': timezone.now().isoformat(),
                'message': 'Connected to event stream'
            }))
            
            logger.info(f"WebSocket connected: {self.user.username} to room {self.room_name}")
            
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            # Leave room group
            if self.room_group_name:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
            
            logger.info(f"WebSocket disconnected: {self.user.username if self.user else 'Unknown'}")
            
        except Exception as e:
            logger.error(f"WebSocket disconnection error: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'subscribe_session':
                await self.handle_session_subscription(data)
            elif message_type == 'request_events':
                await self.handle_event_request(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"WebSocket receive error: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_session_subscription(self, data):
        """Handle session subscription request."""
        session_id = data.get('session_id')
        
        if not session_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Session ID required'
            }))
            return
        
        # Validate session exists and user has access
        session = await self.get_session(session_id)
        if not session:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Session not found or access denied'
            }))
            return
        
        self.session_id = session_id
        
        # Send subscription confirmation
        await self.send(text_data=json.dumps({
            'type': 'session_subscribed',
            'session_id': session_id,
            'timestamp': timezone.now().isoformat()
        }))
        
        # Send initial session data
        await self.send_session_data(session)
    
    async def handle_event_request(self, data):
        """Handle event data request."""
        if not self.session_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'No session subscribed'
            }))
            return
        
        # Get recent events
        events = await self.get_recent_events(self.session_id, limit=50)
        
        await self.send(text_data=json.dumps({
            'type': 'events_data',
            'session_id': self.session_id,
            'events': events,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def event_update(self, event):
        """Handle event updates from channel layer."""
        try:
            # Send event to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'event_update',
                'session_id': event.get('session_id'),
                'event': event.get('event_data'),
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending event update: {str(e)}")
    
    async def trait_update(self, event):
        """Handle trait updates from channel layer."""
        try:
            # Send trait update to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'trait_update',
                'session_id': event.get('session_id'),
                'traits': event.get('trait_data'),
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending trait update: {str(e)}")
    
    async def metric_update(self, event):
        """Handle metric updates from channel layer."""
        try:
            # Send metric update to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'metric_update',
                'session_id': event.get('session_id'),
                'metrics': event.get('metric_data'),
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending metric update: {str(e)}")
    
    @database_sync_to_async
    def get_session(self, session_id):
        """Get session with user access validation."""
        try:
            return BehavioralSession.objects.get(
                session_id=session_id,
                user=self.user
            )
        except BehavioralSession.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_recent_events(self, session_id, limit=50):
        """Get recent events for a session."""
        try:
            events = BehavioralEvent.objects.filter(
                session__session_id=session_id
            ).order_by('-timestamp')[:limit]
            
            return [
                {
                    'id': str(event.id),
                    'event_type': event.event_type,
                    'event_name': event.event_name,
                    'timestamp': event.timestamp.isoformat(),
                    'event_data': event.event_data
                }
                for event in events
            ]
        except Exception as e:
            logger.error(f"Error getting recent events: {str(e)}")
            return []
    
    @database_sync_to_async
    def send_session_data(self, session):
        """Send initial session data."""
        try:
            # Get session summary
            session_data = {
                'session_id': session.session_id,
                'game_type': session.game_type,
                'status': session.status,
                'total_duration': session.total_duration,
                'total_games_played': session.total_games_played,
                'is_completed': session.is_completed,
                'started_at': session.started_at.isoformat() if session.started_at else None,
                'session_end_time': session.session_end_time.isoformat() if session.session_end_time else None
            }
            
            return session_data
        except Exception as e:
            logger.error(f"Error getting session data: {str(e)}")
            return {}


class TraitStreamConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time trait updates.
    
    Handles live streaming of trait inference results and
    psychometric assessment updates.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None
    
    async def connect(self):
        """Handle WebSocket connection."""
        try:
            # Extract connection parameters
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'traits_{self.room_name}'
            
            # Get user from scope
            if self.scope['user'].is_authenticated:
                self.user = self.scope['user']
            else:
                await self.close(code=4001)  # Unauthorized
                return
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'room_name': self.room_name,
                'timestamp': timezone.now().isoformat(),
                'message': 'Connected to trait stream'
            }))
            
            logger.info(f"Trait WebSocket connected: {self.user.username} to room {self.room_name}")
            
        except Exception as e:
            logger.error(f"Trait WebSocket connection error: {str(e)}")
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            # Leave room group
            if self.room_group_name:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
            
            logger.info(f"Trait WebSocket disconnected: {self.user.username if self.user else 'Unknown'}")
            
        except Exception as e:
            logger.error(f"Trait WebSocket disconnection error: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'request_traits':
                await self.handle_trait_request(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Trait WebSocket receive error: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_trait_request(self, data):
        """Handle trait data request."""
        session_id = data.get('session_id')
        
        if not session_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Session ID required'
            }))
            return
        
        # Get trait profile
        trait_profile = await self.get_trait_profile(session_id)
        
        if trait_profile:
            await self.send(text_data=json.dumps({
                'type': 'traits_data',
                'session_id': session_id,
                'traits': trait_profile,
                'timestamp': timezone.now().isoformat()
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'traits_data',
                'session_id': session_id,
                'traits': None,
                'message': 'No trait profile available',
                'timestamp': timezone.now().isoformat()
            }))
    
    async def trait_update(self, event):
        """Handle trait updates from channel layer."""
        try:
            # Send trait update to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'trait_update',
                'session_id': event.get('session_id'),
                'traits': event.get('trait_data'),
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending trait update: {str(e)}")
    
    @database_sync_to_async
    def get_trait_profile(self, session_id):
        """Get trait profile for a session."""
        try:
            trait_profile = TraitProfile.objects.filter(
                session__session_id=session_id,
                session__user=self.user
            ).first()
            
            if trait_profile:
                return {
                    'risk_tolerance': trait_profile.risk_tolerance,
                    'consistency': trait_profile.consistency,
                    'learning_ability': trait_profile.learning_ability,
                    'decision_speed': trait_profile.decision_speed,
                    'emotional_regulation': trait_profile.emotional_regulation,
                    'confidence_interval': trait_profile.confidence_interval,
                    'assessment_timestamp': trait_profile.assessment_timestamp.isoformat() if trait_profile.assessment_timestamp else None
                }
            return None
        except Exception as e:
            logger.error(f"Error getting trait profile: {str(e)}")
            return None


class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for interactive dashboard updates.
    
    Handles real-time dashboard updates including metrics,
    session progress, and system status.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None
    
    async def connect(self):
        """Handle WebSocket connection."""
        try:
            # Extract connection parameters
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'dashboard_{self.room_name}'
            
            # Get user from scope
            if self.scope['user'].is_authenticated:
                self.user = self.scope['user']
            else:
                await self.close(code=4001)  # Unauthorized
                return
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'room_name': self.room_name,
                'timestamp': timezone.now().isoformat(),
                'message': 'Connected to dashboard stream'
            }))
            
            logger.info(f"Dashboard WebSocket connected: {self.user.username} to room {self.room_name}")
            
        except Exception as e:
            logger.error(f"Dashboard WebSocket connection error: {str(e)}")
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            # Leave room group
            if self.room_group_name:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
            
            logger.info(f"Dashboard WebSocket disconnected: {self.user.username if self.user else 'Unknown'}")
            
        except Exception as e:
            logger.error(f"Dashboard WebSocket disconnection error: {str(e)}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'request_dashboard_data':
                await self.handle_dashboard_request(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Dashboard WebSocket receive error: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_dashboard_request(self, data):
        """Handle dashboard data request."""
        # Get dashboard data
        dashboard_data = await self.get_dashboard_data()
        
        await self.send(text_data=json.dumps({
            'type': 'dashboard_data',
            'data': dashboard_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def dashboard_update(self, event):
        """Handle dashboard updates from channel layer."""
        try:
            # Send dashboard update to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'dashboard_update',
                'data': event.get('dashboard_data'),
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending dashboard update: {str(e)}")
    
    @database_sync_to_async
    def get_dashboard_data(self):
        """Get dashboard data for the user."""
        try:
            # Get user's sessions
            sessions = BehavioralSession.objects.filter(user=self.user)
            
            # Get recent activity
            recent_sessions = sessions.order_by('-session_start_time')[:5]
            
            # Get system status
            system_status = {
                'total_sessions': sessions.count(),
                'completed_sessions': sessions.filter(is_completed=True).count(),
                'active_sessions': sessions.filter(status='in_progress').count(),
                'average_session_duration': sessions.aggregate(
                    avg_duration=models.Avg('total_duration')
                )['avg_duration'] or 0
            }
            
            return {
                'system_status': system_status,
                'recent_sessions': [
                    {
                        'session_id': session.session_id,
                        'game_type': session.game_type,
                        'status': session.status,
                        'started_at': session.started_at.isoformat() if session.started_at else None
                    }
                    for session in recent_sessions
                ]
            }
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
 