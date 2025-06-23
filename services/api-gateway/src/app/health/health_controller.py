from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import httpx
import asyncio

from shared.core.base_controller import BaseController
from shared.utils.config import config

router = APIRouter()


class HealthController(BaseController):
    """Controller for health check endpoints."""
    
    def __init__(self):
        super().__init__()
        self.services = {
            "auth-service": "http://auth-service:8000/api/health",
            "organization-service": "http://organization-service:8000/health"
        }


health_controller = HealthController()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    try:
        return health_controller.success_response(
            data={
                "service": "api-gateway",
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": config.get("APP_VERSION", "1.0.0")
            },
            message="API Gateway is healthy"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=health_controller.error_response(
                message="Health check failed"
            )
        )


@router.get("/services")
async def services_health_check():
    """Check health of all microservices."""
    try:
        service_statuses = {}
        
        async def check_service_health(service_name: str, health_url: str):
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(health_url)
                    if response.status_code == 200:
                        service_statuses[service_name] = {
                            "status": "healthy",
                            "response_time": response.elapsed.total_seconds(),
                            "last_checked": datetime.utcnow().isoformat()
                        }
                    else:
                        service_statuses[service_name] = {
                            "status": "unhealthy",
                            "error": f"HTTP {response.status_code}",
                            "last_checked": datetime.utcnow().isoformat()
                        }
            except Exception as e:
                service_statuses[service_name] = {
                    "status": "unreachable",
                    "error": str(e),
                    "last_checked": datetime.utcnow().isoformat()
                }
        
        # Check all services concurrently
        tasks = [
            check_service_health(name, url) 
            for name, url in health_controller.services.items()
        ]
        await asyncio.gather(*tasks)
        
        # Determine overall status
        all_healthy = all(
            status["status"] == "healthy" 
            for status in service_statuses.values()
        )
        
        overall_status = "healthy" if all_healthy else "degraded"
        
        return health_controller.success_response(
            data={
                "service": "api-gateway",
                "overall_status": overall_status,
                "services": service_statuses,
                "timestamp": datetime.utcnow().isoformat()
            },
            message=f"Services status check complete - {overall_status}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=health_controller.error_response(
                message="Services health check failed"
            )
        )
