"""Authentication response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserInfo(BaseModel):
    """User information schema."""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    is_active: bool = Field(..., description="User active status")
    is_verified: bool = Field(..., description="Email verification status")
    permissions: List[str] = Field(default=[], description="User permissions")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="User last update timestamp")


class LoginResponse(BaseModel):
    """Login response schema."""
    success: bool = Field(default=True, description="Operation success status")
    message: str = Field(default="Login successful", description="Response message")
    data: dict = Field(..., description="Response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "data": {
                    "tokens": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "token_type": "bearer",
                        "expires_in": 1800
                    },
                    "user": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True,
                        "is_verified": True,
                        "permissions": ["user:read", "user:write"]
                    }
                }
            }
        }


class RegisterResponse(BaseModel):
    """Registration response schema."""
    success: bool = Field(default=True, description="Operation success status")
    message: str = Field(default="Registration successful", description="Response message")
    data: dict = Field(..., description="Response data")


class AuthResponse(BaseModel):
    """Generic authentication response schema."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[dict] = Field(None, description="Response data")
    status_code: int = Field(..., description="HTTP status code")
