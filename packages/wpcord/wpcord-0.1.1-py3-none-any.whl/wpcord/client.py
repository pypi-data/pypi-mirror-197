import asyncio

from typing import (
    Callable,
    List,
    Optional,
)

from aiohttp import ClientSession

from .api import DiscordAPIClient
from .channel import Channel
from .enums import *
from .exceptions import *
from .flags import Intents
from .gateway import DiscordGatewayClient
from .guild import Guild
from .http import HTTPClient
from .message import Message
from .snowflake import Snowflake
from .utils import get_from_list



class Client:
    def __init__(self,
        token: str,
        *,
        is_bot: bool = True,
        intents: Intents = Intents(),
        api_version: int = 10,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[ClientSession] = None
    ) -> None:
        self.is_bot = is_bot
        self.token = token
        self.intents: Intents = intents

        self.loop = loop or asyncio.get_event_loop()
        self.session = session or ClientSession()
        
        kwargs = dict(loop = self.loop, session = self.session, api_version = api_version)
        self.api = DiscordAPIClient(
            self.token,
            TokenType.Bot if self.is_bot else TokenType.User,
            **kwargs
        )
        self.gateway = DiscordGatewayClient(intents = self.intents, **kwargs)
        self.http = HTTPClient()
        
        self.run = self.gateway.run

    @property
    def channels(self) -> List[Channel]:
        result = []
        for guild in self.guilds:
            for channel in guild.channels:
                result.append(channel)
        return result

    @property
    def channel_count(self) -> int:
        return len(self.channels)

    @property
    def guilds(self) -> List[Guild]:
        return [guild for guild in self.gateway.cache.guilds.values() if not guild.unavailable]

    @property
    def guild_count(self) -> int:
        return len(self.guilds)



    def event(self, function: Callable):
        self.gateway.event(function)

    def get_channel(self, id: Snowflake) -> Optional[Channel]:
        return get_from_list(self.channels, lambda channel: channel.id == Snowflake(id))

    def get_guild(self, id: Snowflake) -> Optional[Guild]:
        return self.gateway.cache.get_guild(Snowflake(id))