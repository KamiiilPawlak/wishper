from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging(level=get_settings().LOG_LEVEL)

app = FastAPI(title="Wishper")
app.include_router(api_router, prefix="/api/v1")
