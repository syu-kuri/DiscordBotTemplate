# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-08-05

First usable release: the full "standard feature set" described in [DESIGN.md](./DESIGN.md) is implemented and wired together.

### Added

- Cog-based extension structure with automatic loading (`bot/cogs/*.py`)
- Slash Command (`app_commands`) support
- Configuration via `.env` + `config/config.yaml`
- i18n foundation — English by default, Japanese included (`bot/locales/`)
- Moderation commands: `/kick`, `/ban`, `/timeout`, `/clear`
- General commands: `/ping`, `/help`, `/botinfo`
- Owner-only admin commands: `/reload`, `/sync`, `/shutdown`
- Configurable join/leave welcome messages
- Centralized application-command error handling with user-facing embeds
- Console + rotating-file logging
- CI (ruff + pytest) and branch protection on `main`
- MIT license

[0.1.0]: https://github.com/syu-kuri/DiscordBotTemplate/releases/tag/v0.1.0
