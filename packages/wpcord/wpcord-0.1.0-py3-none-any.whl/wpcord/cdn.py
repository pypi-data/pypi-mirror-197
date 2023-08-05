from typing import Optional, Self

from .enums import ImageFormat, WPCordEnum

__all__ = (
    "CDNImage",
    "DiscordCDN"
)



class CDNImage:
    def __init__(self, endpoint: str, support_formats: tuple[str], **options) -> None:
        self.endpoint: str = endpoint.format(**options)
        self.hash: Optional[str] = options.get("hash")
        self.size = 1024
        self.format = ImageFormat.PNG
        if self.hash is not None and "GIF" in support_formats and self.hash.startswith("a_"):
            self.format = ImageFormat.GIF

    @property
    def url(self) -> str:
        return f"https://cdn.discordapp.com{self.endpoint}.{self.format}?size={self.size}"

    def __call__(self, size: int = 1024, format = ImageFormat.PNG) -> Self:
        self.size = size
        if isinstance(format, str):
            format = ImageFormat.from_value(format)
        self.format = format
        return self

    def __str__(self) -> str:
        return self.url

class DiscordCDN(WPCordEnum):
    def __call__(self, **parameters) -> CDNImage:
        return CDNImage(*self.value, **parameters)

    custom_emoji                = "/emojis/{emoji_id}",                                                      ("PNG", "JPEG", "WEBP", "GIF")
    guild_icon                  = "/icons/{guild_id}/{hash}",                                                ("PNG", "JPEG", "WEBP", "GIF")
    guild_splash                = "/splashes/{guild_id}/{hash}",                                             ("PNG", "JPEG", "WEBP"       )
    guild_discovery_splash      = "/discovery-splashes/{guild_id}/{hash}",                                   ("PNG", "JPEG", "WEBP"       )
    guild_banner                = "/banners/{guild_id}/{hash}",                                              ("PNG", "JPEG", "WEBP", "GIF")
    user_banner                 = "/banners/{user_id}/{hash}",                                               ("PNG", "JPEG", "WEBP", "GIF")
    default_user_avatar         = "/embeds/avatars/{number}",                                                ("PNG"                       )
    user_avatar                 = "/avatars/{user_id}/{hash}",                                               ("PNG", "JPEG", "WEBP", "GIF")
    guild_member_avatar         = "/guilds/{guild_id}/users/{user_id}/avatars/{hash}",                       ("PNG", "JPEG", "WEBP", "GIF")
    application_icon            = "/app-icons/{application_id}/{hash}",                                      ("PNG", "JPEG", "WEBP"       )
    application_cover           = "/app-icons/{application_id}/{hash}",                                      ("PNG", "JPEG", "WEBP"       )
    application_asset           = "/app-assets/{application_id}/{asset_id}",                                 ("PNG", "JPEG", "WEBP"       )
    achievment_icon             = "/app-assets/{application_id}/achievements/{achievement_id}/icons/{hash}", ("PNG", "JPEG", "WEBP"       )
    sticker_pack_banner         = "/app-assets/710982414301790216/store/{sticker_pack_banner_asset_id}",     ("PNG", "JPEG", "WEBP"       )
    team_icon                   = "/team-icons/{team_id}/{hash}",                                            ("PNG", "JPEG", "WEBP"       )
    sticker                     = "/stickers/{sticker_id}",                                                  ("PNG", "LOTTIE"             )
    role_icon                   = "/role-icons/{role_id}/{hash}",                                            ("PNG", "JPEG", "WEBP"       )
    guild_scheduled_event_cover = "/guild-events/{scheduled_event_id}/{hash}",                               ("PNG", "JPEG", "WEBP"       )
    guild_member_banner         = "/guilds/{guild_id}/users/{user_id}/banners/{hash}",                       ("PNG", "JPEG", "WEBP", "GIF")

    def __str__(self) -> str:
        return self.value[0]