# TODO(Codex): Implement per DESIGN.md section 3.3 ("Internationalization (i18n)").
# - On startup, load all bot/locales/*.yml files into memory as {locale: {key: value}}
# - Provide t(key: str, locale: str | None = None, **kwargs) -> str
#   - If locale is omitted, use config.yaml's locale.default
#   - If the key is missing in the requested locale, fall back to "en";
#     if it's missing there too, return the key string itself (never raise)
#   - kwargs are interpolated into the message via str.format()
# - Nested keys are referenced with dot notation (e.g. "moderation.kick.success")
