import asyncio
from typing import Callable

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

from app.config import settings
from app.logger import logger
from app.routers import ingestion

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=f"{settings.PROJECT_NAME} API",
        version="1.0.0",
        docs_url=f"{settings.APP_URL_PREFIX}/docs",
        redoc_url=f"{settings.APP_URL_PREFIX}/redoc",
        openapi_url=f"{settings.APP_URL_PREFIX}/openapi.json",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    return app

def configure_app(app: FastAPI) -> None:
    """Configure the FastAPI application with middleware, routes, and other settings"""
    # Mount metrics endpoint
    metrics_app = make_asgi_app()
    app.mount(f"{settings.APP_URL_PREFIX}/metrics", metrics_app)
    
    # Include ingestion router
    app.include_router(ingestion.router, prefix=settings.APP_URL_PREFIX)

def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = create_app()
    configure_app(app)
    return app

app = create_application()

async def start() -> None:
    """Start the application"""
    config = uvicorn.Config(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "error"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start())