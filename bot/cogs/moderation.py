"""Moderation application commands."""

from __future__ import annotations

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.core.config import settings
from bot.core.i18n import t
from bot.utils.checks import has_permissions
from bot.utils.embeds import success_embed


class Moderation(commands.Cog):
    """Commands for common server moderation actions."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.mute_role_name = settings.moderation.mute_role_name

    @app_commands.command(
        name="kick",
        description=t("moderation.kick.description"),
    )
    @has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
    ) -> None:
        """Kick a member from the guild."""
        await member.kick(reason=reason)
        await interaction.response.send_message(
            embed=success_embed(
                t("moderation.kick.description"),
                t("moderation.kick.success", member=member, reason=reason),
            )
        )

    @app_commands.command(
        name="ban",
        description=t("moderation.ban.description"),
    )
    @has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
    ) -> None:
        """Ban a member from the guild."""
        await member.ban(reason=reason)
        await interaction.response.send_message(
            embed=success_embed(
                t("moderation.ban.description"),
                t("moderation.ban.success", member=member, reason=reason),
            )
        )

    @app_commands.command(
        name="timeout",
        description=t("moderation.timeout.description"),
    )
    @has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320] = (
            settings.moderation.default_timeout_minutes
        ),
    ) -> None:
        """Temporarily prevent a member from interacting in the guild."""
        await member.timeout(timedelta(minutes=minutes))
        await interaction.response.send_message(
            embed=success_embed(
                t("moderation.timeout.description"),
                t("moderation.timeout.success", member=member, minutes=minutes),
            )
        )

    @app_commands.command(
        name="clear",
        description=t("moderation.clear.description"),
    )
    @has_permissions(manage_messages=True)
    async def clear(
        self,
        interaction: discord.Interaction,
        count: app_commands.Range[int, 1, 100],
    ) -> None:
        """Bulk delete messages from the current channel."""
        channel = interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            raise TypeError("The clear command requires a guild text channel")

        await interaction.response.defer()
        deleted = await channel.purge(limit=count)
        await interaction.followup.send(
            embed=success_embed(
                t("moderation.clear.description"),
                t("moderation.clear.success", count=len(deleted)),
            )
        )


async def setup(bot: commands.Bot) -> None:
    """Load the moderation cog."""
    await bot.add_cog(Moderation(bot))
