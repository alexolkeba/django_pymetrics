"""
Behavioral Data Validators for Django Pymetrics

This module provides validators for ensuring data integrity and scientific validity
of behavioral data collection and processing.
"""

from django.core.exceptions import ValidationError
from django.utils import timezone
from typing import Dict, Any, List, Optional
import re
import uuid


class BehavioralDataValidator:
    """
    Base validator class for behavioral data validation.
    
    Provides common validation methods and error handling for all behavioral data types.
    """
    
    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """
        Validate UUID format.
        
        Args:
            uuid_string: UUID string to validate
            
        Returns:
            bool: True if valid UUID
        """
        try:
            uuid.UUID(uuid_string)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_timestamp_range(timestamp: timezone.datetime, 
                               min_age_hours: int = 0, 
                               max_age_hours: int = 24) -> bool:
        """
        Validate timestamp is within acceptable range.
        
        Args:
            timestamp: Timestamp to validate
            min_age_hours: Minimum age in hours (default: 0)
            max_age_hours: Maximum age in hours (default: 24)
            
        Returns:
            bool: True if timestamp is within range
        """
        now = timezone.now()
        min_time = now - timezone.timedelta(hours=max_age_hours)
        max_time = now + timezone.timedelta(hours=1)  # Allow slight future timestamps
        
        return min_time <= timestamp <= max_time
    
    @staticmethod
    def validate_numeric_range(value: float, min_value: float, max_value: float) -> bool:
        """
        Validate numeric value is within range.
        
        Args:
            value: Numeric value to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            bool: True if value is within range
        """
        return min_value <= value <= max_value
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """
        Sanitize string value for database storage.
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized string
        """
        if not isinstance(value, str):
            raise ValidationError("Value must be a string")
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', value.strip())
        
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized


