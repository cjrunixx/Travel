from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import Base, engine
from app.config.settings import get_settings
from app.models import *  # noqa: F401,F403 — ensure all models are registered before create_all
from app.routers.api import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Base.metadata.create_all(bind=engine)  # Handled by Alembic instead 
    yield


app = FastAPI(
    title="Travel Planner API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


app.add_middleware(

    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


app.include_router(api_router, prefix=settings.api_v1_prefix)
