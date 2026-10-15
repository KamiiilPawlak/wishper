from fastapi import FastAPI

from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Wishper")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