class BalloonRiskValidator(BehavioralDataValidator):
    """
    Validator for Balloon Risk Game behavioral data.
    
    Ensures data integrity and scientific validity for balloon risk game events.
    """
    
    @staticmethod
    def validate_pump_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate pump event data.
        
        Args:
            data: Pump event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValidationError: If data is invalid
        """
        errors = []
        
        # Validate required fields
        required_fields = ['balloon_id', 'pump_number', 'timestamp', 'timestamp_milliseconds']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError(errors)
        
        # Validate balloon_id
        if not isinstance(data['balloon_id'], str) or len(data['balloon_id']) > 64:
            errors.append("balloon_id must be string with max length 64")
        
        # Validate pump_number
        if not isinstance(data['pump_number'], int) or data['pump_number'] < 0:
            errors.append("pump_number must be non-negative integer")
        
        # Validate timestamp_milliseconds
        if not isinstance(data['timestamp_milliseconds'], int) or data['timestamp_milliseconds'] < 0:
            errors.append("timestamp_milliseconds must be non-negative integer")
        
        # Validate optional numeric fields
        numeric_fields = ['balloon_size', 'current_earnings', 'total_earnings', 'time_since_prev_pump']
        for field in numeric_fields:
            if field in data:
                if not isinstance(data[field], (int, float)) or data[field] < 0:
                    errors.append(f"{field} must be non-negative number")
        
        # Validate boolean fields
        boolean_fields = ['is_new_personal_max', 'is_rapid_pump']
        for field in boolean_fields:
            if field in data and not isinstance(data[field], bool):
                errors.append(f"{field} must be boolean")
        
        if errors:
            raise ValidationError(errors)
        
        return data
    
    @staticmethod
    def validate_balloon_outcome(outcome: str) -> bool:
        """
        Validate balloon outcome value.
        
        Args:
            outcome: Outcome string to validate
            
        Returns:
            bool: True if valid outcome
        """
        valid_outcomes = ['popped', 'cashed', 'ongoing']
        return outcome in valid_outcomes
    
    @staticmethod
    def validate_earnings_consistency(balloon_events: List[Dict[str, Any]]) -> bool:
        """
        Validate earnings consistency across balloon events.
        
        Args:
            balloon_events: List of balloon events for a session
            
        Returns:
            bool: True if earnings are consistent
        """
        total_earnings = 0
        
        for event in balloon_events:
            if event.get('event_type') == 'cash_out':
                earnings = event.get('earnings_collected', 0)
                if earnings < 0:
                    return False
                total_earnings += earnings
            elif event.get('event_type') == 'pop':
                # No earnings lost on pop in this model
                pass
        
        return total_earnings >= 0


class MemoryCardsValidator(BehavioralDataValidator):
    """
    Validator for Memory Cards Game behavioral data.
    
    Ensures data integrity and scientific validity for memory cards game events.
    """
    
    @staticmethod
    def validate_card_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate card event data.
        
        Args:
            data: Card event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValidationError: If data is invalid
        """
        errors = []
        
        # Validate required fields
        required_fields = ['card_id', 'card_position', 'timestamp', 'timestamp_milliseconds']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError(errors)
        
        # Validate card_id
        if not isinstance(data['card_id'], str) or len(data['card_id']) > 64:
            errors.append("card_id must be string with max length 64")
        
        # Validate card_position
        if not isinstance(data['card_position'], int) or data['card_position'] < 0:
            errors.append("card_position must be non-negative integer")
        
        # Validate timestamp_milliseconds
        if not isinstance(data['timestamp_milliseconds'], int) or data['timestamp_milliseconds'] < 0:
            errors.append("timestamp_milliseconds must be non-negative integer")
        
        # Validate optional numeric fields
        numeric_fields = ['reaction_time', 'round_number', 'cards_flipped', 'matches_found']
        for field in numeric_fields:
            if field in data:
                if not isinstance(data[field], (int, float)) or data[field] < 0:
                    errors.append(f"{field} must be non-negative number")
        
        # Validate memory_accuracy
        if 'memory_accuracy' in data:
            accuracy = data['memory_accuracy']
            if not isinstance(accuracy, (int, float)) or accuracy < 0 or accuracy > 100:
                errors.append("memory_accuracy must be between 0 and 100")
        
        if errors:
            raise ValidationError(errors)
        
        return data
    
    @staticmethod
    def validate_match_consistency(match_events: List[Dict[str, Any]]) -> bool:
        """
        Validate match consistency across memory cards events.
        
        Args:
            match_events: List of match events for a session
            
        Returns:
            bool: True if matches are consistent
        """
        total_matches = 0
        total_attempts = 0
        
        for event in match_events:
            if event.get('event_type') == 'card_match':
                total_matches += 1
                total_attempts += 1
            elif event.get('event_type') == 'card_mismatch':
                total_attempts += 1
        
        # Validate that matches don't exceed reasonable bounds
        if total_attempts > 0:
            match_rate = total_matches / total_attempts
            return 0 <= match_rate <= 1
        
        return True


