import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.recording import Recording
from app.schemas.recording import RecordingOut
from app.services.recording import create_recording
from app.storage.local import FileTooLargeError

router = APIRouter(prefix="/recordings", tags=["recordings"])


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=RecordingOut)
async def upload_recording(file: UploadFile, session: AsyncSession = Depends(get_db)) -> Recording:
    content = await file.read()

    try:
        return await create_recording(session, file.filename or "upload", content)
    except FileTooLargeError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc)
        ) from exc


@router.get("/{recording_id}", response_model=RecordingOut)
async def get_recording(
    recording_id: uuid.UUID, session: AsyncSession = Depends(get_db)
) -> Recording:
    recording = await session.scalar(select(Recording).where(Recording.id == recording_id))

    if recording is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found")

    return recording
