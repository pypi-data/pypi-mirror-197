import base64

from typing import Optional

class File:
    def __init__(self,
        path: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        mark_as_spoiler: bool = False
    ) -> None:
        self.path: str = path
        self.name: str = name
        self.description: Optional[str] = description
        self.mark_as_spoiler: bool = mark_as_spoiler
        
        if isinstance(path, bytes):
            self.bytes = path
        else:
            self.fp = open(self.path, 'rb')
            self.bytes = self.fp.read()
        if self.name is None:
            self.name = self.fp.name

        if self.mark_as_spoiler:
            self.name = "SPOILER_" + self.name

    @property
    def image_data(self) -> str:
        return f"data:image/{self.name.split('.')[-1]};base64,{base64.b64encode(self.bytes).decode('ascii')}"