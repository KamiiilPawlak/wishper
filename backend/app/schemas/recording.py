import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.recording import RecordingStatus


class RecordingCreate(BaseModel):
    filename: str


class RecordingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    status: RecordingStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime
