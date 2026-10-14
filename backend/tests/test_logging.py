import pytest
from loguru import logger

from app.core.logging import configure_logging


def test_configure_logging_emits_message(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="DEBUG")
    logger.debug("smoke test message")

    captured = capsys.readouterr()
    assert "smoke test message" in captured.err
