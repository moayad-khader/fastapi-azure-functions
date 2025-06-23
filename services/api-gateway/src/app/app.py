from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx
import json
from typing import Dict, Any, List
import asyncio
from datetime import datetime

from shared.utils.logger import setup_logger
from shared.utils.config import config
from .docs.docs_controller import router as docs_router
from .health.health_controller import router as health_router


def create_app() -> FastAPI:
    setup_logger("api-gateway", config.get("LOG_LEVEL", "INFO"))

    app = FastAPI(
        title="API Gateway",
        description="Centralized API Gateway with unified Swagger documentation for all microservices",
        version=config.get("APP_VERSION", "1.0.0"),
        debug=config.is_debug(),
        docs_url="/gateway/docs",  # Gateway's own docs
        redoc_url="/gateway/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        health_router,
        prefix="/health",
        tags=["Health"]
    )
    
    app.include_router(
        docs_router,
        prefix="",
        tags=["Documentation"]
    )

    return app


app = create_app()
