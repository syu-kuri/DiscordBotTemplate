"""Consistently styled embed factories for bot responses."""

import discord


def success_embed(title: str, description: str) -> discord.Embed:
    """Build an embed for a successful operation."""
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green(),
    )


def error_embed(title: str, description: str) -> discord.Embed:
    """Build an embed for an unsuccessful operation."""
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.red(),
    )


def info_embed(title: str, description: str) -> discord.Embed:
    """Build an embed for informational output."""
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue(),
    )
