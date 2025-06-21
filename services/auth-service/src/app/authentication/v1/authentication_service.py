"""Authentication service implementation."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from shared.core.base_service import BaseService
from shared.core.exceptions import (
    AuthenticationException, 
    ValidationException, 
    ConflictException,
    NotFoundException
)
from shared.authentication.jwt_handler import JWTHandler
from shared.utils.helpers import (
    generate_id, 
    hash_password, 
    verify_password, 
    validate_email,
    validate_password_strength
)
from .authentication_models import User, RefreshToken
from .schemas.requests import LoginRequest, RegisterRequest, ChangePasswordRequest
from .schemas.responses import TokenResponse, UserInfo


class AuthenticationService(BaseService):
    
    def __init__(self):
        super().__init__()
        self.jwt_handler = JWTHandler()
        # In a real implementation, you would inject a database repository here
        self._users_db = {}  # Mock database
        self._refresh_tokens_db = {}  # Mock database
    
    async def login(self, request: LoginRequest, ip_address: str, user_agent: str) -> Dict[str, Any]:
        try:
            self.log_operation("login_attempt", {"email": request.email, "ip": ip_address})

            if not validate_email(request.email):
                raise ValidationException("Invalid email format")
            
            user = await self._find_user_by_email(request.email)
            if not user:
                raise AuthenticationException("Invalid credentials")
            
            if not verify_password(request.password, user.password_hash):
                await self._log_failed_login(request.email, ip_address, user_agent, "invalid_password")
                raise AuthenticationException("Invalid credentials")
            
            if not user.is_active:
                raise AuthenticationException("Account is deactivated")
            
            tokens = await self._generate_tokens(user)
            
            await self._update_last_login(user.id)
            
            await self._log_successful_login(user.id, ip_address, user_agent)
            
            self.log_operation("login_success", {"user_id": user.id})
            
            return {
                "tokens": tokens,
                "user": self._user_to_info(user)
            }
            
        except Exception as e:
            return self.handle_exception("login", e)
    
    async def register(self, request: RegisterRequest) -> Dict[str, Any]:

        try:
            self.log_operation("register_attempt", {"email": request.email})
            
            
            self._validate_registration_data(request)
            
            
            existing_user = await self._find_user_by_email(request.email)
            if existing_user:
                raise ConflictException("User with this email already exists")
            
            
            user = await self._create_user(request)
            
            # Generate email verification token (in real implementation)
            # await self._send_verification_email(user)
            
            self.log_operation("register_success", {"user_id": user.id})
            
            return {
                "user": self._user_to_info(user),
                "message": "Registration successful. Please check your email for verification."
            }
            
        except Exception as e:
            return self.handle_exception("register", e)
    
    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        try:
            # Verify refresh token
            payload = self.jwt_handler.verify_token(refresh_token, "refresh")
            user_id = payload.get("sub")
            
            # Find user
            user = await self._find_user_by_id(user_id)
            if not user or not user.is_active:
                raise AuthenticationException("Invalid refresh token")
            
            # Generate new tokens
            tokens = await self._generate_tokens(user)
            
            # Revoke old refresh token (in real implementation)
            # await self._revoke_refresh_token(refresh_token)
            
            return tokens
            
        except Exception as e:
            raise self.handle_exception("refresh_token", e)
    
    async def change_password(self, user_id: str, request: ChangePasswordRequest) -> Dict[str, Any]:
        """Change user password."""
        try:
            # Find user
            user = await self._find_user_by_id(user_id)
            if not user:
                raise NotFoundException("User not found")
            
            # Verify current password
            if not verify_password(request.current_password, user.password_hash):
                raise AuthenticationException("Current password is incorrect")
            
            # Validate new password
            is_valid, errors = validate_password_strength(request.new_password)
            if not is_valid:
                raise ValidationException("Password does not meet requirements", {"errors": errors})
            
            # Update password
            await self._update_password(user_id, request.new_password)
            
            self.log_operation("password_changed", {"user_id": user_id})
            
            return {"message": "Password changed successfully"}
            
        except Exception as e:
            return self.handle_exception("change_password", e)
    
    def _validate_registration_data(self, request: RegisterRequest) -> None:
        """Validate registration data."""
        if not validate_email(request.email):
            raise ValidationException("Invalid email format")
        
        is_valid, errors = validate_password_strength(request.password)
        if not is_valid:
            raise ValidationException("Password does not meet requirements", {"errors": errors})
    
    async def _find_user_by_email(self, email: str) -> Optional[User]:
        """Find user by email (mock implementation)."""
        # In real implementation, this would query the database
        return self._users_db.get(email)
    
    async def _find_user_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID (mock implementation)."""
        # In real implementation, this would query the database
        for user in self._users_db.values():
            if user.id == user_id:
                return user
        return None
    
    async def _create_user(self, request: RegisterRequest) -> User:
        """Create a new user (mock implementation)."""
        user = User(
            id=generate_id(),
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            created_at=datetime.utcnow(),
            permissions=["user:read"]  # Default permissions
        )
        
        self._users_db[request.email] = user
        
        return user
    
    async def _generate_tokens(self, user: User) -> TokenResponse:
        """Generate access and refresh tokens."""
        token_data = {
            "sub": user.id,
            "email": user.email,
            "permissions": user.permissions
        }
        
        access_token = self.jwt_handler.create_access_token(token_data)
        refresh_token = self.jwt_handler.create_refresh_token({"sub": user.id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_handler.access_token_expire_minutes * 60
        )
    
    async def _update_last_login(self, user_id: str) -> None:
        """Update user's last login timestamp."""
        # In real implementation, this would update the database
        pass
    
    async def _update_password(self, user_id: str, new_password: str) -> None:
        """Update user password."""
        # In real implementation, this would update the database
        for user in self._users_db.values():
            if user.id == user_id:
                user.password_hash = hash_password(new_password)
                user.updated_at = datetime.utcnow()
                break
    
    async def _log_successful_login(self, user_id: str, ip_address: str, user_agent: str) -> None:
        """Log successful login attempt."""
        # In real implementation, this would log to database
        pass
    
    async def _log_failed_login(self, email: str, ip_address: str, user_agent: str, reason: str) -> None:
        """Log failed login attempt."""
        # In real implementation, this would log to database
        pass
    
    def _user_to_info(self, user: User) -> UserInfo:
        """Convert User model to UserInfo response."""
        return UserInfo(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            permissions=user.permissions,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
