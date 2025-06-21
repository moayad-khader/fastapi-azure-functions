from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.core.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
from shared.core.versioning import VersionNegotiationMiddleware, APIVersion
from shared.utils.logger import setup_logger
from shared.utils.config import config
from .authentication.v1 import auth_v1_router
from .health.health_controller import router as health_router


def create_app() -> FastAPI:
    setup_logger("auth-service", config.get("LOG_LEVEL", "INFO"))

    app = FastAPI(
        title="Authentication Service",
        description="Microservice for user authentication and authorization with API versioning",
        version=config.get("APP_VERSION", "1.0.0"),
        debug=config.is_debug(),
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(VersionNegotiationMiddleware, default_version=APIVersion.V1)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    app.include_router(
        health_router,
        prefix="/api",
        tags=["Health"]
    )

    app.include_router(auth_v1_router)

    return app


app = create_app()
