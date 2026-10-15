from collections.abc import AsyncGenerator

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.models.recording import Recording, RecordingStatus


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


async def test_create_and_read_recording(session: AsyncSession) -> None:
    recording = Recording(
        filename="meeting.mp3",
        storage_path="/data/recordings/meeting.mp3",
        status=RecordingStatus.UPLOADED,
    )
    session.add(recording)
    await session.commit()

    result = await session.execute(select(Recording).where(Recording.id == recording.id))
    fetched = result.scalar_one()

    assert fetched.filename == "meeting.mp3"
    assert fetched.status == RecordingStatus.UPLOADED
    assert fetched.created_at is not None
