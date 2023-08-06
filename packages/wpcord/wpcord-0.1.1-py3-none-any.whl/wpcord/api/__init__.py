from datetime import datetime
import aiohttp
from typing import TYPE_CHECKING, Callable, Optional


from .__routes__ import APIRoute, APIRoutes
from ..components import Component
from ..embed import Embed
from ..enums import *
from ..http import HTTPClient, HTTPMethod, HTTPResults
from ..file import File
from ..guild import Guild
from ..message import AllowedMentions, Message, MessageReference
from ..snowflake import Snowflake
from ..utils import JSONObject, State, eor, hasarg
from ..exceptions import InvalidType

from . import (
    application_commands,
    receiving_and_responding,
    channel,
    guild,
    user,
)

__all__ = (
    "APIRoutes",
    "DiscordAPIClient"
)

class DiscordAPIClient:
    """
    Discord API Client
    ------------------
    A class for interacting with [Discord API](https://discord.com/developers/docs/reference) via HTTP requests.
    """
    def __init__(self,
        token: str = None,
        token_type: TokenType = TokenType.Bot,
        *,
        name: Optional[str] = None,
        api_version: int = 10,
        print_errors: bool = True,
        print_all_requests: bool = False,
        _state: Optional[State] = None,
        **http_options
    ) -> None:
        self._state: State = _state or State()
        if not 6 <= api_version <= 10:
            # https://discord.com/developers/docs/reference#api-versioning-api-versions
            raise ValueError("API version must be >= 6 and <= 10")
        self.name: Optional[str] = name
        self.api_version: int = api_version
        http_options.pop("convert_response", None) # It must be wpcord.HTTPResponse only
        self.http: HTTPClient = HTTPClient(f"https://discord.com/api/v{self.api_version}", **http_options)
        self.token: Optional[str] = token
        if self.token is None:
            self.token = self._state.token

        self.type: TokenType = token_type
        if isinstance(self.type, str) and TokenType.from_name(self.type.title()):
            self.type = TokenType.from_name(self.type.title())
        if not isinstance(self.type, TokenType):
            raise ValueError("Invalid token type")

        self.authorization: str = str(self.type) + token
        self._print_errors: bool = print_errors
        self._print_all_reqs: bool = print_all_requests

        self._state._api = self




    def _response(self, cls: object, *args, **kwargs):
        if hasarg(cls.__init__, "state"):
            return cls(*args, **kwargs, state = self._state)
        return cls(*args, **kwargs)

    async def request(self,
        *routes: APIRoute,
        reason: Optional[str] = None,
        content_type: Optional[str] = ...,
        **request_options
    ) -> HTTPResults:
        headers = request_options.pop("headers", {})
        headers.pop("content-type", None)
        content_type = eor(content_type, "application/json")
        if content_type is not None:
            headers["content-type"] = content_type
        if "X-Audit-Log-Reason" not in headers:
            headers["X-Audit-Log-Reason"] = str(reason)
        if "authorization" not in headers:
            headers["authorization"] = self.authorization
        r = {}
        for route in routes:
            if not isinstance(route, (APIRoute, APIRoutes)):
                raise InvalidType(route, "route", APIRoute, APIRoutes)
            if r:
                if route.method != r["method"]:
                    raise ValueError("All routes must have the same HTTP method")
            else:
                r["method"] = route.method
                r["paths"] = []
            r["paths"].append(route.path)
        if r["method"] not in (HTTPMethod.get, HTTPMethod.patch, HTTPMethod.post):
            headers.pop("content-type")

        request = await self.http.request(r["method"], *r["paths"], headers = headers, **request_options)
        result = request
        if not isinstance(request, list):
            request = [request]
        for index, req in enumerate(request):
            path = r["paths"][index]
            def log(success: bool):
                BOLD     = "\033[1m"
                END      = "\033[0m"
                SEP_LEN  = 41                if success else 36
                SOE      = "successful"      if success else "error"
                ST_COLOR = "\033[92m"        if success else "\033[91m"
                NAME     = f" ({self.name})" if self.name else ""

                print(
                    "-" * (SEP_LEN + len(NAME)),
                    f"{BOLD}[{datetime.now().strftime('%X')}] Discord API request {SOE}{NAME}{END}",
                    f"{BOLD}Route:{END} \033[93m\"{r['method']}\"{END}, \033[96m\"{path}\"{END}",
                    f"{BOLD}Status:{END} {ST_COLOR}{req.status}{END}",
                sep = "\n")

                if not success:
                    error = req.json()
                    if error is not None:
                        print(
                            f"{BOLD}Error code:{END} \033[31m{error['code']}{END}",
                            f"{BOLD}Error message:{END} {error['message']}",
                        sep = "\n")
                        print(error)

            if self._print_all_reqs and req.client_response.ok:
                log(True)
            if (self._print_errors or self._print_all_reqs) and not req.client_response.ok:
                log(False)

        return result



    

    async def send_message(self,
        channel_id: Snowflake,
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
    ) -> Optional[Message]: ...
    async def edit_message(self, 
        channel_id: Snowflake, 
        message_id: Snowflake,
        content: Optional[str] = ...,
        *,
        embed: Optional[Embed] = ...,
        embeds: list[Embed] = ...,
        file: Optional[str | File] = ...,
        files: list[str | File] = ...,
        components: list[Component] = ...,
        allowed_mentions: Optional[AllowedMentions] = ...,
        suppress_embeds: Optional[bool] = ...,
    ) -> Optional[Message]: ...
    async def delete_message(self, channel_id: Snowflake, message_id: Snowflake) -> None: ...


    async def get_guild(self, guild_id: Snowflake) -> Optional[Guild]: ...

    
    async def leave_guild(self, guild_id: Snowflake) -> None: ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, et, ev, t) -> None:
        await self.http.session.close()

for module in (
    application_commands,
    receiving_and_responding,
    channel,
    guild,
    user,
):
    for method in module.methods:
        setattr(DiscordAPIClient, method, getattr(module, method))
