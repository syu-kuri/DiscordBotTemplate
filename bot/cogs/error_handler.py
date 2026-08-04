# TODO(Codex): Implement per DESIGN.md section 5 ("Cog Specification") for error_handler.py.
# - Centralize handling in on_app_command_error
# - Notify the user via an Embed for permission errors, cooldowns, etc.
#   (strings via bot.core.i18n.t("errors.*"))
# - Log unexpected exceptions with a stack trace (log output is always English,
#   independent of locale)
