from __future__ import annotations

from datetime import datetime

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Union,
    overload
)

from .enums import *

if TYPE_CHECKING:
    from .api import DiscordAPIClient
    from .client import Client
    from .gateway import DiscordGatewayClient

JSONObject = Dict[str, Any]
JSON = Union[List[Any], JSONObject]

class State:
    def __init__(self,
        token: Optional[str] = None,
        api: Optional[DiscordAPIClient] = None,
        gateway: Optional[DiscordGatewayClient] = None,
        client: Optional[Client] = None
    ) -> None:
        self._token, self._api, self._gateway, self.client = token, api, gateway, client
    
    @property
    def api(self):
        if self._api:
            return self._api
        if self.client:
            return self.client.api

    @property
    def gateway(self) -> Optional[DiscordGatewayClient]:
        if self._gateway:
            return self._gateway
        if self.client:
            return self.client.gateway

    @property
    def token(self) -> Optional[str]:
        if self._token:
            return self._token
        if self.client:
            return self.client.token
        if self.api:
            return self.api.token
        if self.gateway:
            return self.gateway.token

def eor(obj, default):
    if obj is ...:
        return default
    return obj

def neor(obj, default):
    obj = eor(obj, default)
    if obj is None:
        return default
    return obj

def create_repr(instance, **options) -> str:
    return "<{} {}>".format(
        type(instance).__name__,
        " ".join(f'{key}="{value}"' for key, value in options.items())
    )

def hasarg(func: Callable, arg: str) -> bool:
    return arg in func.__code__.co_varnames

def get_from_list(sequence: Sequence[Any], condition: Callable[[Any], bool]) -> Any:
    for item in sequence:
        if condition(item):
            return item

def lstrip_word(text: str, word: str, max_strip: int = -1):
    count = 0
    while max_strip != count and text.startswith(word):
        text = text[len(word):]
        count += 1
    return text

def rstrip_word(text: str, word: str, max_strip: int = -1):
    count = 0
    while max_strip != count and text.endswith(word):
        text = text[:-len(word)]
        count += 1
    return text

def strip_word(text: str, word: str, max_strip: int = -1):
    return lstrip_word(rstrip_word(text, word, max_strip), word, max_strip)

    
@overload
def discord_timestamp(timestamp: Union[int, float, str], style: str | TimestampStyle = TimestampStyle.default) -> str: ...
@overload
def discord_timestamp(date_time: datetime, style: str | TimestampStyle = TimestampStyle.default) -> str: ...
def discord_timestamp(ts_or_dt: Union[int, float, str, datetime], style: str | TimestampStyle = TimestampStyle.default) -> str:
    if not isinstance(style, TimestampStyle) and not TimestampStyle.from_value(str(style)):
        raise ValueError(f"Invalid timestamp style: {style}")
        # https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
    if isinstance(ts_or_dt, datetime):
        ts_or_dt = round(ts_or_dt.timestamp())
    try:
        return f"<t:{round(float(ts_or_dt))}:{str(style)}>"
    except ValueError as e:
        raise ValueError("Invalid timestamp") from e