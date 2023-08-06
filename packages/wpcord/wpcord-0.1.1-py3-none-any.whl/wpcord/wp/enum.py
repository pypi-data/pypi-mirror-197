import enum
from typing import Any, Dict, List, Optional, Self, Tuple

class Enum(enum.Enum):
    @classmethod
    def from_name(cls, name: str) -> Optional[Self]:
        for item in cls:
            if item.name == name:
                return item

    @classmethod
    def from_value(cls, value: Any):
        for item in cls:
            if item.value == value:
                return item
    
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
        
    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __str__(self) -> str:
        return self.name

