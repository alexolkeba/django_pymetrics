"""
Machine Learning Engine for Django Pymetrics

This module provides comprehensive ML capabilities including:
- Predictive analytics models
- Anomaly detection algorithms
- Adaptive trait mapping
- Model versioning and A/B testing
"""

import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import joblib
import os

from django.utils import timezone
from django.conf import settings
from behavioral_data.models import BehavioralSession, BehavioralEvent, BehavioralMetric
from ai_model.models import TraitProfile
from django.db import models

logger = logging.getLogger(__name__)


class PredictiveAnalyticsEngine:
    """
    Advanced predictive analytics engine for behavioral data.
    
    Provides capabilities for:
    - Trait prediction models
    - Behavioral pattern recognition
    - Performance forecasting
    - Anomaly detection
    """
    
    def __init__(self):
        """Initialize the predictive analytics engine."""
        self.models = {}
        self.scalers = {}
        self.model_versions = {}
        self.performance_metrics = {}
        
        # Model configuration
        self.model_config = {
            'trait_prediction': {
                'algorithm': 'random_forest',
                'features': ['session_duration', 'games_played', 'completion_rate'],
                'targets': ['risk_tolerance', 'consistency', 'learning_ability']
            },
            'anomaly_detection': {
                'algorithm': 'isolation_forest',
                'contamination': 0.1,
                'features': ['event_frequency', 'response_time', 'error_rate']
            },
            'performance_forecasting': {
                'algorithm': 'linear_regression',
                'features': ['historical_performance', 'session_count', 'improvement_rate']
            }
        }
        
        # Initialize model storage
        self.model_storage_path = getattr(settings, 'ML_MODEL_STORAGE_PATH', 'ml_models/')
        os.makedirs(self.model_storage_path, exist_ok=True)
    
    def train_trait_prediction_model(self, user_id: str = None) -> Dict[str, Any]:
        """
        Train trait prediction model using behavioral data.
        
        Args:
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Training results and model performance
        """
        try:
            logger.info(f"Training trait prediction model for user: {user_id}")
            
            # Prepare training data
            X, y = self._prepare_trait_training_data(user_id)
            
            if len(X) < 10:  # Minimum data requirement
                return {
                    'success': False,
                    'error': 'Insufficient training data',
                    'data_points': len(X)
                }
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2_score = model.score(X_test_scaled, y_test)
            
            # Store model and scaler
            model_name = f'trait_prediction_{user_id}' if user_id else 'trait_prediction_global'
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            
            # Save model
            self._save_model(model_name, model, scaler)
            
            # Update performance metrics
            self.performance_metrics[model_name] = {
                'mse': mse,
                'r2_score': r2_score,
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'last_trained': timezone.now().isoformat()
            }
            
            logger.info(f"Trait prediction model trained successfully. R²: {r2_score:.3f}")
            
            return {
                'success': True,
                'model_name': model_name,
                'performance': {
                    'mse': mse,
                    'r2_score': r2_score,
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                },
                'last_trained': timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training trait prediction model: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def train_anomaly_detection_model(self, user_id: str = None) -> Dict[str, Any]:
        """
        Train anomaly detection model for behavioral patterns.
        
        Args:
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Training results and model performance
        """
        try:
            logger.info(f"Training anomaly detection model for user: {user_id}")
            
            # Prepare training data
            X = self._prepare_anomaly_training_data(user_id)
            
            if len(X) < 20:  # Minimum data requirement
                return {
                    'success': False,
                    'error': 'Insufficient training data',
                    'data_points': len(X)
                }
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
            
            model.fit(X_scaled)
            
            # Evaluate model (anomaly detection is unsupervised)
            anomaly_scores = model.decision_function(X_scaled)
            anomaly_rate = np.mean(model.predict(X_scaled) == -1)
            
            # Store model and scaler
            model_name = f'anomaly_detection_{user_id}' if user_id else 'anomaly_detection_global'
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            
            # Save model
            self._save_model(model_name, model, scaler)
            
            # Update performance metrics
            self.performance_metrics[model_name] = {
                'anomaly_rate': anomaly_rate,
                'avg_anomaly_score': np.mean(anomaly_scores),
                'training_samples': len(X),
                'last_trained': timezone.now().isoformat()
            }
            
            logger.info(f"Anomaly detection model trained successfully. Anomaly rate: {anomaly_rate:.3f}")
            
            return {
                'success': True,
                'model_name': model_name,
                'performance': {
                    'anomaly_rate': anomaly_rate,
                    'avg_anomaly_score': float(np.mean(anomaly_scores)),
                    'training_samples': len(X)
                },
                'last_trained': timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training anomaly detection model: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def train_performance_forecasting_model(self, user_id: str = None) -> Dict[str, Any]:
        """
        Train performance forecasting model.
        
        Args:
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Training results and model performance
        """
        try:
            logger.info(f"Training performance forecasting model for user: {user_id}")
            
            # Prepare training data
            X, y = self._prepare_performance_training_data(user_id)
            
            if len(X) < 10:  # Minimum data requirement
                return {
                    'success': False,
                    'error': 'Insufficient training data',
                    'data_points': len(X)
                }
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = LinearRegression()
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2_score = model.score(X_test_scaled, y_test)
            
            # Store model and scaler
            model_name = f'performance_forecasting_{user_id}' if user_id else 'performance_forecasting_global'
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            
            # Save model
            self._save_model(model_name, model, scaler)
            
            # Update performance metrics
            self.performance_metrics[model_name] = {
                'mse': mse,
                'r2_score': r2_score,
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'last_trained': timezone.now().isoformat()
            }
            
            logger.info(f"Performance forecasting model trained successfully. R²: {r2_score:.3f}")
            
            return {
                'success': True,
                'model_name': model_name,
                'performance': {
                    'mse': mse,
                    'r2_score': r2_score,
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                },
                'last_trained': timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training performance forecasting model: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_traits(self, session_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Predict traits based on behavioral session data.
        
        Args:
            session_data: Behavioral session features
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Predicted traits with confidence scores
        """
        try:
            model_name = f'trait_prediction_{user_id}' if user_id else 'trait_prediction_global'
            
            if model_name not in self.models:
                # Load model if not in memory
                self._load_model(model_name)
            
            if model_name not in self.models:
                return {
                    'success': False,
                    'error': 'Model not available'
                }
            
            # Prepare features
            features = self._extract_trait_features(session_data)
            features_scaled = self.scalers[model_name].transform([features])
            
            # Make prediction
            predictions = self.models[model_name].predict(features_scaled)[0]
            
            # Calculate confidence (using model's feature importance)
            confidence = self._calculate_prediction_confidence(model_name, features_scaled)
            
            return {
                'success': True,
                'predictions': {
                    'risk_tolerance': float(predictions[0]),
                    'consistency': float(predictions[1]),
                    'learning_ability': float(predictions[2])
                },
                'confidence': confidence,
                'model_name': model_name
            }
            
        except Exception as e:
            logger.error(f"Error predicting traits: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def detect_anomalies(self, behavioral_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Detect anomalies in behavioral patterns.
        
        Args:
            behavioral_data: Behavioral event data
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Anomaly detection results
        """
        try:
            model_name = f'anomaly_detection_{user_id}' if user_id else 'anomaly_detection_global'
            
            if model_name not in self.models:
                # Load model if not in memory
                self._load_model(model_name)
            
            if model_name not in self.models:
                return {
                    'success': False,
                    'error': 'Model not available'
                }
            
            # Prepare features
            features = self._extract_anomaly_features(behavioral_data)
            features_scaled = self.scalers[model_name].transform([features])
            
            # Make prediction
            anomaly_score = self.models[model_name].decision_function(features_scaled)[0]
            is_anomaly = self.models[model_name].predict(features_scaled)[0] == -1
            
            return {
                'success': True,
                'anomaly_detected': bool(is_anomaly),
                'anomaly_score': float(anomaly_score),
                'severity': self._calculate_anomaly_severity(anomaly_score),
                'model_name': model_name
            }
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def forecast_performance(self, historical_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Forecast future performance based on historical data.
        
        Args:
            historical_data: Historical performance data
            user_id: Optional user ID for user-specific model
            
        Returns:
            Dict: Performance forecast
        """
        try:
            model_name = f'performance_forecasting_{user_id}' if user_id else 'performance_forecasting_global'
            
            if model_name not in self.models:
                # Load model if not in memory
                self._load_model(model_name)
            
            if model_name not in self.models:
                return {
                    'success': False,
                    'error': 'Model not available'
                }
            
            # Prepare features
            features = self._extract_performance_features(historical_data)
            features_scaled = self.scalers[model_name].transform([features])
            
            # Make prediction
            forecast = self.models[model_name].predict(features_scaled)[0]
            
            return {
                'success': True,
                'forecast': float(forecast),
                'confidence': self._calculate_forecast_confidence(model_name, features_scaled),
                'model_name': model_name
            }
            
        except Exception as e:
            logger.error(f"Error forecasting performance: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_trait_training_data(self, user_id: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for trait prediction."""
        try:
            # Get sessions with trait profiles
            if user_id:
                sessions = BehavioralSession.objects.filter(
                    user_id=user_id,
                    is_completed=True
                )
            else:
                sessions = BehavioralSession.objects.filter(is_completed=True)
            
            # Get trait profiles
            trait_profiles = TraitProfile.objects.filter(
                session__in=sessions
            ).select_related('session')
            
            X = []
            y = []
            
            for profile in trait_profiles:
                session = profile.session
                
                # Extract features
                features = [
                    session.total_duration / 1000,  # Duration in seconds
                    session.total_games_played,
                    session.total_games_played / max(session.total_duration / 1000, 1),  # Games per second
                    1.0 if session.is_completed else 0.0,  # Completion status
                ]
                
                # Extract targets
                targets = [
                    profile.risk_tolerance or 0.5,
                    profile.consistency or 0.5,
                    profile.learning_ability or 0.5
                ]
                
                X.append(features)
                y.append(targets)
            
            return np.array(X), np.array(y)
            
        except Exception as e:
            logger.error(f"Error preparing trait training data: {str(e)}")
            return np.array([]), np.array([])
    
    def _prepare_anomaly_training_data(self, user_id: str = None) -> np.ndarray:
        """Prepare training data for anomaly detection."""
        try:
            # Get behavioral events
            if user_id:
                events = BehavioralEvent.objects.filter(
                    session__user_id=user_id
                )
            else:
                events = BehavioralEvent.objects.all()
            
            # Aggregate event features
            event_features = []
            
            for session in events.values('session').distinct():
                session_events = events.filter(session=session['session'])
                
                features = [
                    session_events.count(),  # Event count
                    session_events.filter(event_type='user_action').count(),  # User actions
                    session_events.filter(event_type='system_event').count(),  # System events
                    session_events.aggregate(avg_timestamp=models.Avg('timestamp_milliseconds'))['avg_timestamp'] or 0,
                ]
                
                event_features.append(features)
            
            return np.array(event_features)
            
        except Exception as e:
            logger.error(f"Error preparing anomaly training data: {str(e)}")
            return np.array([])
    
    def _prepare_performance_training_data(self, user_id: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for performance forecasting."""
        try:
            # Get historical performance data
            if user_id:
                sessions = BehavioralSession.objects.filter(
                    user_id=user_id,
                    is_completed=True
                ).order_by('session_start_time')
            else:
                sessions = BehavioralSession.objects.filter(
                    is_completed=True
                ).order_by('session_start_time')
            
            X = []
            y = []
            
            for i, session in enumerate(sessions):
                if i < 5:  # Need at least 5 sessions for features
                    continue
                
                # Get previous sessions for features
                prev_sessions = sessions[i-5:i]
                
                features = [
                    prev_sessions.aggregate(avg_duration=models.Avg('total_duration'))['avg_duration'] or 0,
                    prev_sessions.count(),
                    prev_sessions.filter(is_completed=True).count() / max(prev_sessions.count(), 1),
                    (session.session_start_time - prev_sessions.first().session_start_time).total_seconds() / 3600,  # Hours since first session
                ]
                
                # Target: current session performance
                target = session.total_duration / 1000  # Duration in seconds
                
                X.append(features)
                y.append(target)
            
            return np.array(X), np.array(y)
            
        except Exception as e:
            logger.error(f"Error preparing performance training data: {str(e)}")
            return np.array([]), np.array([])
    
    def _extract_trait_features(self, session_data: Dict[str, Any]) -> List[float]:
        """Extract features for trait prediction."""
        return [
            session_data.get('total_duration', 0) / 1000,
            session_data.get('total_games_played', 0),
            session_data.get('total_games_played', 0) / max(session_data.get('total_duration', 0) / 1000, 1),
            1.0 if session_data.get('is_completed', False) else 0.0,
        ]
    
    def _extract_anomaly_features(self, behavioral_data: Dict[str, Any]) -> List[float]:
        """Extract features for anomaly detection."""
        return [
            behavioral_data.get('event_count', 0),
            behavioral_data.get('user_action_count', 0),
            behavioral_data.get('system_event_count', 0),
            behavioral_data.get('avg_timestamp', 0),
        ]
    
    def _extract_performance_features(self, historical_data: Dict[str, Any]) -> List[float]:
        """Extract features for performance forecasting."""
        return [
            historical_data.get('avg_duration', 0),
            historical_data.get('session_count', 0),
            historical_data.get('completion_rate', 0),
            historical_data.get('hours_since_first', 0),
        ]
    
    def _calculate_prediction_confidence(self, model_name: str, features: np.ndarray) -> float:
        """Calculate prediction confidence."""
        try:
            # Use model's feature importance or R² score as confidence
            if hasattr(self.models[model_name], 'feature_importances_'):
                importance = np.mean(self.models[model_name].feature_importances_)
                return min(1.0, max(0.0, importance))
            else:
                # Use performance metrics
                return self.performance_metrics.get(model_name, {}).get('r2_score', 0.5)
        except Exception:
            return 0.5
    
    def _calculate_anomaly_severity(self, anomaly_score: float) -> str:
        """Calculate anomaly severity level."""
        if anomaly_score < -0.5:
            return 'high'
        elif anomaly_score < -0.2:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_forecast_confidence(self, model_name: str, features: np.ndarray) -> float:
        """Calculate forecast confidence."""
        try:
            # Use model's R² score as confidence
            return self.performance_metrics.get(model_name, {}).get('r2_score', 0.5)
        except Exception:
            return 0.5
    
    def _save_model(self, model_name: str, model, scaler):
        """Save model and scaler to disk."""
        try:
            model_path = os.path.join(self.model_storage_path, f'{model_name}.joblib')
            scaler_path = os.path.join(self.model_storage_path, f'{model_name}_scaler.joblib')
            
            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)
            
            logger.info(f"Model saved: {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def _load_model(self, model_name: str):
        """Load model and scaler from disk."""
        try:
            model_path = os.path.join(self.model_storage_path, f'{model_name}.joblib')
            scaler_path = os.path.join(self.model_storage_path, f'{model_name}_scaler.joblib')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)
                
                self.models[model_name] = model
                self.scalers[model_name] = scaler
                
                logger.info(f"Model loaded: {model_path}")
            else:
                logger.warning(f"Model files not found: {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
    
    def get_model_performance(self, model_name: str = None) -> Dict[str, Any]:
        """Get performance metrics for models."""
        if model_name:
            return self.performance_metrics.get(model_name, {})
        else:
            return self.performance_metrics
    
    def retrain_all_models(self, user_id: str = None) -> Dict[str, Any]:
        """Retrain all models with latest data."""
        results = {}
        
        # Train trait prediction model
        results['trait_prediction'] = self.train_trait_prediction_model(user_id)
        
        # Train anomaly detection model
        results['anomaly_detection'] = self.train_anomaly_detection_model(user_id)
        
        # Train performance forecasting model
        results['performance_forecasting'] = self.train_performance_forecasting_model(user_id)
        
        return results 