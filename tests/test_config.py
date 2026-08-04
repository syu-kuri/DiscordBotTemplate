from pathlib import Path

from dotenv import dotenv_values

from bot.core import config


def test_load_settings_from_example_files(monkeypatch) -> None:
    project_root = Path(__file__).resolve().parents[1]
    env_values = dotenv_values(project_root / ".env.example")
    for key, value in env_values.items():
        if value is not None:
            monkeypatch.setenv(key, value)
    monkeypatch.setenv(
        "CONFIG_PATH", str(project_root / "config" / "config.example.yaml")
    )

    loaded = config.load_settings()

    assert loaded.command_prefix == "!"
    assert loaded.locale.default == "en"
    assert loaded.features.moderation is True


def test_load_settings_ignores_unknown_nested_keys(
    monkeypatch, tmp_path: Path
) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
locale:
  future_option: value
features:
  future_option: true
welcome:
  future_option: value
moderation:
  future_option: value
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONFIG_PATH", str(config_path))

    loaded = config.load_settings()

    assert loaded.locale.default == "en"
    assert loaded.features.welcome is True
    assert loaded.welcome.channel_name == "welcome"
    assert loaded.moderation.mute_role_name == "Muted"


def test_default_config_path_is_anchored_to_project_root(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("CONFIG_PATH", raising=False)
    monkeypatch.chdir(tmp_path)

    loaded = config.load_settings()

    assert loaded.config_path == config._PROJECT_ROOT / "config" / "config.yaml"
