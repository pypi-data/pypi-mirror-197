from .object import *
from .utils import JSONObject

class Role(DiscordObject):
    def __init__(self, data: JSONObject) -> None:
        super().__init__(data)