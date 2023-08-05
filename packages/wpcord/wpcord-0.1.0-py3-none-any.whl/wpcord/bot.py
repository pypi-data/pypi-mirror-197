from .client import Client
from .enums import TokenType

class Bot(Client):
    def __init__(self, token: str, **kwargs) -> None:
        super().__init__(token, TokenType.Bot, **kwargs)