"""
Behavioral Data Schemas for Django Pymetrics

This module defines JSON schemas for behavioral data validation and serialization.
All schemas are designed for scientific reproducibility and data integrity.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class BehavioralDataSchema:
    """
    Base schema class for behavioral data validation.
    
    Provides common validation methods and schema definitions
    for all behavioral data types.
    """
    
    @staticmethod
    def validate_timestamp(timestamp: str) -> bool:
        """
        Validate timestamp format and precision.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            bool: True if valid timestamp
        """
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_milliseconds(milliseconds: int) -> bool:
        """
        Validate millisecond precision timestamp.
        
        Args:
            milliseconds: Millisecond timestamp
            
        Returns:
            bool: True if valid millisecond timestamp
        """
        return isinstance(milliseconds, int) and milliseconds >= 0
    
    @staticmethod
    def validate_json_data(data: Dict[str, Any]) -> bool:
        """
        Validate JSON data structure.
        
        Args:
            data: JSON data dictionary
            
        Returns:
            bool: True if valid JSON structure
        """
        try:
            json.dumps(data)
            return True
        except (TypeError, ValueError):
            return False


class BalloonRiskSchema(BehavioralDataSchema):
    """
    Schema for Balloon Risk Game behavioral data.
    
    Validates all balloon risk game events according to scientific standards.
    """
    
    @staticmethod
    def validate_pump_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate pump event data structure.
        
        Args:
            data: Pump event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['balloon_id', 'pump_number', 'timestamp_milliseconds']
        optional_fields = ['timestamp', 'balloon_color', 'balloon_size', 'current_earnings', 'total_earnings',
                          'time_since_prev_pump', 'is_new_personal_max', 'is_rapid_pump']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['balloon_id'], str):
            raise ValueError("balloon_id must be string")
        
        if not isinstance(data['pump_number'], int) or data['pump_number'] < 0:
            raise ValueError("pump_number must be non-negative integer")
        
        if not BalloonRiskSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Handle timestamp - generate from milliseconds if not provided
        validated_data = data.copy()
        if 'timestamp' not in data:
            # Generate ISO timestamp from milliseconds
            import datetime
            timestamp_ms = data['timestamp_milliseconds']
            timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0, tz=datetime.timezone.utc)
            validated_data['timestamp'] = timestamp_dt.isoformat()
        else:
            # Validate provided timestamp
            if not BalloonRiskSchema.validate_timestamp(data['timestamp']):
                raise ValueError("Invalid timestamp format")
        
        # Validate optional fields
        for field in optional_fields:
            if field in data and field != 'timestamp':  # Skip timestamp as it's already handled
                if field in ['balloon_size', 'current_earnings', 'total_earnings', 'time_since_prev_pump']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field in ['is_new_personal_max', 'is_rapid_pump']:
                    if not isinstance(data[field], bool):
                        raise ValueError(f"{field} must be boolean")
        
        return validated_data
    
    @staticmethod
    def validate_cash_out_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate cash out event data structure.
        
        Args:
            data: Cash out event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['balloon_id', 'timestamp_milliseconds', 'earnings_collected']
        optional_fields = ['timestamp', 'pumps_before_cash_out', 'cumulative_earnings', 'hesitation_time']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['earnings_collected'], (int, float)) or data['earnings_collected'] < 0:
            raise ValueError("earnings_collected must be non-negative number")
        
        if not BalloonRiskSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Handle timestamp - generate from milliseconds if not provided
        validated_data = data.copy()
        if 'timestamp' not in data:
            # Generate ISO timestamp from milliseconds
            import datetime
            timestamp_ms = data['timestamp_milliseconds']
            timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0, tz=datetime.timezone.utc)
            validated_data['timestamp'] = timestamp_dt.isoformat()
        else:
            # Validate provided timestamp
            if not BalloonRiskSchema.validate_timestamp(data['timestamp']):
                raise ValueError("Invalid timestamp format")
        
        # Validate optional fields
        for field in optional_fields:
            if field in data and field != 'timestamp':  # Skip timestamp as it's already handled
                if field in ['pumps_before_cash_out', 'cumulative_earnings']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field == 'hesitation_time':
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError("hesitation_time must be non-negative number")
        
        return validated_data
    
    @staticmethod
    def validate_pop_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate pop event data structure.
        
        Args:
            data: Pop event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['balloon_id', 'timestamp_milliseconds', 'pumps_at_pop']
        optional_fields = ['timestamp', 'earnings_lost', 'time_since_last_pump', 'risk_escalation']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['pumps_at_pop'], int) or data['pumps_at_pop'] < 0:
            raise ValueError("pumps_at_pop must be non-negative integer")
        
        if not BalloonRiskSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Handle timestamp - generate from milliseconds if not provided
        validated_data = data.copy()
        if 'timestamp' not in data:
            # Generate ISO timestamp from milliseconds
            import datetime
            timestamp_ms = data['timestamp_milliseconds']
            timestamp_dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0, tz=datetime.timezone.utc)
            validated_data['timestamp'] = timestamp_dt.isoformat()
        else:
            # Validate provided timestamp
            if not BalloonRiskSchema.validate_timestamp(data['timestamp']):
                raise ValueError("Invalid timestamp format")
        
        # Validate optional fields
        for field in optional_fields:
            if field in data and field != 'timestamp':  # Skip timestamp as it's already handled
                if field in ['earnings_lost', 'time_since_last_pump']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field == 'risk_escalation':
                    if not isinstance(data[field], bool):
                        raise ValueError("risk_escalation must be boolean")
        
        return validated_data


class MemoryCardsSchema(BehavioralDataSchema):
    """
    Schema for Memory Cards Game behavioral data.
    
    Validates all memory cards game events according to scientific standards.
    """
    
    @staticmethod
    def validate_card_flip_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate card flip event data structure.
        
        Args:
            data: Card flip event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['card_id', 'card_position', 'timestamp', 'timestamp_milliseconds']
        optional_fields = ['card_value', 'reaction_time', 'round_number', 'cards_flipped']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['card_id'], str):
            raise ValueError("card_id must be string")
        
        if not isinstance(data['card_position'], int) or data['card_position'] < 0:
            raise ValueError("card_position must be non-negative integer")
        
        if not MemoryCardsSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not MemoryCardsSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if field in ['reaction_time', 'round_number', 'cards_flipped']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
        
        return validated_data
    
    @staticmethod
    def validate_match_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate card match event data structure.
        
        Args:
            data: Card match event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['card_id_1', 'card_id_2', 'timestamp', 'timestamp_milliseconds', 'is_correct_match']
        optional_fields = ['reaction_time', 'round_number', 'matches_found', 'memory_accuracy']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['card_id_1'], str) or not isinstance(data['card_id_2'], str):
            raise ValueError("card_id_1 and card_id_2 must be strings")
        
        if not isinstance(data['is_correct_match'], bool):
            raise ValueError("is_correct_match must be boolean")
        
        if not MemoryCardsSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not MemoryCardsSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if field in ['reaction_time', 'round_number', 'matches_found']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field == 'memory_accuracy':
                    if not isinstance(data[field], (int, float)) or data[field] < 0 or data[field] > 100:
                        raise ValueError("memory_accuracy must be between 0 and 100")
        
        return validated_data


class ReactionTimerSchema(BehavioralDataSchema):
    """
    Schema for Reaction Timer Game behavioral data.
    
    Validates all reaction timer game events according to scientific standards.
    """
    
    @staticmethod
    def validate_stimulus_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate stimulus presentation event data structure.
        
        Args:
            data: Stimulus event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['trial_number', 'stimulus_type', 'timestamp', 'timestamp_milliseconds']
        optional_fields = ['block_number', 'stimulus_time', 'stimulus_data']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['trial_number'], int) or data['trial_number'] < 0:
            raise ValueError("trial_number must be non-negative integer")
        
        if not isinstance(data['stimulus_type'], str):
            raise ValueError("stimulus_type must be string")
        
        if not ReactionTimerSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not ReactionTimerSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if field in ['block_number', 'stimulus_time']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field == 'stimulus_data':
                    if not ReactionTimerSchema.validate_json_data(data[field]):
                        raise ValueError("stimulus_data must be valid JSON")
        
        return validated_data
    
    @staticmethod
    def validate_response_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user response event data structure.
        
        Args:
            data: Response event data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['trial_number', 'timestamp', 'timestamp_milliseconds', 'response_time', 'is_correct']
        optional_fields = ['block_number', 'accuracy', 'response_data']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['trial_number'], int) or data['trial_number'] < 0:
            raise ValueError("trial_number must be non-negative integer")
        
        if not isinstance(data['response_time'], (int, float)) or data['response_time'] < 0:
            raise ValueError("response_time must be non-negative number")
        
        if not isinstance(data['is_correct'], bool):
            raise ValueError("is_correct must be boolean")
        
        if not ReactionTimerSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not ReactionTimerSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if field in ['block_number', 'response_time']:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative number")
                elif field == 'accuracy':
                    if not isinstance(data[field], (int, float)) or data[field] < 0 or data[field] > 100:
                        raise ValueError("accuracy must be between 0 and 100")
                elif field == 'response_data':
                    if not ReactionTimerSchema.validate_json_data(data[field]):
                        raise ValueError("response_data must be valid JSON")
        
        return validated_data


class SessionSchema(BehavioralDataSchema):
    """
    Schema for behavioral session data.
    
    Validates session-level data according to scientific standards.
    """
    
    @staticmethod
    def validate_session_start(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate session start data structure.
        
        Args:
            data: Session start data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['session_id', 'device_info', 'timestamp', 'timestamp_milliseconds']
        optional_fields = ['user_agent', 'screen_resolution', 'browser_info']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['session_id'], str):
            raise ValueError("session_id must be string")
        
        if not SessionSchema.validate_json_data(data['device_info']):
            raise ValueError("device_info must be valid JSON")
        
        if not SessionSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not SessionSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if not isinstance(data[field], str):
                    raise ValueError(f"{field} must be string")
        
        return validated_data
    
    @staticmethod
    def validate_session_end(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate session end data structure.
        
        Args:
            data: Session end data dictionary
            
        Returns:
            Dict: Validated and sanitized data
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['session_id', 'timestamp', 'timestamp_milliseconds', 'total_duration']
        optional_fields = ['total_games_played', 'completion_status', 'session_summary']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate data types
        if not isinstance(data['session_id'], str):
            raise ValueError("session_id must be string")
        
        if not isinstance(data['total_duration'], (int, float)) or data['total_duration'] < 0:
            raise ValueError("total_duration must be non-negative number")
        
        if not SessionSchema.validate_timestamp(data['timestamp']):
            raise ValueError("Invalid timestamp format")
        
        if not SessionSchema.validate_milliseconds(data['timestamp_milliseconds']):
            raise ValueError("Invalid millisecond timestamp")
        
        # Validate optional fields
        validated_data = data.copy()
        for field in optional_fields:
            if field in data:
                if field in ['total_games_played']:
                    if not isinstance(data[field], int) or data[field] < 0:
                        raise ValueError(f"{field} must be non-negative integer")
                elif field == 'session_summary':
                    if not SessionSchema.validate_json_data(data[field]):
                        raise ValueError("session_summary must be valid JSON")
        
        return validated_data 