from __future__ import annotations

from typing import TYPE_CHECKING

from .__routes__ import APIRoutes
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from . import DiscordAPIClient

methods = (
    "leave_guild",
)

async def leave_guild(self: DiscordAPIClient, guild_id):
    await self.request(APIRoutes.leave_guild(guild_id = Snowflake(guild_id)))