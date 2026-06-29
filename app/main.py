from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db.elasticsearch import es_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await es_client.close()


app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")
