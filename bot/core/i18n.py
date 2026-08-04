"""Load and retrieve the bot's translated user-facing strings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from bot.core.config import settings

_FALLBACK_LOCALE = "en"
_LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"


def _flatten(data: dict[str, Any], prefix: str = "") -> dict[str, str]:
    """Convert a nested locale mapping to dot-separated translation keys."""
    flattened: dict[str, str] = {}
    for key, value in data.items():
        dotted_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            flattened.update(_flatten(value, dotted_key))
        else:
            flattened[dotted_key] = str(value)
    return flattened


def _load_locales() -> dict[str, dict[str, str]]:
    translations: dict[str, dict[str, str]] = {}
    for path in sorted(_LOCALES_DIR.glob("*.yml")):
        with path.open(encoding="utf-8") as locale_file:
            content = yaml.safe_load(locale_file) or {}
        if not isinstance(content, dict):
            content = {}
        translations[path.stem] = _flatten(content)
    return translations


_TRANSLATIONS = _load_locales()
_DEFAULT_LOCALE = settings.locale.default


def t(key: str, locale: str | None = None, **kwargs: object) -> str:
    """Return a translated string, falling back to English and then ``key``."""
    requested = _TRANSLATIONS.get(locale or _DEFAULT_LOCALE, {})
    fallback = _TRANSLATIONS.get(_FALLBACK_LOCALE, {})
    message = requested.get(key, fallback.get(key))
    if message is None:
        return key
    return message.format(**kwargs)
