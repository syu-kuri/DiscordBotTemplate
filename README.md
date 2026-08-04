# Discord Bot Template

A Discord bot template that covers the essentials of running a server bot — a Slash Command foundation, moderation, join/leave notifications, and logging — and is easy to extend.

See [DESIGN.md](./DESIGN.md) for the full design.

## Features

- Cog-based extension structure (drop a file into `bot/cogs/` and it auto-loads)
- Slash Command (`app_commands`) support
- Simple configuration via `.env` + YAML
- Built-in moderation commands (kick / ban / timeout / clear)
- Configurable welcome/leave messages on join/leave
- Built-in i18n foundation (English by default, Japanese included)
- Console and file logging

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env               # set DISCORD_TOKEN, etc.
cp config/config.example.yaml config/config.yaml
python -m bot.main
```

## Directory Layout

See [DESIGN.md](./DESIGN.md#2-directory-layout) for details.

## License

[MIT License](./LICENSE)
