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
