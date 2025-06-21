from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from shared.core.base_controller import BaseController
from shared.utils.config import config

router = APIRouter()


class HealthController(BaseController):
    """Controller for health check endpoints."""
    
    def __init__(self):
        super().__init__()


health_controller = HealthController()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    try:
        return health_controller.success_response(
            data={
                "service": "auth-service",
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": config.get("APP_VERSION", "1.0.0")
            },
            message="Service is healthy"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=health_controller.error_response(
                message="Health check failed"
            )
        )


@router.get("/ready")
async def readiness_check():
    try:   
        checks = {
            "database": "healthy",
            "jwt_config": "healthy" if config.get("JWT_SECRET_KEY") else "unhealthy",
            "service": "ready"
        }
        
        overall_status = "ready" if all(status == "healthy" for status in checks.values() if status != "ready") else "not_ready"
        
        status_code = status.HTTP_200_OK if overall_status == "ready" else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return health_controller.success_response(
            status_code=status_code,
            data={
                "service": "auth-service",
                "status": overall_status,
                "checks": checks,
                "timestamp": datetime.utcnow().isoformat()
            },
            message=f"Service is {overall_status}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=health_controller.error_response(
                message="Readiness check failed"
            )
        )


@router.get("/live")
async def liveness_check():
    try:
        return health_controller.success_response(
            status_code= status.HTTP_200_OK,
            data={
                "service": "auth-service",
                "status": "alive",
                "timestamp": datetime.utcnow().isoformat()
            },
            message="Service is alive"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=health_controller.error_response(
                message="Liveness check failed"
            )
        )
