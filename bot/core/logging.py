"""Application logging configuration."""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_LOG_FILE = Path("logs/bot.log")
_MAX_LOG_BYTES = 5 * 1024 * 1024
_BACKUP_COUNT = 3
_HANDLER_MARKER = "_discord_bot_template_handler"


def _resolve_log_level(log_level: str | int | None) -> int:
    """Return a logging level, defaulting to the ``LOG_LEVEL`` environment variable."""
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")

    if isinstance(log_level, int):
        return log_level

    level = logging.getLevelNamesMapping().get(log_level.upper())
    if level is None:
        raise ValueError(f"Unknown log level: {log_level}")
    return level


def setup_logging(log_level: str | int | None = None) -> None:
    """Configure console and rotating-file logging for the bot and discord.py.

    Calling this function more than once updates the configured level without
    adding another set of handlers.
    """
    level = _resolve_log_level(log_level)
    root_logger = logging.getLogger()
    discord_logger = logging.getLogger("discord")

    handlers = [
        handler
        for handler in root_logger.handlers
        if getattr(handler, _HANDLER_MARKER, False)
    ]

    if not handlers:
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(
            _LOG_FILE,
            maxBytes=_MAX_LOG_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
        handlers = [console_handler, file_handler]

        for handler in handlers:
            setattr(handler, _HANDLER_MARKER, True)
            handler.setFormatter(formatter)
            root_logger.addHandler(handler)

    root_logger.setLevel(level)
    discord_logger.setLevel(level)

    for handler in handlers:
        handler.setLevel(level)
        if handler not in discord_logger.handlers:
            discord_logger.addHandler(handler)

    # The shared handlers already emit discord.py records, so propagation would
    # send the same record through the root logger a second time.
    discord_logger.propagate = False
