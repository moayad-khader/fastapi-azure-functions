"""Authentication decorators."""

from functools import wraps
from typing import Callable, List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import JWTHandler
from .permissions import PermissionChecker
from ..core.exceptions import AuthenticationException, AuthorizationException

security = HTTPBearer()
jwt_handler = JWTHandler()
permission_checker = PermissionChecker()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token."""
    try:
        token = credentials.credentials
        payload = jwt_handler.verify_token(token)
        return payload
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This decorator is used with FastAPI dependency injection
        # The actual authentication is handled by get_current_user dependency
        return await func(*args, **kwargs)
    return wrapper


def require_permission(required_permissions: List[str]) -> Callable:
    """Decorator to require specific permissions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user from kwargs (injected by FastAPI)
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_permissions = current_user.get('permissions', [])
            
            if not permission_checker.has_permissions(user_permissions, required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    """Get current user from JWT token (optional)."""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = jwt_handler.verify_token(token)
        return payload
    except AuthenticationException:
        return None
