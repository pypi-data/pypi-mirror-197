from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp


from .__routes__ import APIRoutes
from ..message import Message, to_dict_or_multipart
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from . import DiscordAPIClient

methods = (
    "get_channel",
    "send_message",
    "edit_message",
    "delete_message"
)

async def get_channel(self: DiscordAPIClient, channel_id):
    pass


async def send_message(
    self: DiscordAPIClient,
    channel_id,
    content = None,
    *,
    embed = None,
    embeds = [],
    file = None,
    files = [],
    components = [],
    allowed_mentions = None,
    reference = None,
    sticker = None,
    suppress_embeds = False,
    tts = False
):
    route = APIRoutes.create_message(channel_id = Snowflake(channel_id))
    payload = to_dict_or_multipart(content, embed, embeds, file, files, components, allowed_mentions, reference, suppress_embeds, sticker, tts)
    
    if isinstance(payload, aiohttp.FormData):
        res = await self.request(route, data = payload, content_type = None)
    else:
        res = await self.request(route, json = payload)
    if res.client_response.ok:
        return self._response(Message, **res.json())

async def edit_message( 
    self: DiscordAPIClient,
    channel_id, 
    message_id,
    content = None,
    *,
    embed = None,
    embeds = [],
    file = None,
    files = [],
    components = [],
    allowed_mentions = None,
    suppress_embeds = None,
):
    route = APIRoutes.edit_message(channel_id = Snowflake(channel_id), message_id = Snowflake(message_id))
    payload = to_dict_or_multipart(content, embed, embeds, file, files, components, allowed_mentions, suppress_embeds)
    
    if isinstance(payload, aiohttp.FormData):
        res = await self.request(route, data = payload)
    else:
        res = await self.request(route, json = payload)
    if res.ok:
        return Message(**res.json())


async def delete_message(self: DiscordAPIClient, channel_id: Snowflake, message_id: Snowflake):
    route = APIRoutes.delete_message(channel_id = Snowflake(channel_id), message_id = Snowflake(message_id))
    return await self.request(route)