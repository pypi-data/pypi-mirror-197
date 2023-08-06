from typing import (
    Callable,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Type,
    Union,
    overload
)

from .enums import (
    Intent,
    Permission,
    WPCordEnum
)
from .exceptions import InvalidType

class value:
    def __init__(self, func: Callable) -> None:
        self.__doc__ = func.__doc__
        self.value = func(None)
        if self.value is None:
            self.value = func.__name__
    
    def __get__(self, instance: Optional["Flag"], owner: Optional[Type["Flag"]]) -> bool:
        if instance is None:
            return self
        return instance._check(self.value, instance._default_check)

    def __set__(self, instance: "Flag", toggle) -> None:
        if instance is None:
            return self
        instance._set(self.value, toggle)

class Flag:
    """

    """
    _values: Dict[str, int]
    _default_check: bool = True
    def __init__(self, total: int = 0, **values: bool) -> None:
        self.total: int = total
        for name, value in values.items():
            if name not in self._values:
                raise ValueError(f"Invalid flag value: {name}")
            if not isinstance(value, bool):
                raise InvalidType(value, "value", bool)
            self._set(name, value)
        
    
    @classmethod
    def all(cls):
        instance = cls()
        for name in cls._values:
            instance._set(name, True)
        return instance

    @overload
    def _check(self, name: str, true_or_false: bool = True) -> bool: ...
    @overload
    def _check(self, value: int, true_or_false: bool = True) -> bool: ...
    def _check(self, nv: str | int, true_or_false: bool = True) -> bool:
        if not self._default_check and true_or_false:
            true_or_false = False
        value = self.__to_value(nv)
        return ((self.total & value) == value) is true_or_false

    @overload
    def _set(self, name: str, toggle: bool) -> None: ...
    @overload
    def _set(self, value: int, toggle: bool) -> None: ...
    def _set(self, nv: Union[str, int], toggle: bool) -> None:
        if not isinstance(toggle, bool):
            raise InvalidType(toggle, "toggle", bool)
        value = self.__to_value(nv)
        if toggle:
            self.total |= value
        else:
            self.total &= ~value

    def __to_value(self, nv: Union[str, int]) -> int:
        if isinstance(nv, int):
            value = nv
        else:
            value = self._values.get(str(nv))
        if value is None:
            raise ValueError(f"Invalid flag value: {nv}")
        return int(value)

    def __getitem__(self, name: str) -> bool:
        return self._check(str(name), self._default_check)

    def __contains__(self, name: str) -> bool:
        return self._check(str(name), self._default_check)

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        for name in self._values:
            yield (name, self._check(name), self._default_check)

    def __int__(self) -> int:
        return self.total

class Intents(Flag):
    _values = Intent.to_dict()
    @value
    def guilds(self)                        -> bool: ""
    @value
    def guild_members(self)                 -> bool: ""
    @value
    def guild_bans(self)                    -> bool: ""
    @value
    def guild_emojis_and_stickers(self)     -> bool: ""
    @value
    def guild_integrations(self)            -> bool: ""
    @value
    def guild_webhooks(self)                -> bool: ""
    @value
    def guild_invites(self)                 -> bool: ""
    @value
    def guild_voice_states(self)            -> bool: ""
    @value
    def guild_presences(self)               -> bool: ""
    @value
    def guild_messages(self)                -> bool: ""
    @value
    def guild_message_reactions(self)       -> bool: ""
    @value
    def guild_message_typing(self)          -> bool: ""
    @value
    def direct_messages(self)               -> bool: ""
    @value
    def direct_message_reactions(self)      -> bool: ""
    @value
    def direct_message_typing(self)         -> bool: ""
    @value
    def message_content(self)               -> bool: ""
    @value
    def guild_sheduled_events(self)         -> bool: ""
    @value
    def auto_moderation_configuration(self) -> bool: "Test"
    @value
    def auto_moderation_execution(self)     -> bool: ""

class Permissions(Flag):
    _values = Permission.to_dict()
    @value
    def create_instant_invite(self)      -> bool: "Allows creation of instant invites"
    @value
    def kick_members(self)               -> bool: "Allows kicking members"
    @value
    def ban_members(self)                -> bool: "Allows banning members"
    @value
    def administrator(self)              -> bool: "Allows all permissions and bypasses channel permission overwrites"
    @value
    def manage_channels(self)            -> bool: "Allows management and editing of channels"
    @value
    def manage_guild(self)               -> bool: "Allows management and editing of the guild"
    @value
    def add_reactions(self)              -> bool: "Allows for the addition of reactions to messages"
    @value
    def view_audit_log(self)             -> bool: "Allows for viewing of audit logs"
    @value
    def priority_speaker(self)           -> bool: "Allows for using priority speaker in a voice channel"
    @value
    def stream(self)                     -> bool: "Allows the user to go live"
    @value
    def view_channel(self)               -> bool: "Allows guild members to view a channel, which includes reading messages in text channels and joining voice channels"
    @value
    def send_messages(self)              -> bool: ""
    @value
    def send_tts_messages(self)          -> bool: ""
    @value
    def manage_messages(self)            -> bool: ""
    @value
    def embed_links(self)                -> bool: ""
    @value
    def attach_files(self)               -> bool: ""
    @value
    def read_message_history(self)       -> bool: ""
    @value
    def mention_everyone(self)           -> bool: ""
    @value
    def use_external_emojis(self)        -> bool: ""
    @value
    def view_guild_insights(self)        -> bool: ""
    @value
    def connect(self)                    -> bool: ""
    @value
    def speak(self)                      -> bool: ""
    @value
    def mute_members(self)               -> bool: ""
    @value
    def deafen_members(self)             -> bool: ""
    @value
    def move_members(self)               -> bool: ""
    @value
    def use_vad(self)                    -> bool: ""
    @value
    def change_nickname(self)            -> bool: ""
    @value
    def manage_nicknames(self)           -> bool: ""
    @value
    def manage_roles(self)               -> bool: ""
    @value
    def manage_webhooks(self)            -> bool: ""
    @value
    def manage_emojis_and_stickers(self) -> bool: ""
    @value
    def use_application_commands(self)   -> bool: ""
    @value
    def request_to_speak(self)           -> bool: ""
    @value
    def manage_events(self)              -> bool: ""
    @value
    def manage_threads(self)             -> bool: ""
    @value
    def create_public_threads(self)      -> bool: ""
    @value
    def create_private_threads(self)     -> bool: ""
    @value
    def use_external_stickers(self)      -> bool: ""
    @value
    def send_messages_in_threads(self)   -> bool: ""
    @value
    def use_embedded_activities(self)    -> bool: ""
    @value
    def moderate_members(self)           -> bool: ""