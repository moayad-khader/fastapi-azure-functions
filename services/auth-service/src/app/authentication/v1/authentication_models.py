"""Authentication data models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    first_name: str
    last_name: str
    is_active: bool = True
    is_verified: bool = False
    permissions: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    id: str
    user_id: str
    token_hash: str
    expires_at: datetime
    created_at: datetime
    is_revoked: bool = False
    
    class Config:
        from_attributes = True


class PasswordResetToken(BaseModel):
    id: str
    user_id: str
    token_hash: str
    expires_at: datetime
    created_at: datetime
    is_used: bool = False
    
    class Config:
        from_attributes = True


class EmailVerificationToken(BaseModel):
    id: str
    user_id: str
    token_hash: str
    expires_at: datetime
    created_at: datetime
    is_used: bool = False
    
    class Config:
        from_attributes = True


class LoginAttempt(BaseModel):
    id: str
    email: str
    ip_address: str
    user_agent: str
    success: bool
    failure_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
