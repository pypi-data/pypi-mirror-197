class WPException(Exception):
    pass

class InvalidType(WPException):
    def __init__(self, obj: object, obj_name: str, *valid_types) -> None:
        super().__init__(f"{obj_name} must be instance of {' | '.join(t.__name__ for t in valid_types)}, not {type(obj).__name__}")