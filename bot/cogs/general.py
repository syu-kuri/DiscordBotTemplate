"""General-purpose information commands."""

from __future__ import annotations

from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.i18n import t
from bot.utils.embeds import info_embed


class General(commands.Cog):
    """Provide commands that expose basic bot information."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.started_at = datetime.now(timezone.utc)

    @app_commands.command(name="ping", description=t("general.ping.description"))
    async def ping(self, interaction: discord.Interaction) -> None:
        """Report the bot's current websocket latency."""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(
            t("general.ping.response", latency=latency)
        )

    @app_commands.command(name="help", description=t("general.help.description"))
    async def help_command(self, interaction: discord.Interaction) -> None:
        """List the bot's registered application commands."""
        commands_list = sorted(self.bot.tree.walk_commands(), key=lambda item: item.name)
        description = "\n".join(
            f"/{command.qualified_name} — {command.description}"
            for command in commands_list
        )
        embed = info_embed(t("general.help.description"), description)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description=t("general.botinfo.description"))
    async def botinfo(self, interaction: discord.Interaction) -> None:
        """Report uptime, websocket latency, and the discord.py version."""
        uptime = datetime.now(timezone.utc) - self.started_at
        latency = round(self.bot.latency * 1000)
        embed = info_embed(t("general.botinfo.title"), "")
        embed.add_field(
            name=t("general.botinfo.field_uptime"),
            value=str(uptime).split(".", maxsplit=1)[0],
        )
        embed.add_field(
            name=t("general.botinfo.field_latency"),
            value=latency,
        )
        embed.add_field(
            name=t("general.botinfo.field_version"),
            value=discord.__version__,
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Register the general cog."""
    await bot.add_cog(General(bot))
