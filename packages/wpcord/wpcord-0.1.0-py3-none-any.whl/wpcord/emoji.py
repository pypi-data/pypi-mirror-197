from datetime import datetime
from typing import Optional

import urllib.parse

from .snowflake import Snowflake
from .utils import JSONObject

class Emoji:
    def __init__(self,
        name: str,
        id: Optional[Snowflake] = None,
        animated: bool = False,
        *,
        available: bool = True,
        managed: bool = False,
        require_collons: bool = True,
        user: Optional[dict] = None
    ) -> None:
        self.name: str = name
        self.id: Optional[Snowflake] = Snowflake(id) if id is not None else None
        self.animated: bool = animated
        self.available: bool = available
        self.managed: bool = managed
        self.require_collons: bool = require_collons
        self.created_by: dict = user

    @property
    def created_at(self) -> datetime:
        return self.id.created_at

    @classmethod
    def from_str(cls, string: str):
        e = string.strip("<>").split(":")
        if 2 <= len(e) <= 3:
            if len(e) == 3:
                if e[0] == "a":
                    return cls(e[1], e[2], True)
                return cls(e[1], e[2])
        return cls(e[0])

    def partial_dict(self) -> JSONObject:
        return {
            "id": str(self.id) if self.id is not None else None,
            "name": self.name,
            "animated": self.animated
        }

    def __str__(self) -> str:
        if self.id is not None:
            if self.animated:
                return f"<a:{self.name}:{self.id}>"
            return f"<{self.name}:{self.id}>"
        return self.name
    
    @property
    def uri_encoded(self) -> str:
        return urllib.parse.quote(str(self).strip("<>"))