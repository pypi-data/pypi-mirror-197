from datetime import datetime
from typing import Optional

from .cdn import CDNImage, DiscordCDN
from .snowflake import Snowflake

class User:
    def __init__(self,
        id: Snowflake,
        *,
        username: Optional[str] = None,
        discriminator: Optional[str] = None,
        avatar: Optional[str] = None,
        bot: bool = False,

    ) -> None:
        self.id: Snowflake = Snowflake(id)

        self.username: Optional[str] = username
        self.discriminator: Optional[str] = discriminator
        self.avatar_hash: Optional[str] = avatar

    @property
    def avatar(self) -> CDNImage:
        return DiscordCDN.user_avatar(user_id = self.id, hash = self.avatar_hash)

    @property
    def default_avatar(self) -> CDNImage:
        return DiscordCDN.default_user_avatar(user_id = self.id, number = int(self.discriminator) % 5)

    @property
    def created_at(self) -> datetime:
        return self.id.created_at