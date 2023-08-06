from datetime import datetime

from .enums import TimestampStyle
from .utils import discord_timestamp

__all__ = (
    "Snowflake",
)

DISCORD_EPOCH = 1420070400000

class Snowflake(int):
    @property
    def timestamp_ms(self) -> int:
        return (self >> 22) + DISCORD_EPOCH

    @property
    def timestamp(self) -> float:
        return self.timestamp_ms / 1000
    
    @property
    def created_at(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

    @property
    def internal_worker(self) -> int:
        return (self & 0x3E0000) >> 17

    @property
    def internal_process(self) -> int:
        return (self & 0x1F000) >> 12
    
    @property
    def increment(self) -> int:
        return self & 0xFFF
    
    def discord_timestamp(self, style: TimestampStyle = TimestampStyle.default) -> str:
        return discord_timestamp(self.timestamp, style)

    @classmethod
    def from_timestamp_ms(cls, timestamp_ms: int):
        return cls(int(timestamp_ms - DISCORD_EPOCH) << 22)

    @classmethod
    def from_timestamp(cls, timestamp: float):
        return cls.from_timestamp_ms(timestamp * 1000)