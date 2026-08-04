"""Reusable application-command permission checks."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

import discord
from discord import app_commands

from bot.core.config import settings

Check = Callable[[discord.Interaction], Coroutine[Any, Any, bool]]


class PermissionCheckFailure(app_commands.CheckFailure):
    """Raised when a user does not satisfy one of the bot's permission checks."""

    def __init__(
        self,
        *,
        owner_only: bool = False,
        missing_permissions: tuple[str, ...] = (),
    ) -> None:
        self.owner_only = owner_only
        self.missing_permissions = missing_permissions
        super().__init__()


def is_owner() -> Callable[[Check], Check]:
    """Allow an application command only for a configured bot owner."""

    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id not in settings.owner_ids:
            raise PermissionCheckFailure(owner_only=True)
        return True

    return app_commands.check(predicate)


def has_permissions(**perms: bool) -> Callable[[Check], Check]:
    """Require the invoking member to have all of ``perms`` in the channel."""
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        names = ", ".join(sorted(invalid))
        raise TypeError(f"Invalid permission name(s): {names}")
    if not all(isinstance(value, bool) for value in perms.values()):
        raise TypeError("Permission values must be bools")

    async def predicate(interaction: discord.Interaction) -> bool:
        permissions = interaction.permissions
        missing = tuple(
            name for name, value in perms.items() if getattr(permissions, name) != value
        )
        if missing:
            raise PermissionCheckFailure(missing_permissions=missing)
        return True

    return app_commands.check(predicate)
