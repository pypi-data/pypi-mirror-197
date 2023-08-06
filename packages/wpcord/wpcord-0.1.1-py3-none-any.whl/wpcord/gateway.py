from __future__ import annotations
import zlib

import aiohttp
import asyncio
import concurrent.futures._base
import json
import sys
import threading
import time

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union
)

from .enums import GatewayOpcode
from .events import Events
from .flags import Intents
from .guild import Guild
from .message import Message
from .snowflake import Snowflake
from .utils import JSONObject, State, eor, neor

__all__ = (
    "DiscordGatewayClient",
    "Shard"
)

class GatewayMessage(NamedTuple):
    op: GatewayOpcode
    d: Optional[Any] = None
    s: Optional[int] = None
    t: Optional[str] = None

    def to_dict(self) -> JSONObject:
        payload = {
            "op": int(self.op),
            "d": self.d
        }
        if self.s is not None:
            payload["s"] = self.s
        if self.t is not None:
            payload["t"] = self.t
        return payload

    def json(self) -> str:
        return json.dumps(self.to_dict())

class Shard(NamedTuple):
    id: int
    count: int



class GatewayCache:
    def __init__(self, gateway: "DiscordGatewayClient") -> None:
        self.gw: DiscordGatewayClient = gateway
        self.guilds: Dict[Snowflake, Guild] = {}
        self.messages: Dict[Snowflake, Message] = {}

    def set_guild(self, data: dict) -> Guild:
        guild = Guild(data, _state = self.gw._state)
        guild.shard_id = (guild.id >> 22) % self.gw.connection_count
        self.guilds[guild.id] = guild
        return guild

    def set_message(self, data: dict) -> Message:
        self.messages[int(data["id"])] = Message(**data, _state = self.gw._state)
        return self.get_message(int(data["id"]))

    def get_guild(self, id: Snowflake) -> Optional[Guild]:
        return self.guilds.get(int(id))

    def get_message(self, id: Snowflake) -> Optional[Message]:
        return self.messages.get(int(id))