class ReactionTimerValidator(BehavioralDataValidator):
    """
    Validator for Reaction Timer Game behavioral data.
    
    Ensures data integrity and scientific validity for reaction timer game events.
    """
    
    @staticmethod
    def validate_trial_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate trial event data.
        
        Args:
            data: Trial event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValidationError: If data is invalid
        """
        errors = []
        
        # Validate required fields
        required_fields = ['trial_number', 'timestamp', 'timestamp_milliseconds']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError(errors)
        
        # Validate trial_number
        if not isinstance(data['trial_number'], int) or data['trial_number'] < 0:
            errors.append("trial_number must be non-negative integer")
        
        # Validate timestamp_milliseconds
        if not isinstance(data['timestamp_milliseconds'], int) or data['timestamp_milliseconds'] < 0:
            errors.append("timestamp_milliseconds must be non-negative integer")
        
        # Validate optional numeric fields
        numeric_fields = ['block_number', 'stimulus_time', 'response_time']
        for field in numeric_fields:
            if field in data:
                if not isinstance(data[field], (int, float)) or data[field] < 0:
                    errors.append(f"{field} must be non-negative number")
        
        # Validate boolean fields
        boolean_fields = ['is_correct']
        for field in boolean_fields:
            if field in data and not isinstance(data[field], bool):
                errors.append(f"{field} must be boolean")
        
        # Validate accuracy
        if 'accuracy' in data:
            accuracy = data['accuracy']
            if not isinstance(accuracy, (int, float)) or accuracy < 0 or accuracy > 100:
                errors.append("accuracy must be between 0 and 100")
        
        if errors:
            raise ValidationError(errors)
        
        return data
    
    @staticmethod
    def validate_response_time_range(response_time: float) -> bool:
        """
        Validate response time is within reasonable range.
        
        Args:
            response_time: Response time in milliseconds
            
        Returns:
            bool: True if response time is reasonable
        """
        # Typical human response times: 100ms to 5000ms
        return 100 <= response_time <= 5000
    
    @staticmethod
    def validate_accuracy_consistency(trial_events: List[Dict[str, Any]]) -> bool:
        """
        Validate accuracy consistency across trial events.
        
        Args:
            trial_events: List of trial events for a session
            
        Returns:
            bool: True if accuracy is consistent
        """
        correct_responses = 0
        total_responses = 0
        
        for event in trial_events:
            if event.get('event_type') == 'user_response':
                total_responses += 1
                if event.get('is_correct', False):
                    correct_responses += 1
        
        # Validate that accuracy doesn't exceed reasonable bounds
        if total_responses > 0:
            accuracy = correct_responses / total_responses
            return 0 <= accuracy <= 1
        
        return True


class SessionValidator(BehavioralDataValidator):
    """
    Validator for behavioral session data.
    
    Ensures data integrity and scientific validity for session-level data.
    """
    
    @staticmethod
    def validate_session_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate session data.
        
        Args:
            data: Session data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValidationError: If data is invalid
        """
        errors = []
        
        # Validate required fields
        required_fields = ['session_id', 'device_info', 'timestamp', 'timestamp_milliseconds']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            raise ValidationError(errors)
        
        # Validate session_id
        if not isinstance(data['session_id'], str) or len(data['session_id']) > 64:
            errors.append("session_id must be string with max length 64")
        
        # Validate device_info
        if not isinstance(data['device_info'], dict):
            errors.append("device_info must be dictionary")
        
        # Validate timestamp_milliseconds
        if not isinstance(data['timestamp_milliseconds'], int) or data['timestamp_milliseconds'] < 0:
            errors.append("timestamp_milliseconds must be non-negative integer")
        
        # Validate optional numeric fields
        numeric_fields = ['total_duration', 'total_games_played']
        for field in numeric_fields:
            if field in data:
                if not isinstance(data[field], (int, float)) or data[field] < 0:
                    errors.append(f"{field} must be non-negative number")
        
        # Validate boolean fields
        boolean_fields = ['is_completed', 'data_anonymized', 'consent_given']
        for field in boolean_fields:
            if field in data and not isinstance(data[field], bool):
                errors.append(f"{field} must be boolean")
        
        if errors:
            raise ValidationError(errors)
        
        return data
    
    @staticmethod
    def validate_session_duration(duration: int) -> bool:
        """
        Validate session duration is reasonable.
        
        Args:
            duration: Session duration in milliseconds
            
        Returns:
            bool: True if duration is reasonable
        """
        # Typical session duration: 5 minutes to 2 hours
        min_duration = 5 * 60 * 1000  # 5 minutes
        max_duration = 2 * 60 * 60 * 1000  # 2 hours
        
        return min_duration <= duration <= max_duration
    
    @staticmethod
    def validate_device_info(device_info: Dict[str, Any]) -> bool:
        """
        Validate device information structure.
        
        Args:
            device_info: Device information dictionary
            
        Returns:
            bool: True if device info is valid
        """
        required_fields = ['user_agent', 'screen_resolution']
        
        for field in required_fields:
            if field not in device_info:
                return False
        
        return True 