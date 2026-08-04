"""Centralized error handling for application commands."""

from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.i18n import t
from bot.utils.checks import PermissionCheckFailure
from bot.utils.embeds import error_embed

logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """Return user-friendly responses for application-command errors."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Handle expected command failures and report unexpected exceptions."""
        if isinstance(error, PermissionCheckFailure):
            key = "errors.owner_only" if error.owner_only else "errors.no_permission"
            message = t(key)
        elif isinstance(error, app_commands.CommandOnCooldown):
            message = t("errors.cooldown", retry_after=f"{error.retry_after:.1f}")
        elif isinstance(error, app_commands.CheckFailure):
            message = t("errors.no_permission")
        else:
            message = t("errors.unexpected")
            logger.error(
                "Unexpected error while handling application command %s",
                interaction.command,
                exc_info=error,
            )

        embed = error_embed("", message)
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Load the error handler cog."""
    await bot.add_cog(ErrorHandler(bot))
