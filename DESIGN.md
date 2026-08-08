# Discord Bot Template — Design Document

- **Role split**: Design = Claude (this document) / Implementation = Codex
- **Language/Framework**: Python 3.11+ / discord.py 2.x (Slash Commands via `app_commands`)
- **License**: MIT (see `LICENSE`)
- **Distribution**: GitHub template repository (server operators clone it via "Use this template")
- **Bot output language**: Has an i18n foundation; default is English (`en`). Japanese (`ja`) is bundled and selectable via `config.yaml`

Codex should implement the `TODO` comments embedded in the code, each of which points at the corresponding section of this document. When adding new files, follow the directory layout and naming conventions defined here.

## 1. Goal

Provide a generic "foundation" for a Discord bot. A server operator should be able to clone → configure `.env` → run, and get baseline bot operation (moderation, join/leave notifications, basic info commands) out of the box, while being able to add features easily on a per-cog basis.

## 2. Directory Layout

```
DiscordBotTemplate/
├── LICENSE
├── README.md
├── DESIGN.md
├── .env.example
├── .gitignore
├── requirements.txt
├── config/
│   └── config.example.yaml
├── bot/
│   ├── __init__.py
│   ├── main.py                 # entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bot.py              # Bot subclass, cog auto-loading
│   │   ├── config.py           # loads .env + config.yaml
│   │   ├── logging.py          # logging setup
│   │   └── i18n.py             # loads locale files, translation function t()
│   ├── locales/
│   │   ├── en.yml               # default locale (English)
│   │   └── ja.yml               # Japanese locale
│   ├── cogs/
│   │   ├── __init__.py
│   │   ├── general.py          # ping / help / botinfo
│   │   ├── moderation.py       # kick / ban / timeout / clear
│   │   ├── welcome.py          # join/leave messages
│   │   ├── admin.py            # owner-only: reload / sync / shutdown
│   │   └── error_handler.py    # shared command error handling
│   └── utils/
│       ├── __init__.py
│       ├── embeds.py           # shared Embed builders
│       └── checks.py           # permission-check decorators
├── data/                        # runtime-generated data (gitignored)
├── tests/
│   └── test_config.py
├── docs/
│   └── CONTRIBUTING.md
└── .github/
    └── workflows/
        └── ci.yml               # lint + import tests
```

## 3. Configuration

### 3.1 `.env` (secrets and environment-specific values)

```
DISCORD_TOKEN=
COMMAND_PREFIX=!
OWNER_IDS=              # comma-separated Discord user IDs
LOG_LEVEL=INFO
CONFIG_PATH=config/config.yaml
```

### 3.2 `config/config.yaml` (feature toggles and copy; defaults are safe to commit)

```yaml
locale:
  default: en              # matches a filename (without extension) under bot/locales/. Bundled: en, ja

features:
  moderation: true
  welcome: true

welcome:
  channel_name: "welcome"          # matched by channel name (a channel ID also works)
  join_message: "Welcome {member_mention} to {guild_name}!"
  leave_message: "{member_name} has left the server."

moderation:
  mute_role_name: "Muted"
  default_timeout_minutes: 10
```

`bot/core/config.py` loads `.env` via `python-dotenv` and merges in the YAML at `CONFIG_PATH`, exposing it as an immutable settings object (a `dataclass` is recommended). Missing keys must fall back to their default values.

`welcome.join_message` / `leave_message` are meant to be freely rewritten by the operator, so they are not part of the locale files (i18n only covers the fixed strings built into the template). The defaults are in English, but operators are free to rewrite them in Japanese or any other language for their own server.

### 3.3 Internationalization (i18n)

**Purpose**: Make the fixed strings built into the template — such as the `/ping` response and error messages — switchable between English and Japanese.

**Locale files** (`bot/locales/*.yml`): `en.yml` is the source of truth (and fallback target); every locale file must have an identical key structure. Nested keys are referenced with dot notation (e.g. `moderation.kick.success`).

**Responsibilities of `bot/core/i18n.py`**:

- On startup, load all `bot/locales/*.yml` files into memory as a `{locale: {key: value}}` dictionary.
- Provide `t(key: str, locale: str | None = None, **kwargs) -> str`.
  - If `locale` is omitted, use `config.yaml`'s `locale.default`.
  - If the key is missing in the requested locale, fall back to `en`; if it's missing there too, return the key string itself (never raise on a missing key).
  - `kwargs` are interpolated into the message via `str.format()`.
