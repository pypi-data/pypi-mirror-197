from typing import Any, Callable, Literal, Optional, Type

from . import enums, flags
from .snowflake import Snowflake
from .utils import JSONObject

__all__ = (
    "DiscordObject",
    "data",
    "data_enum",
    "data_flag",
    "data_snowflake",
    "data_custom"
)

class DiscordObject:
    def __init__(self, data: JSONObject) -> None:
        self._data: JSONObject = data
        self.id: Snowflake = Snowflake(data["id"])
        self._data_saved: dict[str, Any] = {}

class data(property):
    option = None
    def __init__(self, default = None, name = None):
        self.default = default
        self.name = name
        
    def __call__(self, func: Callable) -> None:
        self.func = func
        self.__annotations__ = func.__annotations__
        self.__doc__ = func.__doc__
        self.fn = func.__name__
        self.name = self.name or self.fn

    def set_var(self, instance: DiscordObject, value: Any):
        instance._data_saved[self.fn] = value

    def convert_result(self, result, instance) -> Any:
        if self.option == "c":
            result = self.func(instance, result)
        elif self.option == "e":
            result = getattr(enums, self.func.__annotations__["return"]).from_value(result)
        elif self.option == "f":
            result = getattr(flags, self.func.__annotations__["return"])(result or 0)
        elif self.option == "s":
            result = Snowflake(result) if result is not None else None
        return result

    def config(self, default: Optional[Any] = None, name: Optional[str] = None):
        self.default, self.name = default, name

    def __get__(self, instance: DiscordObject, owner):
        if instance is None:
            return self
        if self.fn in instance._data_saved:
            return instance._data_saved[self.fn]
        name = self.name or self.fn
        result = instance._data.get(name, self.default)
        if self.option is not None:
            result = self.convert_result(result, instance)
        self.set_var(instance, result)
        return result

class data_custom(data): option = "c"
class data_enum(data): option = "e"
class data_flag(data): option = "f"
class data_snowflake(data): option = "s"