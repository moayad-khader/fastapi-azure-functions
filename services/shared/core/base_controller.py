"""Base controller class with common functionality."""

from abc import ABC
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from .exceptions import ServiceException


class BaseController(ABC):
    """Base controller class that provides common functionality for all controllers."""
    
    def __init__(self):
        """Initialize the base controller."""
        pass
    
    def success_response(
        self, 
        data: Any = None, 
        message: str = "Success", 
        status_code: int = status.HTTP_200_OK
    ) -> Dict[str, Any]:
        """Create a standardized success response."""
        response = {
            "success": True,
            "message": message,
            "status_code": status_code
        }
        
        if data is not None:
            response["data"] = data
            
        return response
    
    def error_response(
        self, 
        message: str = "An error occurred", 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a standardized error response."""
        response = {
            "success": False,
            "message": message,
            "status_code": status_code
        }
        
        if details:
            response["details"] = details
            
        return response
    
    def handle_service_exception(self, exception: ServiceException) -> HTTPException:
        """Convert service exceptions to HTTP exceptions."""
        return HTTPException(
            status_code=exception.status_code,
            detail=self.error_response(
                message=exception.message,
                status_code=exception.status_code,
                details=exception.details
            )
        )
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: list[str]) -> None:
        """Validate that required fields are present in the data."""
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.error_response(
                    message="Missing required fields",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    details={"missing_fields": missing_fields}
                )
            )
