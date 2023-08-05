class WPCordException(Exception):
    """
    Base class for WPCord exceptions based on :class:`Exception`
    """

class InvalidType(WPCordException):
    def __init__(self, obj: object, obj_name: str, *valid_types) -> None:
        super().__init__(f"{obj_name} must be instance of {' | '.join(t.__name__ for t in valid_types)}, not {type(obj).__name__}")

class DiscordAPIError(WPCordException):
    pass

class Unauthorized(DiscordAPIError):
    pass

class NotFound(DiscordAPIError):
    pass

class UnknownEvent(WPCordException):
    pass