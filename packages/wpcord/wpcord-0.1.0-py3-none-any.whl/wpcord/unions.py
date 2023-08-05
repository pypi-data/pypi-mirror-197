from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Tuple, Union

if TYPE_CHECKING:
    from .enums import ColorEnum
    from .file import File
    from .gateway import Shard

ColorUnion = Union[int, "ColorEnum", Tuple[int, int, int], Dict[str, int]]
FileUnion  = Union["File", str]
ShardUnion = Union["Shard", Tuple[int, int]]