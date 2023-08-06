from __future__ import annotations

from typing import TYPE_CHECKING

from .__routes__ import APIRoutes
from ..guild import Guild
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from . import DiscordAPIClient
    
methods = (
    "get_guild",
)

async def get_guild(self: DiscordAPIClient, guild_id):
    request = await self.request(APIRoutes.get_guild(guild_id = Snowflake(guild_id)))
    if request.ok:
        return self._response(Guild, request.json())