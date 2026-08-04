"""Send configured welcome and farewell messages."""

from __future__ import annotations

from typing import cast

import discord
from discord.ext import commands

from bot.core.config import settings


class WelcomeCog(commands.Cog):
    """Post configured messages when members join or leave a guild."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    def _channel_for(guild: discord.Guild) -> discord.TextChannel | None:
        channel_name = settings.welcome.channel_name

        try:
            channel_id = int(channel_name)
        except ValueError:
            return discord.utils.get(guild.text_channels, name=channel_name)

        return cast("discord.TextChannel | None", guild.get_channel(channel_id))

    @staticmethod
    def _format_message(template: str, member: discord.Member) -> str:
        return template.format(
            member=member,
            guild=member.guild,
            # Retain compatibility with the placeholders in the shipped config.
            member_mention=member.mention,
            member_name=member.name,
            guild_name=member.guild.name,
        )

    async def _send_message(self, member: discord.Member, template: str) -> None:
        if not settings.features.welcome:
            return

        channel = self._channel_for(member.guild)
        if channel is not None:
            await channel.send(self._format_message(template, member))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Send the configured message when a member joins."""
        await self._send_message(member, settings.welcome.join_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """Send the configured message when a member leaves."""
        await self._send_message(member, settings.welcome.leave_message)


async def setup(bot: commands.Bot) -> None:
    """Load the welcome cog."""
    await bot.add_cog(WelcomeCog(bot))
