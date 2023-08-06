from __future__ import annotations

import json

from enum import Enum
from typing import TYPE_CHECKING, Literal, Optional, Type, Union

from .components import Component
from .embed import Embed
from .enums import *
from .file import File
from .snowflake import Snowflake
from .utils import JSONObject, State, hasarg

if TYPE_CHECKING:
    from .message import AllowedMentions, Message, MessageReference

class ChannelBase:
    def __init__(self,
        id: Snowflake,
        type: int,
        *,
        _state: Optional[State] = None
    ) -> None:
        self.id: Snowflake = Snowflake(id)
        self.type: ChannelType = ChannelType.from_value(type)
        self._state = _state

    def __call__(self, **kwargs) -> Channel:
        d = {
            ChannelType.text: TextChannel,
            ChannelType.dm: DMChannel,
            ChannelType.voice: VoiceChannel,
            ChannelType.category: 4,
            ChannelType.news: 5,
            ChannelType.news_thread: 10,
            ChannelType.public_thread: 11,
            ChannelType.private_thread: 12,
            ChannelType.stage: StageChannel,
            ChannelType.forum: ForumChannel
        }
        cls = d[self.type]
        args = [self.id]
        if hasarg(cls.__init__, "type"):
            args.append(int(self.type))
        kwargs.pop("id", None)
        kwargs.pop("type", None)
        kwargs.pop("_state", None)
        return cls(*args, **kwargs)

class GuildChannel(ChannelBase):
    def __init__(self,
        id: Snowflake,
        type: Literal[0, 2, 4, 13, 15],
        *,
        name: Optional[str] = None,
        nsfw: bool = False,
        
        guild,
        _state = None
    ) -> None:
        super().__init__(id, type, _state = _state)

class _TextChannel(ChannelBase):
    async def send_message(self,
        content: Optional[str] = None,
        *,
        embed: Optional[Embed] = None,
        embeds: list[Embed] = [],
        file: Optional[str | File] = None,
        files: list[str | File] = [],
        components: list[Component] = [],
        allowed_mentions: Optional[AllowedMentions] = None,
        reference: Optional[MessageReference | JSONObject] = None,
        sticker: Optional[Snowflake] = None,
        suppress_embeds: bool = False,
        tts: bool = False
    ) -> Optional[Message]:
        return await self._state.api.send_message(self.id, **locals())

    send = send_message

class _VoiceChannel(ChannelBase):
    pass

class DMChannel(_TextChannel):
    def __init__(self, id: Snowflake, **options) -> None:
        super().__init__(id, int(ChannelType.dm), **options)

class TextChannel(GuildChannel, _TextChannel):
    def __init__(self, id: Snowflake, **options) -> None:
        super().__init__(id, int(ChannelType.text), **options)

class VoiceChannel(GuildChannel, _TextChannel):
    def __init__(self, id: Snowflake, **options) -> None:
        super().__init__(id, int(ChannelType.voice), **options)

class StageChannel: pass

class ForumChannel(GuildChannel):
    def __init__(self, id: Snowflake, **options) -> None:
        super().__init__(id, int(ChannelType.forum), **options)

class Thread(_TextChannel):
    pass

Channel = Union[
    DMChannel,
    TextChannel,
    VoiceChannel
]