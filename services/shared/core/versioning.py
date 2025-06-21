"""API versioning utilities and middleware."""

import re
from enum import Enum
from typing import Optional, Dict, Any, Callable
from fastapi import Request, HTTPException, status
from fastapi.routing import APIRouter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .base_controller import BaseController


class APIVersion(Enum):
    """Supported API versions."""
    V1 = "v1"
    V2 = "v2"
    
    @classmethod
    def from_string(cls, version_str: str) -> Optional['APIVersion']:
        """Convert string to APIVersion enum."""
        version_str = version_str.lower().strip()
        if not version_str.startswith('v'):
            version_str = f'v{version_str}'
        
        for version in cls:
            if version.value == version_str:
                return version
        return None
    
    @classmethod
    def get_latest(cls) -> 'APIVersion':
        """Get the latest API version."""
        return cls.V2
    
    @classmethod
    def get_default(cls) -> 'APIVersion':
        """Get the default API version."""
        return cls.V1


class VersionedController(BaseController):
    """Base controller class with versioning support."""
    
    def __init__(self, version: APIVersion):
        super().__init__()
        self.version = version
    
    def success_response(
        self, 
        data: Any = None, 
        message: str = "Success", 
        status_code: int = status.HTTP_200_OK
    ) -> Dict[str, Any]:
        """Create a standardized success response with version info."""
        response = super().success_response(data, message, status_code)
        response["api_version"] = self.version.value
        return response
    
    def error_response(
        self, 
        message: str = "An error occurred", 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a standardized error response with version info."""
        response = super().error_response(message, status_code, details)
        response["api_version"] = self.version.value
        return response


class VersionNegotiationMiddleware(BaseHTTPMiddleware):
    """Middleware to handle API version negotiation."""
    
    def __init__(self, app, default_version: APIVersion = APIVersion.get_default()):
        super().__init__(app)
        self.default_version = default_version
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and determine API version."""
        # Extract version from URL path
        version = self._extract_version_from_path(request.url.path)
        
        # If no version in path, check headers
        if not version:
            version = self._extract_version_from_headers(request.headers)
        
        # Use default version if none specified
        if not version:
            version = self.default_version
        
        # Store version in request state
        request.state.api_version = version
        
        # Process the request
        response = await call_next(request)
        
        # Add version header to response
        response.headers["X-API-Version"] = version.value
        
        return response
    
    def _extract_version_from_path(self, path: str) -> Optional[APIVersion]:
        """Extract API version from URL path."""
        # Match patterns like /v1/api/, /v2/api/, etc.
        match = re.search(r'/v(\d+)/', path)
        if match:
            version_num = match.group(1)
            return APIVersion.from_string(f"v{version_num}")
        return None
    
    def _extract_version_from_headers(self, headers) -> Optional[APIVersion]:
        """Extract API version from request headers."""
        # Check Accept header for version (e.g., application/vnd.api+json;version=1)
        accept_header = headers.get("accept", "")
        version_match = re.search(r'version=(\d+)', accept_header)
        if version_match:
            version_num = version_match.group(1)
            return APIVersion.from_string(f"v{version_num}")
        
        # Check custom X-API-Version header
        api_version_header = headers.get("x-api-version", "")
        if api_version_header:
            return APIVersion.from_string(api_version_header)
        
        return None


def get_api_version(request: Request) -> APIVersion:
    """Get the API version from request state."""
    return getattr(request.state, 'api_version', APIVersion.get_default())


def version_route(version: APIVersion, path: str) -> str:
    """Generate a versioned route path."""
    return f"/{version.value}/api{path}"


def create_versioned_router(version: APIVersion, prefix: str = "", tags: list = None) -> APIRouter:
    """Create a versioned API router."""
    if tags is None:
        tags = []
    
    return APIRouter(
        prefix=f"/{version.value}/api{prefix}",
        tags=tags
    )


class VersionDeprecationWarning:
    """Utility class for handling version deprecation warnings."""
    
    @staticmethod
    def add_deprecation_header(response: Response, version: APIVersion, sunset_date: str = None):
        """Add deprecation warning headers to response."""
        response.headers["Deprecation"] = "true"
        response.headers["X-API-Deprecated-Version"] = version.value
        if sunset_date:
            response.headers["Sunset"] = sunset_date
    
    @staticmethod
    def is_deprecated(version: APIVersion) -> bool:
        """Check if a version is deprecated."""
        # For now, only V1 is considered deprecated when V2 exists
        return version == APIVersion.V1


def validate_version_compatibility(required_version: APIVersion, request_version: APIVersion) -> bool:
    """Validate if the request version is compatible with required version."""
    # For now, exact match is required
    return required_version == request_version


def get_version_info() -> Dict[str, Any]:
    """Get information about all supported API versions."""
    return {
        "supported_versions": [v.value for v in APIVersion],
        "default_version": APIVersion.get_default().value,
        "latest_version": APIVersion.get_latest().value,
        "deprecated_versions": [v.value for v in APIVersion if VersionDeprecationWarning.is_deprecated(v)]
    }
