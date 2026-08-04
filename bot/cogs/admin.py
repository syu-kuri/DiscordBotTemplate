"""Owner-only commands for administering the bot."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.config import settings
from bot.core.i18n import t
from bot.utils.checks import is_owner


class Admin(commands.Cog):
    """Owner-only bot administration commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="reload", description=t("admin.reload.description"))
    @is_owner()
    async def reload(self, interaction: discord.Interaction, cog: str) -> None:
        """Reload a bot cog extension."""
        await self.bot.reload_extension(f"bot.cogs.{cog}")
        await interaction.response.send_message(t("admin.reload.success", cog=cog))

    @app_commands.command(name="sync", description=t("admin.sync.description"))
    @is_owner()
    async def sync(self, interaction: discord.Interaction) -> None:
        """Synchronize the bot's application commands."""
        if settings.dev_guild_id is not None:
            guild = discord.Object(id=settings.dev_guild_id)
            self.bot.tree.copy_global_to(guild=guild)
            synced = await self.bot.tree.sync(guild=guild)
        else:
            synced = await self.bot.tree.sync()
        await interaction.response.send_message(
            t("admin.sync.success", count=len(synced))
        )

    @app_commands.command(name="shutdown", description=t("admin.shutdown.description"))
    @is_owner()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        """Acknowledge the command and shut down the bot."""
        await interaction.response.send_message(t("admin.shutdown.confirm"))
        await self.bot.close()


async def setup(bot: commands.Bot) -> None:
    """Load the admin cog."""
    await bot.add_cog(Admin(bot))
