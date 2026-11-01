from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.db.base import Base
from app.models.recording import RecordingStatus
from app.services.recording import create_recording, update_recording_status
from app.storage.local import FileTooLargeError, read_file


@pytest.fixture(autouse=True)
def _storage_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[None]:
    get_settings.cache_clear()
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    yield
    get_settings.cache_clear()


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


async def test_create_recording_saves_file_and_record(session: AsyncSession) -> None:
    recording = await create_recording(session, "meeting.mp3", b"audio-bytes")

    assert recording.status == RecordingStatus.UPLOADED
    assert Path(recording.storage_path).exists()
    assert read_file(recording.storage_path) == b"audio-bytes"


async def test_create_recording_rejects_oversized_file(
    session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "1")
    get_settings.cache_clear()
    oversized_content = b"x" * (2 * 1024 * 1024)

    with pytest.raises(FileTooLargeError):
        await create_recording(session, "meeting.mp3", oversized_content)

    get_settings.cache_clear()


async def test_update_recording_status(session: AsyncSession) -> None:
    recording = await create_recording(session, "meeting.mp3", b"audio-bytes")

    updated = await update_recording_status(
        session, recording, RecordingStatus.FAILED, error_message="boom"
    )

    assert updated.status == RecordingStatus.FAILED
    assert updated.error_message == "boom"
