import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routes import router as api_router
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version="0.1.0", 
    lifespan=lifespan
)

# Instrumentator adds middleware and must be called before the app starts
Instrumentator().instrument(app).expose(app)

app.include_router(api_router, prefix=settings.API_V1_STR)