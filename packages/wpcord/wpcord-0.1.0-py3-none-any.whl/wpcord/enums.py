from enum import Enum
from typing import Any, Dict, List, Tuple

__all__ = (
    "ButtonStyle",
    "ChannelType",
    "ColorEnum",
    "ComponentType",
    "ImageFormat",
    "Intent",
    "MessageFlag",
    "Permission",
    "TimestampStyle",
    "TokenType"
)

class WPCordEnum(Enum):
    @classmethod
    def from_name(cls, name: str):
        d = {c.name: c for c in cls}
        return d.get(name)

    @classmethod
    def from_value(cls, value: Any):
        d = {c.value: c for c in cls}
        return d.get(value)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        return {c.name: c.value for c in cls}

    @classmethod
    def items(cls) -> Tuple[str, Any]:
        return cls.to_dict().items()

    @classmethod
    def names(cls) -> List[str]:
        return [c.name for c in cls]

    @classmethod
    def values(cls) -> List[str]:
        return [c.value for c in cls]

    @classmethod
    def __getitem__(cls, name: str):
        return cls.from_name(name)
        
    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __str__(self) -> str:
        return str(self.value)  

WE = WPCordEnum

class WEN(WE):
    def __str__(self) -> str:
        return self.name



class ButtonStyle(WEN):
    primary   = 1
    secondary = 2
    success   = 3
    danger    = 4
    link      = 5

class ChannelType(WEN):
    text           = 0
    dm             = 1
    voice          = 2
    dm_group       = 3
    category       = 4
    news           = 5
    news_thread    = 10
    public_thread  = 11
    private_thread = 12
    stage          = 13
    directory      = 14
    forum          = 15

class ColorEnum(WEN):
    aqua    = 0x00FFFF
    black   = 0x000000
    blue    = 0x0000FF
    green   = 0x00FF00
    magenta = 0xFF00FF
    red     = 0xFF0000
    white   = 0xFFFFFF
    yellow  = 0xFFFF00

class ComponentType(WEN):
    action_row  = 1
    button      = 2
    select_menu = 3
    text_input  = 4

class GatewayOpcode(WEN):
    dispatch              = 0
    heartbeat             = 1
    identify              = 2
    presence_update       = 3
    voice_state_update    = 4
    resume                = 6
    reconnect             = 7
    request_guild_members = 8
    invalid_session       = 9
    hello                 = 10
    heartbeat_ack         = 11

class ImageFormat(WE):
    PNG    = "png"
    JPG    = "jpg"
    JPEG   = "jpg"
    GIF    = "gif"
    WebP   = "webp"
    Lottie = "json"

class Intent(WEN):
    guilds                        = 1 << 0
    guild_members                 = 1 << 1
    guild_bans                    = 1 << 2
    guild_emojis_and_stickers     = 1 << 3
    guild_integrations            = 1 << 4
    guild_webhooks                = 1 << 5
    guild_invites                 = 1 << 6
    guild_voice_states            = 1 << 7
    guild_presences               = 1 << 8
    guild_messages                = 1 << 9
    guild_message_reactions       = 1 << 10
    guild_message_typing          = 1 << 11
    direct_messages               = 1 << 12
    direct_message_reactions      = 1 << 13
    direct_message_typing         = 1 << 14
    message_content               = 1 << 15
    guild_sheduled_events         = 1 << 16
    auto_moderation_configuration = 1 << 20
    auto_moderation_execution     = 1 << 21

class Locale(WEN):
    Danish               = "da"
    German               = "de"
    English_UK           = "en-UK"
    English_US           = "en-US"
    Spanish              = "es-ES"
    French               = "fr"
    Croatian             = "hr"
    Italian              = "it"
    Lithuanian           = "lt"
    Hungarian            = "hu"
    Dutch                = "nl"
    Norwegian            = "no"
    Polish               = "pl"
    Portuguese_Brazilian = "pt-BR"

class MessageFlag(WEN):
    crossposted                            = 1 << 0
    is_crosspost                           = 1 << 1
    suppress_embeds                        = 1 << 2
    source_message_deleted                 = 1 << 3
    urgent                                 = 1 << 4
    has_thread                             = 1 << 5
    ephemeral                              = 1 << 6
    loading                                = 1 << 7
    failed_to_metnion_some_roles_in_thread = 1 << 8

class MFALevel(WEN):
    none = 0
    elevated = 1

class Permission(WEN):
    create_instant_invite      = 1 << 0
    kick_members               = 1 << 1
    ban_members                = 1 << 2
    administrator              = 1 << 3
    manage_channels            = 1 << 4
    manage_guild               = 1 << 5
    add_reactions              = 1 << 6
    view_audit_log             = 1 << 7
    priority_speaker           = 1 << 8
    stream                     = 1 << 9
    view_channel               = 1 << 10
    send_messages              = 1 << 11
    send_tts_messages          = 1 << 12
    manage_messages            = 1 << 13
    embed_links                = 1 << 14
    attach_files               = 1 << 15
    read_message_history       = 1 << 16
    mention_everyone           = 1 << 17
    use_external_emojis        = 1 << 18
    view_guild_insights        = 1 << 19
    connect                    = 1 << 20
    speak                      = 1 << 21
    mute_members               = 1 << 22
    deafen_members             = 1 << 23
    move_members               = 1 << 24
    use_vad                    = 1 << 25
    change_nickname            = 1 << 26
    manage_nicknames           = 1 << 27
    manage_roles               = 1 << 28
    manage_webhooks            = 1 << 29
    manage_emojis_and_stickers = 1 << 30
    use_application_commands   = 1 << 31
    request_to_speak           = 1 << 32
    manage_events              = 1 << 33
    manage_threads             = 1 << 34
    create_public_threads      = 1 << 35
    create_private_threads     = 1 << 36
    use_external_stickers      = 1 << 37
    send_messages_in_threads   = 1 << 38
    use_embedded_activities    = 1 << 39
    moderate_members           = 1 << 40
    
class TimestampStyle(WE):
    short_time      = "t"
    long_time       = "T"
    short_date      = "d"
    long_date       = "D"
    short_date_time = "f" # Default
    long_date_time  = "F"
    relative_time   = "R"

    default = short_date_time

class TokenType(WE):
    User   = ""
    Bot    = "Bot "
    Bearer = "Bearer "