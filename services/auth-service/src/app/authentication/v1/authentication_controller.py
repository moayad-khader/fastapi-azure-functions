from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from shared.core.versioning import VersionedController, APIVersion, create_versioned_router
from shared.core.exceptions import ServiceException
from shared.authentication.decorators import get_current_user
from .authentication_service import AuthenticationService
from .schemas.requests import (
    LoginRequest, 
    RegisterRequest, 
    RefreshTokenRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from .schemas.responses import LoginResponse, RegisterResponse, AuthResponse

router = create_versioned_router(APIVersion.V1, tags=["Authentication"])
security = HTTPBearer()


class AuthenticationController(VersionedController):    
    def __init__(self):
        super().__init__(APIVersion.V1)
        self.auth_service = AuthenticationService()

auth_controller = AuthenticationController()


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, http_request: Request):
    try:
        ip_address = http_request.client.host if http_request.client else "unknown"
        user_agent = http_request.headers.get("user-agent", "unknown")
        
        result = await auth_controller.auth_service.login(request, ip_address, user_agent)
        
        if isinstance(result, ServiceException):
            raise auth_controller.handle_service_exception(result)
        
        return auth_controller.success_response(
            data=result,
            message="Login successful"
        )
        
    except ServiceException as e:
        raise auth_controller.handle_service_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred during login"
            )
        )


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    try:
        result = await auth_controller.auth_service.register(request)
        
        if isinstance(result, ServiceException):
            raise auth_controller.handle_service_exception(result)
        
        return auth_controller.success_response(
            data=result,
            message="Registration successful",
            status_code=status.HTTP_201_CREATED
        )
        
    except ServiceException as e:
        raise auth_controller.handle_service_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred during registration"
            )
        )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(request: RefreshTokenRequest):
    try:
        tokens = await auth_controller.auth_service.refresh_token(request.refresh_token)
        
        return auth_controller.success_response(
            data={"tokens": tokens.dict()},
            message="Token refreshed successfully"
        )
        
    except ServiceException as e:
        raise auth_controller.handle_service_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred during token refresh"
            )
        )


@router.post("/change-password", response_model=AuthResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        result = await auth_controller.auth_service.change_password(
            current_user["sub"], 
            request
        )
        
        if isinstance(result, ServiceException):
            raise auth_controller.handle_service_exception(result)
        
        return auth_controller.success_response(
            data=result,
            message="Password changed successfully"
        )
        
    except ServiceException as e:
        raise auth_controller.handle_service_exception(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred while changing password"
            )
        )


@router.post("/forgot-password", response_model=AuthResponse)
async def forgot_password(request: ForgotPasswordRequest):
    try:
        return auth_controller.success_response(
            message="If an account with this email exists, a password reset link has been sent"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred while processing forgot password request"
            )
        )


@router.post("/reset-password", response_model=AuthResponse)
async def reset_password(request: ResetPasswordRequest):
    try:
        return auth_controller.success_response(
            message="Password reset successful"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred while resetting password"
            )
        )


@router.post("/logout", response_model=AuthResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    try:
        return auth_controller.success_response(
            message="Logout successful"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred during logout"
            )
        )


@router.get("/me", response_model=AuthResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    try:
        return auth_controller.success_response(
            data={"user": current_user},
            message="User information retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=auth_controller.error_response(
                message="An unexpected error occurred while retrieving user information"
            )
        )
