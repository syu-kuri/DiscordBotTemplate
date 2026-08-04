"""Discord bot subclass and startup hooks."""

from __future__ import annotations

import importlib
import logging
from pathlib import Path

import discord
from discord.ext import commands

from bot.core.config import settings

_COGS_DIR = Path(__file__).resolve().parent.parent / "cogs"
_LOGGER = logging.getLogger(__name__)


class TemplateBot(commands.Bot):
    """Bot implementation that discovers cogs and synchronizes commands."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        # Enable additional privileged intents here if a custom cog needs them.
        super().__init__(command_prefix=settings.command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        """Load translations and cogs, then synchronize application commands."""
        importlib.import_module("bot.core.i18n")

        for cog_path in sorted(_COGS_DIR.glob("*.py")):
            if cog_path.name == "__init__.py":
                continue
            extension = f"bot.cogs.{cog_path.stem}"
            try:
                await self.load_extension(extension)
            except commands.NoEntryPointError:
                _LOGGER.warning("skipping %s: not yet implemented", extension)

        if settings.dev_guild_id is not None:
            guild = discord.Object(id=settings.dev_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