class GatewayHeartbeat(threading.Thread):
    def __init__(self, connection: "GatewayConnection", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conn: GatewayConnection = connection
        self.event = threading.Event()
        self.last_send: float = None
        self.last_recieve: float = None

    async def send(self) -> None:
        await self.conn.send_msg(GatewayOpcode.heartbeat, self.conn.sequence)
        self.last_send = time.perf_counter()

    def ack(self) -> None:
        self.last_recieve = time.perf_counter()

    @property
    def latency(self) -> float:
        return self.last_recieve - self.last_send

    def run(self) -> None:
        while not self.event.wait(self.conn.heartbeat_interval):
            try:
                future = asyncio.run_coroutine_threadsafe(self.send(), self.conn.gw.loop)
                future.result(10)
            except concurrent.futures._base.TimeoutError:
                future = asyncio.run_coroutine_threadsafe(
                    self.conn.reconnect() if self.conn.gw._reconnect else self.conn.disconnect(),
                    self.conn.gw.loop
                )
                future.result()
                break

    def stop(self) -> None:
        self.event.set()





class DiscordGatewayClient:
    """
    Discord Gateway Client
    --------------------
    A class for interacting with [Discord Gateway](https://discord.com/developers/docs/topics/gateway) via WebSocket connections.
    
    Connections
    -----------
    A simple connection:
    >>> client = DiscordGatewayClient(...)

    Multiple connections with sharding:
    >>> client = DiscordGatewayClient(..., connection_count = ...)

    Multiple connections without sharding:
    >>> client = DiscordGatewayClient(..., connection_count = ..., sharding = False)
    """
    def __init__(self,
        token: str = None,
        intents: Optional[Intents] = ...,
        connection_count = 1,
        sharding: bool = True,
        api_version: int = 10,
        reconnect: bool = True,
        large_threshold: int = 250,
        zlib_compress: bool = True,
        zlib_decompress_obj: Optional[Any] = ...,
        session: Optional[aiohttp.ClientSession] = ...,
        loop: Optional[asyncio.AbstractEventLoop] = ...,
        _state: Optional[State] = None,
    ) -> None:
        self._state = _state or State()
        self.token: str = token
        if self.token is None:
            self.token = self._state.token
        self._session: aiohttp.ClientSession = neor(session, aiohttp.ClientSession())
        self.loop: asyncio.AbstractEventLoop = neor(loop, asyncio.get_event_loop())
        self.intents: Intents = eor(intents, Intents()) or Intents()
        if not 6 <= api_version <= 10:
            # https://discord.com/developers/docs/reference#api-versioning-api-versions
            raise ValueError("API version must be >= 6 and <= 10")
        self.connections: List[GatewayConnection] = []
        self.connection_count: int = connection_count
        if self.connection_count == 1:
            self.connections.append(GatewayConnection(self))
        else:
            for i in range(self.connection_count):
                self.connections.append(GatewayConnection(self, Shard(i, self.connection_count) if sharding else None))

        self.api_version: int = api_version
        self._reconnect: bool = reconnect
        self.large_threshold: int = large_threshold
        self.zlib_compress: bool = zlib_compress
        self.inflator = neor(zlib_decompress_obj, zlib.decompressobj())
        self.events: Events = Events(self.loop)
        self.cache: GatewayCache = GatewayCache(self)
        self._state._gateway = self

    def event(self, function: Callable) -> None:
        name = function.__name__.lower().replace("on_", "", 1)
        if name == "message":
            name += "_create"
        self.events.add_to_event(name, function)

    @property
    def avg_latency(self) -> float:
        return sum(conn.latency for conn in self.connections) / self.connection_count

    def run(self):
        for conn in self.connections:
            self.loop.create_task(conn.connect())
        self.loop.run_forever()



class GatewayConnection:
    def __init__(self, gateway: DiscordGatewayClient, shard: Optional[Union[Shard, Tuple[int, int]]] = None) -> None:
        self.gw: DiscordGatewayClient = gateway
        self.shard: Shard = Shard(*shard) if shard is not None else None
        
        self.base_url: str = "wss://gateway.discord.gg/"
        self._resume: bool = False
        self.heartbeat_interval: int = None
        self.session_id: str = None
        self.sequence: int = None
        self.ws: aiohttp.ClientWebSocketResponse = None
        self._run_event = self.gw.events.run_event
        self.cache = GatewayCache(self)
        self.heartbeat: GatewayHeartbeat = None
        self.buffer: bytearray = bytearray()

    @property
    def url(self):
        return f"{self.base_url}?v={self.gw.api_version}&encoding=json{'&compress=zlib-stream' if self.gw.zlib_compress else ''}"
    
    async def send_msg(self, opcode: GatewayOpcode, data: Optional[Any] = None) -> None:
        await self.ws.send_str(GatewayMessage(opcode, data).json())

    async def connect(self, **ws_connect_options) -> None:
        self.ws = await self.gw._session.ws_connect(self.url, autoclose = False, **ws_connect_options)
        self._run_event("connect")
        while True:
            await self.receive_message()
            
    async def identify(self) -> None:
        data = {
            "token": self.gw.token,
            "properties": {
                "$os": sys.platform,
                "$browser": "wpcord",
                "$device": "wpcord"
            },
            "intents": int(self.gw.intents),
            "large_threshold": self.gw.large_threshold,
            "compress": bool(self.gw.zlib_compress)
        }
        if self.shard is not None:
            data["shard"] = tuple(self.shard)

        await self.send_msg(GatewayOpcode.identify, data)

    async def resume(self) -> None:
        data = {
            "token": self.gw.token,
            "session_id": self.session_id,
            "seq": self.sequence
        }
        await self.send_msg(GatewayOpcode.resume, data)

    async def reconnect(self, resume: bool = True) -> None:
        self._run_event("reconnect")
        await self.disconnect()
        self._resume = resume
        await self.connect()

    async def disconnect(self, code: Optional[int] = None) -> None:
        self.heartbeat.stop()
        if code is None:
            code = aiohttp.WSCloseCode.OK
            if self.gw._reconnect:
                code = 4000
        await self.ws.close(code = code)
        self._run_event("disconnect")
    
    async def update_voice_state(self) -> None:
        data = {

        }
        await self.send_msg(GatewayOpcode.voice_state_update)

    @property
    def latency(self) -> float:
        return self.heartbeat.latency



    async def receive_message(self) -> None:
        msg = await self.ws.receive()

        if msg.type in (aiohttp.WSMsgType.BINARY, aiohttp.WSMsgType.TEXT):
            data = msg.data
            if self.gw.zlib_compress:
                self.buffer.extend(data)
                if len(data) >= 4 or data[-4:] == b'\x00\x00\xff\xff':
                    data = self.gw.inflator.decompress(self.buffer)
                self.buffer = bytearray()
            data = json.loads(data)
            data["op"] = GatewayOpcode.from_value(data["op"])
            await self.on_message_received(GatewayMessage(**data))

        elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
            code = int(self.ws.close_code)
            if code not in (1000, 4004, 4010, 4011, 4012, 4013, 4014):
                await self.reconnect()
            
    async def on_message_received(self, msg: GatewayMessage) -> None:
        self._run_event("gateway_message", msg)
        if msg.s is not None:
            self.sequence = msg.s

        if msg.op is GatewayOpcode.hello:
            self._run_event("hello")
            self.heartbeat_interval = msg.d["heartbeat_interval"] / 1000
            await self.resume() if self._resume else await self.identify()
            
            self.heartbeat = GatewayHeartbeat(self)
            self.heartbeat.start()

        elif msg.op is GatewayOpcode.heartbeat:
            # The gateway may request a heartbeat from the client in some situations by sending an Opcode 1 Heartbeat. 
            # When this occurs, the client should immediately send an Opcode 1 Heartbeat without waiting the remainder of the current interval.
            # https://discord.com/developers/docs/topics/gateway#connecting-to-the-gateway)      
            await self.heartbeat.send()

        elif msg.op is GatewayOpcode.reconnect:
            if self.gw._reconnect:
                await self.reconnect()

        elif msg.op is GatewayOpcode.heartbeat_ack:
            self.heartbeat.ack()
            self._run_event("heartbeat_ack")

        elif msg.op is GatewayOpcode.invalid_session:
            self._run_event("invalid_session")
            if self._resume and msg.d is False:
                await self.reconnect(False)
            else:
                await self.reconnect()

        elif msg.op is GatewayOpcode.dispatch:
            if msg.t == "READY":
                self.session_id = msg.d["session_id"]
                self.url = msg.d["resume_gateway_url"]
                for guild in msg.d["guilds"]:
                    if self.cache.get_guild(guild["id"]) is None:
                        self.cache.set_guild(guild)
            
            self.gw.events.from_gateway(self, msg.t, msg.d)