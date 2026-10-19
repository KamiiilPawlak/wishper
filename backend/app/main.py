from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Wishper")
app.include_router(api_router, prefix="/api/v1")
