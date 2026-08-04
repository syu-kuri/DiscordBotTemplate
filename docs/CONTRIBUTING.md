# Adding a Cog

1. Create a new file under `bot/cogs/` (e.g. `music.py`).
2. Define a class extending `commands.Cog`, and implement a `setup` function at the bottom of the file:

   ```python
   async def setup(bot: commands.Bot) -> None:
       await bot.add_cog(MyCog(bot))
   ```

3. `TemplateBot.setup_hook()` automatically scans `bot/cogs/`, so no further registration is needed.
4. For commands that need permission gating, use the decorators in `bot/utils/checks.py`.
5. If your cog needs configuration values, add defaults to `config/config.example.yaml` and wire them into the settings object in `bot/core/config.py`.
6. Any user-facing strings should be added as keys in `bot/locales/en.yml` (and `ja.yml`) and fetched via `bot.core.i18n.t()` rather than hardcoded — see [../DESIGN.md](../DESIGN.md) section 3.3.

For the full design rationale, see [../DESIGN.md](../DESIGN.md).

# Issue Policy

- **Design decisions** (architecture, scope, config schema, i18n policy, etc.) live in [../DESIGN.md](../DESIGN.md), not in issues. Open a PR against DESIGN.md to propose a design change.
- **Implementation tasks** (typically picked up by Codex) are tracked as GitHub Issues using the "Implementation task" template, scoped to one DESIGN.md section per issue.
- **Bugs** and **feature requests** from template users are tracked with the "Bug report" / "Feature request" templates.

Labels:

| Label | Meaning |
|---|---|
| `design` | Needs a design decision / DESIGN.md change before implementation |
| `implementation` | A scoped implementation task, ready to be picked up |
| `bug` | Something doesn't work as documented/designed |
| `enhancement` | A new feature or cog request |
| `question` | Needs clarification before it can be scoped |

