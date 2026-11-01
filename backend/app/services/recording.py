import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recording import Recording, RecordingStatus
from app.storage.local import save_file


async def create_recording(session: AsyncSession, filename: str, content: bytes) -> Recording:
    recording_id = uuid.uuid4()
    storage_path = save_file(recording_id, filename, content)

    recording = Recording(
        id=recording_id,
        filename=filename,
        storage_path=storage_path,
        status=RecordingStatus.UPLOADED,
    )
    session.add(recording)
    await session.commit()

    return recording


async def update_recording_status(
    session: AsyncSession,
    recording: Recording,
    status: RecordingStatus,
    error_message: str | None = None,
) -> Recording:
    recording.status = status
    recording.error_message = error_message
    await session.commit()

    return recording
