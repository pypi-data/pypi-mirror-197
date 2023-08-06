from __future__ import annotations
import asyncio

from typing import TYPE_CHECKING, Coroutine

from .utils import JSON

if TYPE_CHECKING:
    from .gateway import DiscordGatewayClient

class Events:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop: asyncio.AbstractEventLoop = loop

        event_list = [
            "connect",
            "disconnect",
            "gateway_message",
            "heartbeat_ack",
            "hello",
            "invalid_session",
            "ready",
            "reconnect",
            "resumed",

            "application_command_permissions_update",
            "auto_moderation_command_execution ",
            "auto_moderation_rule_create",
            "auto_moderation_rule_delete",
            "auto_moderation_rule_update",
            "channel_create",
            "channel_delete",
            "channel_pins_update",
            "channel_update",
            "guild_join",
            "guild_available",
            "thread_create",
            "thread_delete",
            "thread_update",
            "message_create",
            "message_delete",
            "message_update",
        ]

        for event in event_list:
            setattr(self, event, [])
    
    def add_to_event(self, event_name: str, func: Coroutine) -> None:
        try:
            event: list = getattr(self, event_name.lower())
            event.append(func)
            setattr(self, event_name.lower(), event)
        except AttributeError as e:
            raise ValueError(f"Invalid event name: {event_name}") from e
    
    def run_event(self, name: str, *args) -> None:
        try:
            functions = getattr(self, name.lower())
        except AttributeError as e:
            raise ValueError(f"Invalid event name: {name}") from e
        else:
            for function in functions:
                if asyncio.iscoroutinefunction(function):
                    self.loop.create_task(function(*args))
                else:
                    function(*args)



    def from_gateway(self, gateway: DiscordGatewayClient, event: str, data: JSON) -> None:
        if event in (
            "READY",
            "RESUMED"
        ):
            self.run_event(event)

        elif event == "GUILD_CREATE":
            unavailable = data.get("unavailable")
            if unavailable is not True:
                g = gateway.cache.set_guild(data)
                self.run_event("guild_available" if unavailable is False else "guild_join", g)

        elif event == "GUILD_UPDATE":
            old = gateway.cache.get_guild(data["id"])
            new = gateway.cache.set_guild(data)
            self.run_event(event, old, new)

        elif event == "GUILD_DELETE":
            g = gateway.cache.get_guild(data["id"])
            g.unavailable = True
            self.run_event(event, g)

        elif event == "MESSAGE_CREATE":
            msg = gateway.cache.set_message(data)
            self.run_event(event, msg)