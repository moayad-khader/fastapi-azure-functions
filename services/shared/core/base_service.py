"""Base service class with common functionality."""

from abc import ABC
from typing import Any, Dict, Optional
import logging

from .exceptions import ServiceException, ValidationException


class BaseService(ABC):
    """Base service class that provides common functionality for all services."""
    
    def __init__(self):
        """Initialize the base service."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def validate_input(self, data: Dict[str, Any], validation_rules: Dict[str, Any]) -> None:
        """Validate input data against validation rules."""
        errors = []
        
        for field, rules in validation_rules.items():
            value = data.get(field)
            
            # Check required fields
            if rules.get("required", False) and (value is None or value == ""):
                errors.append(f"{field} is required")
                continue
            
            # Skip validation if field is not required and not provided
            if value is None:
                continue
            
            # Check data type
            expected_type = rules.get("type")
            if expected_type and not isinstance(value, expected_type):
                errors.append(f"{field} must be of type {expected_type.__name__}")
            
            # Check minimum length
            min_length = rules.get("min_length")
            if min_length and isinstance(value, str) and len(value) < min_length:
                errors.append(f"{field} must be at least {min_length} characters long")
            
            # Check maximum length
            max_length = rules.get("max_length")
            if max_length and isinstance(value, str) and len(value) > max_length:
                errors.append(f"{field} must be at most {max_length} characters long")
            
            # Check custom validation function
            custom_validator = rules.get("validator")
            if custom_validator and callable(custom_validator):
                try:
                    custom_validator(value)
                except ValueError as e:
                    errors.append(f"{field}: {str(e)}")
        
        if errors:
            raise ValidationException("Validation failed", details={"errors": errors})
    
    def log_operation(self, operation: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log service operations."""
        log_message = f"Operation: {operation}"
        if details:
            log_message += f" | Details: {details}"
        
        self.logger.info(log_message)
    
    def log_error(self, operation: str, error: Exception, details: Optional[Dict[str, Any]] = None) -> None:
        """Log service errors."""
        log_message = f"Error in operation: {operation} | Error: {str(error)}"
        if details:
            log_message += f" | Details: {details}"
        
        self.logger.error(log_message, exc_info=True)
    
    def handle_exception(self, operation: str, error: Exception) -> ServiceException:
        """Handle and convert exceptions to service exceptions."""
        self.log_error(operation, error)
        
        if isinstance(error, ServiceException):
            return error
        
        # Convert common exceptions to service exceptions
        if isinstance(error, ValueError):
            return ValidationException(str(error))
        
        # Default to generic service exception
        return ServiceException(f"An error occurred during {operation}: {str(error)}")
