from __future__ import annotations
import aiohttp
import json

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, NamedTuple, Optional, Union

from .channel import Channel, ChannelBase
from .components import ActionRow, Component
from .embed import Embed
from .enums import ComponentType, MessageFlag
from .exceptions import InvalidType
from .file import File
from .guild import Guild
from .snowflake import Snowflake
from .utils import JSONObject, State

__all__ = (
    "AllowedMentions",
    "Message",
    "MessageReference"
)

class AllowedMentions:
    def __init__(self,
        user: bool = True,
        role: bool = True,
        everyone: bool = True,
        replied_user: bool = True,
        users: Optional[list[Snowflake]] = None,
        roles: Optional[list[Snowflake]] = None
    ) -> None:
        self.user: bool = user
        self.role: bool = role
        self.everyone: bool = everyone
        self.replied_user = replied_user
        self.users = [Snowflake(id) for id in users] if users is not None else None
        self.roles = [Snowflake(id) for id in roles] if roles is not None else None

    def to_dict(self) -> JSONObject:
        payload = {
            "replied_user": not self.replied_user
        }
        parse = {name: getattr(self, name) for name in ("users", "roles", "everyone")}
        if False in parse.values():
            payload["parse"] = [i for i in parse if parse[i]]
        if self.users is not None:
            payload["users"] = [str(id) for id in self.users]
        if self.roles is not None:
            payload["roles"] = [str(id) for id in self.roles]

        return payload

class MessageReference:
    def __init__(self,
        message_id: Snowflake,
        channel_id: Snowflake,
        guild_id: Optional[Snowflake] = None,
        fail_if_not_exists: bool = True,
        mention_author: bool = True,
        _reply_author_id: Optional[Snowflake] = None
    ) -> None:
        self.message_id: Snowflake = Snowflake(message_id)
        self.channel_id: Snowflake = Snowflake(channel_id)
        self.guild_id: Optional[Snowflake] = Snowflake(guild_id) if guild_id is not None else None
        self.fail_if_not_exists = fail_if_not_exists
        self.mention_author: bool = mention_author
        self._reply_author_id: Optional[Snowflake] = Snowflake(_reply_author_id) if _reply_author_id is not None else None

    def to_dict(self) -> JSONObject:
        payload = {
            "message_id": str(self.message_id),
            "channel_id": str(self.channel_id),
            "fail_if_not_exists": self.fail_if_not_exists
        }
        if self.guild_id is not None:
            payload["guild_id"] = str(self.guild_id)
        return payload



class Message:
    def __init__(self,
        # Required
        id: Snowflake, *,
        # Strings (Optional)
        content:          Optional[str] = None,
        edited_timestamp: Optional[str] = None,
        timestamp:        Optional[str] = None,
        # Booleans (Optional)
        mention_everyone: bool = False,
        pinned:           bool = False,
        tts:              bool = False,
        # Objects (Optional)
        activity:           Optional[JSONObject] = None,
        application:        Optional[JSONObject] = None,
        author:             Optional[JSONObject] = None,
        interaction:        Optional[JSONObject] = None,
        message_reference:  Optional[JSONObject] = None,
        referenced_message: Optional[JSONObject] = None,
        thread:             Optional[JSONObject] = None,
        # Lists of objects (Optional)
        attachments:      list[JSONObject] = [],
        embeds:           list[JSONObject] = [],
        components:       list[JSONObject] = [],
        mention_channels: list[JSONObject] = [],
        mention_roles:    list[JSONObject] = [],
        mentions:         list[JSONObject] = [],
        reactions:        list[JSONObject] = [],
        stickers:         list[JSONObject] = [],
        sticker_items:    list[JSONObject] = [],
        # Integers (Optional)
        flags:    int = 0,
        position: Optional[int] = None,
        type:     int = 0,
        # Snowflakes (Optional)
        application_id: Optional[Snowflake] = None,
        channel_id:     Optional[Snowflake] = None,
        guild_id:       Optional[Snowflake] = None,
        webhook_id:     Optional[Snowflake] = None,

        state: Optional[State] = None,
        **kwargs
    ) -> None:
        self.id: Snowflake = Snowflake(id)
        self._state = state

        self.content: str = content or ""
        self.created_at: datetime = datetime.fromisoformat(timestamp) if timestamp is not None else self.id.created_at
        self.edited_at: datetime = datetime.fromisoformat(edited_timestamp) if edited_timestamp is not None else None

        self.tts: bool = tts
        self.pinned: bool = pinned
        self.mention_everyone: bool = mention_everyone
        
        self.channel_id: Optional[Snowflake] = Snowflake(channel_id) if channel_id is not None else None
        self.channel: Optional[Channel] = None
        if self.channel_id is not None and self._state.client is not None:
            self.channel = self._state.client.get_channel(self.guild_id)

        self.guild_id: Optional[Snowflake] = Snowflake(guild_id) if guild_id is not None else None
        self.guild: Optional[Guild] = None
        if self.guild_id is not None and self._state.client is not None:
            self.guild = self._state.client.get_guild(self.guild_id)

    async def delete(self):
        return await self._state.api.delete_message(self.channel_id, self.id)

    async def reply(self, content):
        return await self.channel.send_message(
            content = content,
            reference = {
                "message_id": str(self.id),
                "channel_id": str(self.channel_id),
            }
        )





