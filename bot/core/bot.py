# TODO(Codex): Implement per DESIGN.md section 4 ("Bot Core").
# - TemplateBot class extending commands.Bot
# - In setup_hook(), load bot.core.i18n (see DESIGN.md 3.3), then auto-load
#   all cogs under bot/cogs/, then sync app_commands
#   (guild-scoped sync if DEV_GUILD_ID is set, otherwise global sync)
# - Declare only the minimal required Intents explicitly
