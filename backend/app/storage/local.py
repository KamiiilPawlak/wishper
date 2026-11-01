import uuid
from pathlib import Path

from app.core.config import get_settings


class FileTooLargeError(Exception):
    def __init__(self, size_bytes: int, max_size_bytes: int) -> None:
        self.size_bytes = size_bytes
        self.max_size_bytes = max_size_bytes
        super().__init__(f"File size {size_bytes} bytes exceeds limit of {max_size_bytes} bytes")


def _recording_dir(recording_id: uuid.UUID) -> Path:
    return Path(get_settings().STORAGE_PATH) / str(recording_id)


def save_file(recording_id: uuid.UUID, filename: str, content: bytes) -> str:
    max_size_bytes = get_settings().MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_size_bytes:
        raise FileTooLargeError(len(content), max_size_bytes)

    recording_dir = _recording_dir(recording_id)
    recording_dir.mkdir(parents=True, exist_ok=True)

    file_path = recording_dir / filename
    file_path.write_bytes(content)

    return str(file_path)


def read_file(storage_path: str) -> bytes:
    return Path(storage_path).read_bytes()


def delete_file(storage_path: str) -> None:
    Path(storage_path).unlink(missing_ok=True)
