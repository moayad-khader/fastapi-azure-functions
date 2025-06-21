"""Authentication API v1 module."""

from .authentication_controller import router as auth_v1_router

__all__ = ["auth_v1_router"]
