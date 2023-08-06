from __future__ import annotations
from datetime import datetime

from typing import TYPE_CHECKING, Any, Optional, List

from .cdn import *
from .channel import Channel
from .enums import MFALevel, Locale
from .member import Member
from .object import *
from .snowflake import Snowflake
from .utils import JSONObject, State, create_repr

class Guild(DiscordObject):
    def __init__(self,
        data: JSONObject,
        *,
        # Strings (Optional)
        joined_at:        Optional[str] = None,
        vanity_url_code:  Optional[str] = None,
        # Integers (Optional)
        default_message_notifications: int = 0,
        explicit_content_filter:       int = 0,
        max_video_channel_users:       int = 0,
        member_count:                  int = 0,
        nsfw_level:                    int = 0,
        premium_tier:                  int = 0,
        premium_subscription_count:    int = 0,
        system_channel_flags:          int = 1 << 0,
        verification_level:            int = 0,
        # Lists of objects (Optional)
        roles:                  list[JSONObject] = [],
        embedded_activities:    list[JSONObject] = [],
        emojis:                 list[JSONObject] = [],
        stickers:               list[JSONObject] = [],
        members:                list[JSONObject] = [],
        channels:               list[JSONObject] = [],
        threads:                list[JSONObject] = [],
        presences:              list[JSONObject] = [],
        stage_instances:        list[JSONObject] = [],
        guild_scheduled_events: list[JSONObject] = [],
        voice_states:           list[JSONObject] = [],
        # Objects (Optional)
        region:         Optional[JSONObject] = None,
        welcome_screen: Optional[JSONObject] = None,
        state: Optional[State] = None,
        _shard_id: Optional[int] = None,
        **kwargs
    ) -> None:
        super().__init__(data)
        unavailable = data.get("unavailable")
        self.unavailable: bool = unavailable if unavailable is not None else False
        self.shard_id: Optional[int] = _shard_id
        self._state = state

    @data()
    def name(self)        -> Optional[str]: "The guild's name"
    @data
    def description(self) -> Optional[str]: "The guild's description"
    
    @data_snowflake
    def afk_channel_id(self)            -> Optional[Snowflake]: "ID for the guild's AFK channel"
    @data_snowflake
    def application_id(self)            -> Optional[Snowflake]: "Application ID of the guild creator if it is bot-create"
    @data_snowflake
    def owner_id(self)                  -> Optional[Snowflake]: "ID of the guild's owner"
    @data_snowflake
    def public_updates_channel_id(self) -> Optional[Snowflake]: "The ID of the channel where admins and moderators of Community guilds receive notices from Discord"
    @data_snowflake
    def rules_channel_id(self)          -> Optional[Snowflake]: "The ID of the channel where Community guilds can display rules and/or guidelines"
    @data_snowflake
    def system_channel_id(self)         -> Optional[Snowflake]: "The ID of the channel where guild notices such as welcome messages and boost events are posted"
    @data_snowflake
    def widget_channel_id(self)         -> Optional[Snowflake]: "The channel ID that the widget will generate an invite to"

    @data
    def afk_timeout(self)                -> int:           "AFK timeout in seconds"
    afk_timeout.config(300)
    @data
    def approximate_member_count(self)   -> int:           "Approximate number of members in the guild\n\n*Returned from the `GET /guilds/<id>` endpoint when `with_counts` is :bool:`True`"
    approximate_member_count.config(0)
    @data
    def approximate_presence_count(self) -> int:           "Approximate number of non-offline members in the guild\n\n*Returned from the `GET /guilds/<id>` endpoint when `with_counts` is :bool:`True`"
    approximate_presence_count.config(0)
    @data
    def max_presences(self)              -> Optional[int]: "The maximum number of presences for the guild\n\n*`None` is always returned, apart from the largest of guilds"
    @data
    def max_video_channel_users(self)    -> int:           "Approximate number of non-offline members in the guild\n\n*Returned from the `GET /guilds/<id>` endpoint when `with_counts` is :bool:`True`"
    max_video_channel_users.config(0)
    @data
    def max_members(self)                -> int:           "The maximum number of members for the guild"
    max_members.config(500000)

    @data_enum
    def mfa_level(self)        -> MFALevel: "Required MFA level for the guild"
    mfa_level.config(0)
    @data_enum
    def preferred_locale(self) -> Locale:   "The preferred locale of a Community guild. Used in server discovery and notices from Discord, and sent in interactions"
    preferred_locale.config(0)

    @data
    def features(self) -> List[str]: "Enabled guild features"

    @data
    def large(self)                        -> bool: "`True` if this is considered a large guild"
    large.config(False)
    @data
    def premium_progress_bar_enabled(self) -> bool: "`True` if the guild has the boost progress bar enabled"
    large.config(False)
    @data
    def widget_enabled(self)               -> bool: "`True` if the server widget is enabled"
    widget_enabled.config(False)

    @data_custom
    def banner(self, hash: str) -> Optional[CDNImage]:
        if hash is not None:
            return DiscordCDN.guild_banner(guild_id = self.id, hash = hash)
    @data_custom
    def discovery_splash(self, hash: str) -> Optional[CDNImage]:
        """*Only present for guilds with the "DISCOVERABLE" feature"""
        if hash is not None:
            return DiscordCDN.guild_discovery_splash(guild_id = self.id, hash = hash)
    @data_custom
    def icon(self, icon: str) -> Optional[CDNImage]:
        hash = None
        if icon is not None:
            hash = icon
        else:
            hash = self._data.get("icon_hash")
        if hash is not None:
            return DiscordCDN.guild_icon(guild_id = self.id, hash = hash)
    @data_custom
    def splash(self, hash) -> Optional[CDNImage]:
        if hash is not None:
            return DiscordCDN.guild_splash(guild_id = self.id, hash = hash)

    @property
    def created_at(self) -> datetime:
        return self.id.created_at

    @property
    def channel_list(self) -> list[Channel]:
        return list(self.channels.values())

    @property
    def member_list(self) -> list[Member]:
        return list(self.members.values())

    def get_channel(self, id: int | str) -> Channel | None:
        return self.channels.get(int(id), None)

    def get_member(self, id: int | str) -> Member | None:
        return self.members.get(int(id), None)

    async def leave(self) -> None:
        await self._state.api.leave_guild(self.id)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return create_repr(self,
            id = self.id,
            name = self.name
        )