- The locale is currently a single, bot-wide setting (`config.yaml`'s `locale.default`); a runtime command to switch locale per server (guild) is out of scope for this template (the `locale` argument is kept on `t()`'s signature so this can be added later by persisting a `guild_id -> locale` mapping under `data/`).
- Every cog and `utils/embeds.py` must fetch strings via `t()` rather than hardcoding them.

## 4. Bot Core (`bot/core/bot.py`)

- A `TemplateBot` class extending `commands.Bot`.
- In `setup_hook()`, scan `bot/cogs/` for `*.py` files, auto-load them, and `sync()` `app_commands` (guild-scoped sync if a dev guild ID is set in `.env`, otherwise a global sync).
- Declare only the minimal required Intents, including `message_content` (with a comment guiding template users on how to add more as needed).

## 5. Cog Specification

| Cog | Commands | Permissions | i18n key namespace |
|---|---|---|---|
| `general.py` | `/ping`, `/help`, `/botinfo` (shows uptime, latency, version) | Everyone | `general.*` |
| `moderation.py` | `/kick`, `/ban`, `/timeout`, `/clear` (bulk message delete) | Gated via `checks.py` decorators (e.g. `manage_guild`) | `moderation.*` |
| `welcome.py` | Posts the `config.yaml` templates on `on_member_join` / `on_member_remove`. Supports placeholders `{member}`, `{member.mention}`, `{member.name}`, `{guild.name}` | Event-driven, no commands | - (out of scope; these are free-form operator text in `config.yaml`) |
| `admin.py` | `/reload <cog>`, `/sync`, `/shutdown` | Restricted to users in `OWNER_IDS` (`checks.is_owner()`) | `admin.*` |
| `error_handler.py` | Centralizes `on_app_command_error` handling, returning user-friendly Embeds for permission errors, cooldowns, and unexpected exceptions. Unexpected exceptions are logged with a stack trace | - | `errors.*` |

Every command's `description` (the Slash Command help text), response messages, and Embed copy are expected to come from the keys already defined in `bot/locales/en.yml` / `ja.yml` (an initial version of `bot/locales/*.yml` has been prepared alongside this document).

## 6. Utilities

- `utils/embeds.py`: consistently styled Embed factories such as `success_embed(title, description)`, `error_embed(...)`, `info_embed(...)`.
- `utils/checks.py`: `is_owner()` and `has_permissions(**perms)` provided as `app_commands.check`s, raising a shared permission-error exception on failure (caught by `error_handler.py`).

## 7. Logging (`bot/core/logging.py`)

- Console output honoring `LOG_LEVEL`, plus a `RotatingFileHandler` writing to `logs/bot.log` (~5MB x 3 backups).
- discord.py's own `discord` logger is attached to the same handlers.
- Log messages themselves are unaffected by `locale.default` and are always emitted in English (they're for the developers operating/debugging the bot). i18n only applies to strings end users see on Discord.

## 8. Testing / CI

- `tests/test_config.py`: a minimal test verifying that settings load without raising, using `.env.example` and `config.example.yaml`.
- `tests/test_i18n.py`: verifies that `en.yml` and `ja.yml` have exactly the same set of keys, and that `t()` never raises even for an unknown key or unknown locale.
- `.github/workflows/ci.yml`: runs `ruff` for linting and `pytest`. The bot itself (which requires a token) is not run in CI.

## 9. Distribution / Usage Flow (intended for the README)

1. Create a repository from the GitHub template via "Use this template".
2. `pip install -r requirements.txt`.
3. Copy `.env.example` → `.env` and set `DISCORD_TOKEN`, etc.
4. If needed, copy `config/config.example.yaml` → `config/config.yaml` and edit it.
5. Run with `python -m bot.main`.

## 10. Out of Scope (not included in this template)

- Music playback
- A dashboard/web UI
- Economy / leveling systems
- Anti-raid protection, verification gates, ticket systems, and community extras (polls, reminders, announcement builders) — see `docs/ROADMAP.md` for the rationale
- A runtime command to dynamically switch language per server (guild). The i18n foundation itself is in scope per section 3.3 — switching is expected to happen by changing `config.yaml`'s `locale.default` and restarting; a runtime command for this is not supported.

These are beyond the "standard feature set" tier, so users who want them are expected to add their own cog (see `docs/CONTRIBUTING.md` for how to add a cog).

> **Note:** As of the v0.2.0 roadmap, lightweight database persistence (SQLite via `aiosqlite`) is now *in* scope — it backs per-guild settings and the warning system. It was originally listed here as out of scope for the v0.1.0 MVP; that decision was revisited. External database servers (e.g. standalone PostgreSQL) remain out of scope to preserve the "clone and run" goal. See `docs/ROADMAP.md`.
