"""Application entry point for the Discord bot."""

from bot.core.bot import TemplateBot
from bot.core.config import settings
from bot.core.logging import setup_logging


def main() -> None:
    """Configure and run the bot."""
    setup_logging(settings.log_level)
    bot = TemplateBot()
    bot.run(settings.discord_token)


if __name__ == "__main__":
    main()
