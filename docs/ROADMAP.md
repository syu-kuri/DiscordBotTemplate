# Roadmap

Planned work toward `v1.0.0`. This is a server-management-focused template; features that turn it into a general-purpose "everything" bot (music, economy/leveling, web dashboard) stay out of scope — see [DESIGN.md section 10](../DESIGN.md#10-out-of-scope-not-included-in-this-template).

Versioning and process follow [WORKFLOW.md](./WORKFLOW.md). Each version below becomes a GitHub Milestone; each feature becomes one or more `implementation` issues scoped to a DESIGN.md section.

## v0.1.0 — MVP ✅ (released)

Config + i18n foundation, logging, bot core with cog auto-loading, and the general / moderation / welcome / admin / error-handler cogs. Issues #1–#12.

## v0.2.0 — Persistence foundation

Prerequisite for per-guild features and the warning system.

- **Persistence layer (SQLite via `aiosqlite`)** — a small async DB layer with schema/migration bootstrapping under `data/`. No external server required, keeping the "clone and run" goal intact.
- **Per-guild settings** — move guild-specific config (welcome channel, mod-log channel, etc.) from the single bot-wide `config.yaml` into the DB so one bot instance can serve multiple servers with different settings. `config.yaml` stays as the source of *defaults*.
- **Startup validation** — fail fast with a clear, actionable message when `DISCORD_TOKEN` is missing/blank or required config is malformed, instead of a raw traceback.

## v0.3.0 — Moderation hardening

Directly extends the existing `moderation` cog; the most-requested tier in comparable templates.

- **Mod-log channel** — record kick/ban/timeout/clear (and warnings) as embeds in a configurable channel.
- **Warning system** — `/warn`, `/warnings`, `/clearwarnings`, persisted per guild, with configurable auto-escalation (e.g. N warns → timeout/kick).
- **Command cooldowns** — per-user/per-command cooldowns on moderation actions.
- **Confirmation UI** — button confirm/cancel prompt before destructive actions (ban/kick), handled through the existing error/interaction plumbing.

## v0.4.0 — Server utilities

Low-dependency, low-risk additions.

- **Info commands** — `/serverinfo`, `/userinfo`, `/avatar`.
- **Role menus** — self-assignable roles via buttons/select menus, persisted per guild.
- **Paginated help** — button-based pagination for `/help` as command count grows.

## v0.5.0 — Deployment & developer experience

Independent of bot features; makes the template production-ready and contributor-friendly.

- **Docker** — `Dockerfile` + `docker-compose.yml` for one-command deployment.
- **Dependabot** — automated dependency update PRs.
- **pre-commit** — ruff (+ formatting) hooks so contributors catch issues before CI.
- **Static typing in CI** — add a type checker (mypy or pyright) to the CI workflow.
- **Error webhook** — optionally forward unexpected exceptions to a Discord webhook for ops visibility (opt-in via env).

## v1.0.0 — Stable

Cut once the v0.5.0 feature set has been run on a real server and shaken out — a judgment call by the repo owner, not an automatic trigger (see WORKFLOW.md).

## Explicitly out of scope

Deferred/declined so the template stays focused on server management:

- Anti-raid / join-rate protection
- Verification gate (button-assigned member role)
- Ticket system
- Community extras: polls, reminders, announcement builder
- Music playback, economy/leveling, web dashboard (long-standing non-scope, see DESIGN.md section 10)

These can live as separate optional add-on cogs a user drops in, rather than shipping in the base template.
