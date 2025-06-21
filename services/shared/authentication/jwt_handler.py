"""JWT token handling utilities."""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

from ..core.exceptions import AuthenticationException


class JWTHandler:
    """Handle JWT token creation and validation."""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create an access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create a refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode a token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != token_type:
                raise AuthenticationException(f"Invalid token type. Expected {token_type}")
            
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token has expired")
        
        except jwt.InvalidTokenError:
            raise AuthenticationException("Invalid token")
    
    def extract_user_id(self, token: str) -> str:
        """Extract user ID from token."""
        payload = self.verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise AuthenticationException("Token does not contain user ID")
        
        return user_id
    
    def extract_user_permissions(self, token: str) -> list[str]:
        """Extract user permissions from token."""
        payload = self.verify_token(token)
        return payload.get("permissions", [])
    
    def is_token_expired(self, token: str) -> bool:
        """Check if token is expired without raising an exception."""
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True
