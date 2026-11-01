import uuid
from collections.abc import Generator
from pathlib import Path

import pytest

from app.core.config import get_settings
from app.storage.local import FileTooLargeError, delete_file, read_file, save_file


@pytest.fixture(autouse=True)
def _storage_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[None]:
    get_settings.cache_clear()
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    yield
    get_settings.cache_clear()


def test_save_and_read_file(tmp_path: Path) -> None:
    recording_id = uuid.uuid4()
    storage_path = save_file(recording_id, "meeting.mp3", b"audio-bytes")

    assert Path(storage_path) == tmp_path / str(recording_id) / "meeting.mp3"
    assert Path(storage_path).exists()
    assert read_file(storage_path) == b"audio-bytes"


def test_save_file_overwrites_existing_content(tmp_path: Path) -> None:
    recording_id = uuid.uuid4()
    save_file(recording_id, "meeting.mp3", b"first")
    storage_path = save_file(recording_id, "meeting.mp3", b"second")

    assert read_file(storage_path) == b"second"


def test_save_file_creates_storage_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing_dir = tmp_path / "does-not-exist-yet"
    monkeypatch.setenv("STORAGE_PATH", str(missing_dir))
    get_settings.cache_clear()

    recording_id = uuid.uuid4()
    storage_path = save_file(recording_id, "meeting.mp3", b"audio-bytes")

    assert Path(storage_path).exists()


def test_save_file_rejects_oversized_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "1")
    get_settings.cache_clear()

    recording_id = uuid.uuid4()
    oversized_content = b"x" * (2 * 1024 * 1024)

    with pytest.raises(FileTooLargeError):
        save_file(recording_id, "meeting.mp3", oversized_content)

    get_settings.cache_clear()


def test_delete_file_removes_it(tmp_path: Path) -> None:
    recording_id = uuid.uuid4()
    storage_path = save_file(recording_id, "meeting.mp3", b"audio-bytes")

    delete_file(storage_path)

    assert not Path(storage_path).exists()


def test_delete_file_is_noop_when_missing(tmp_path: Path) -> None:
    delete_file(str(tmp_path / "missing" / "file.mp3"))
