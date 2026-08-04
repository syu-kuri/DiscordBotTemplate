"""Load environment and YAML configuration for the bot."""

from __future__ import annotations

import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH = _PROJECT_ROOT / "config" / "config.example.yaml"


@dataclass(frozen=True)
class LocaleSettings:
    default: str


@dataclass(frozen=True)
class FeatureSettings:
    moderation: bool
    welcome: bool


@dataclass(frozen=True)
class WelcomeSettings:
    channel_name: str
    join_message: str
    leave_message: str


@dataclass(frozen=True)
class ModerationSettings:
    mute_role_name: str
    default_timeout_minutes: int


@dataclass(frozen=True)
class Settings:
    discord_token: str
    command_prefix: str
    owner_ids: tuple[int, ...]
    log_level: str
    config_path: Path
    dev_guild_id: int | None
    locale: LocaleSettings
    features: FeatureSettings
    welcome: WelcomeSettings
    moderation: ModerationSettings


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}

    with path.open(encoding="utf-8") as file:
        contents = yaml.safe_load(file)

    if contents is None:
        return {}
    if not isinstance(contents, dict):
        raise TypeError(f"Configuration in {path} must be a YAML mapping")
    return contents


def _merge(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = defaults.copy()
    for key, value in overrides.items():
        default = merged.get(key)
        if isinstance(default, dict) and isinstance(value, dict):
            merged[key] = _merge(default, value)
        else:
            merged[key] = value
    return merged


def _optional_id(value: str) -> int | None:
    return int(value) if value.strip() else None


def _owner_ids(value: str) -> tuple[int, ...]:
    return tuple(
        int(owner_id.strip()) for owner_id in value.split(",") if owner_id.strip()
    )


def _known_fields(settings_type: type[Any], values: dict[str, Any]) -> dict[str, Any]:
    field_names = {field.name for field in fields(settings_type)}
    return {key: value for key, value in values.items() if key in field_names}


def load_settings() -> Settings:
    """Load settings from ``.env`` and YAML, with example values as defaults."""
    load_dotenv()

    config_path_override = os.getenv("CONFIG_PATH")
    config_path = (
        Path(config_path_override)
        if config_path_override is not None
        else _PROJECT_ROOT / "config" / "config.yaml"
    )
    yaml_config = _merge(_load_yaml(_DEFAULT_CONFIG_PATH), _load_yaml(config_path))

    return Settings(
        discord_token=os.getenv("DISCORD_TOKEN", ""),
        command_prefix=os.getenv("COMMAND_PREFIX", "!"),
        owner_ids=_owner_ids(os.getenv("OWNER_IDS", "")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        config_path=config_path,
        dev_guild_id=_optional_id(os.getenv("DEV_GUILD_ID", "")),
        locale=LocaleSettings(**_known_fields(LocaleSettings, yaml_config["locale"])),
        features=FeatureSettings(
            **_known_fields(FeatureSettings, yaml_config["features"])
        ),
        welcome=WelcomeSettings(
            **_known_fields(WelcomeSettings, yaml_config["welcome"])
        ),
        moderation=ModerationSettings(
            **_known_fields(ModerationSettings, yaml_config["moderation"])
        ),
    )


settings = load_settings()
