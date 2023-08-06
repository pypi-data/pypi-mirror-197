from typing import (
    Callable,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Type,
    Union,
    overload
)

from .exceptions import InvalidType

class value:
    def __init__(self, func: Callable) -> None:
        self.__doc__ = func.__doc__
        self.value = func(None)
        if self.value is None:
            self.value = func.__name__
    
    def __get__(self, instance: Optional["Flag"], owner: Optional[Type["Flag"]]) -> bool:
        if instance is None:
            return self
        return instance._check(self.value, instance._default_check)

    def __set__(self, instance: "Flag", toggle) -> None:
        if instance is None:
            return self
        instance._set(self.value, toggle)

class Flag:
    """

    """
    _values: Dict[str, int]
    _default_check: bool = True
    def __init__(self, total: int = 0, **values: bool) -> None:
        self.total: int = total
        for name, value in values.items():
            if name not in self._values:
                raise ValueError(f"Invalid flag value: {name}")
            if not isinstance(value, bool):
                raise InvalidType(value, "value", bool)
            self._set(name, value)
        
    
    @classmethod
    def all(cls):
        instance = cls()
        for name in cls._values:
            instance._set(name, True)
        return instance

    @overload
    def _check(self, name: str, true_or_false: bool = True) -> bool: ...
    @overload
    def _check(self, value: int, true_or_false: bool = True) -> bool: ...
    def _check(self, nv: str | int, true_or_false: bool = True) -> bool:
        if not self._default_check and true_or_false:
            true_or_false = False
        value = self.__to_value(nv)
        return ((self.total & value) == value) is true_or_false

    @overload
    def _set(self, name: str, toggle: bool) -> None: ...
    @overload
    def _set(self, value: int, toggle: bool) -> None: ...
    def _set(self, nv: Union[str, int], toggle: bool) -> None:
        if not isinstance(toggle, bool):
            raise InvalidType(toggle, "toggle", bool)
        value = self.__to_value(nv)
        if toggle:
            self.total |= value
        else:
            self.total &= ~value

    def __to_value(self, nv: Union[str, int]) -> int:
        if isinstance(nv, int):
            value = nv
        else:
            value = self._values.get(str(nv))
        if value is None:
            raise ValueError(f"Invalid flag value: {nv}")
        return int(value)

    def __getitem__(self, name: str) -> bool:
        return self._check(str(name), self._default_check)

    def __contains__(self, name: str) -> bool:
        return self._check(str(name), self._default_check)

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        for name in self._values:
            yield (name, self._check(name), self._default_check)

    def __int__(self) -> int:
        return self.total