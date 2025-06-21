"""Core utilities and base classes for all services."""

from .base_controller import BaseController
from .base_service import BaseService
from .exceptions import (
    ServiceException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    NotFoundException,
)
from .versioning import (
    APIVersion,
    VersionedController,
    VersionNegotiationMiddleware,
    get_api_version,
    version_route,
)

__all__ = [
    "BaseController",
    "BaseService",
    "ServiceException",
    "ValidationException",
    "AuthenticationException",
    "AuthorizationException",
    "NotFoundException",
    "APIVersion",
    "VersionedController",
    "VersionNegotiationMiddleware",
    "get_api_version",
    "version_route",
]