def to_dict_or_multipart(
    content: Optional[str] = None,
    embed: Optional[Embed] = None,
    embeds: List[Embed] = [],
    file: Optional[Union[str, File]] = None,
    files: List[Union[str, File]] = [],
    components: List[Component] = [],
    allowed_mentions: Optional[AllowedMentions] = None,
    reference: Optional[Union[MessageReference, JSONObject]] = None,
    suppress_embeds: bool = False,
    sticker: Optional[Snowflake] = None,
    tts: bool = False,
    editing: bool = False,
) -> JSONObject | aiohttp.FormData:
    payload: JSONObject = {}
    if content is not None:
        payload["content"] = str(content)
    elif editing and content is not ...:
        payload["content"] = None
    if file is not None:
        files.insert(0, file)
    
    if embed is not None:
        embeds.insert(0, embed)
    for embed in embeds:
        if "embeds" not in payload:
            payload["embeds"] = []
        for _file in embed._files:
            files.append(_file)
        payload["embeds"].append(embed.to_dict())
    embeds.clear()
    
    if components:
        action_rows: List[ActionRow] = []
        for component in components:
            if isinstance(component, ActionRow):
                action_rows.append(component)
        _ = False
        for component in [c for c in components if c.type is not ComponentType.action_row]:
            if component.type is ComponentType.select_menu:
                action_rows.append(ActionRow(select_menu = component))
            if component.type is ComponentType.button:
                if (
                    _ is False or
                    not components or
                    component.next_row or
                    (
                        action_rows and
                        (action_rows[0].components[0].type is ComponentType.select_menu or len(action_rows[-1].components) == 5)
                    )
                ):
                        action_rows.append(ActionRow())
                action_rows[-1].add_component(component)
            if len(action_rows) > 5:
                raise ValueError("Limit of action rows is 5")
            _ = True     
        payload["components"] = [action_row.to_dict() for action_row in action_rows]
    elif editing and components is not ...:
        payload["components"] = []

    if reference is not None:
        if isinstance(reference, dict):
            reference = MessageReference(**reference)
        payload["message_reference"] = reference.to_dict()
        if allowed_mentions is None:
            allowed_mentions = AllowedMentions()
        allowed_mentions.replied_user = reference.mention_author
    elif editing and reference is not ...:
        payload["message_reference"] = None

    if allowed_mentions is not None:
        payload["allowed_mentions"] = allowed_mentions.to_dict()
    elif editing and allowed_mentions is not ...:
        payload["allowed_mentions"] = None

    if sticker is not None:
        payload["sticker_ids"] = [str(Snowflake(sticker))]

    if suppress_embeds is not ...:
        payload["tts"] = tts

    if suppress_embeds is not ...:
        payload["flags"] = int(MessageFlag.suppress_embeds) if suppress_embeds else 0

    if files or (editing and files is not ...):
        form = aiohttp.FormData()
        for index, file in enumerate(files):
            if isinstance(file, str):
                file = File(file)
            if not isinstance(file, File):
                raise InvalidType(file, "*files item", str, File)
            if "attachments" not in payload:
                payload["attachments"] = []
            attachment = {
                "id": index,
                "filename": file.name
            }
            if file.description is not None:
                attachment["description"] = file.description
            payload["attachments"].append(attachment)
            form.add_field(
                name = f"files[{index}]",
                value = file.bytes,
                content_type = "application/octet-stream",
                filename = file.name
            )
        form.add_field("payload_json", json.dumps(payload))
        files.clear()
        return form
    return payload