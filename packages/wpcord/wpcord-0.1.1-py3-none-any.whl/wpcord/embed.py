from datetime import datetime, timezone
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union
)

from . import unions
from .enums import *
from .file import File

__all__ = (
    "EmbedAuthor",
    "EmbedField",
    "EmbedFooter",
    "EmbedImage",
    "EmbedThumbnail",
    "Embed"
)

class EmbedAuthor(NamedTuple):
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    icon_file: Optional[Union[str, File]] = None

class EmbedField(NamedTuple):
    name: str
    value: str
    inline: bool = False

class EmbedFooter(NamedTuple):
    text: str
    icon_url: Optional[str] = None
    icon_file: Optional[Union[str, File]] = None

class EmbedImage(NamedTuple):
    url: str = None
    file: Optional[Union[str, File]] = None

class EmbedThumbnail(NamedTuple):
    url: str = None
    file: Optional[Union[str, File]] = None



class Embed:
    def __init__(self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: unions.ColorUnion = 0x000000,
        url: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        author: Optional[EmbedAuthor] = None,
        fields: list[EmbedField] = [],
        footer: Optional[EmbedFooter] = None,
        image: Optional[EmbedImage] = None,
        thumbnail: Optional[EmbedThumbnail] = None,
        **kwargs
    ) -> None:
        """
        Unions
        ------
        ColorUnion: :class:`int` | :class:`wpcord.ColorEnum` | :class:`tuple[int, int, int]` | :class:`dict[str, int]`
        """
        self.title: Optional[str] = str(title) if title is not None else None
        self.description: Optional[str] = str(description) if description is not None else None
        self.url: Optional[str] = str(url) if url is not None else None
        self.timestamp: Optional[datetime] = timestamp if timestamp is not None else None

        self.color: int = int()
        if kwargs.get("colour") is not None:
            color = kwargs["colour"]
        if color is not None:
            self.set_color(color)
        self.set_colour = self.set_color

        self._files: list[File] = []
        self.author: Optional[EmbedAuthor] = None
        if author is not None:
            self.set_author(author.name, author.url, author.icon_url, author.icon_file)
        self.footer: Optional[EmbedFooter] = None
        if footer is not None:
            self.set_footer(footer.text, footer.icon_url, footer.icon_file)
        self.image: Optional[EmbedImage] = None
        if image is not None:
            self.set_image(image.url, image.file)
        self.thumbnail: Optional[EmbedThumbnail] = None
        if thumbnail is not None:
            self.set_thumbnail(thumbnail.url, thumbnail.file)

        self.fields: List[EmbedField] = []
        for field in fields:
            self.fields.append(field)

    def add_field(self, name: str, value: str, inline: bool = False):
        self.fields.append(EmbedField(name, value, inline))

    def set_author(self, name: str, url: Optional[str] = None, icon_url: Optional[str] = None, icon_file: Optional[str | File] = None):
        if icon_url is None and icon_file is not None:
            if isinstance(icon_file, str):
                icon_file = File(icon_file)
            self._files.append(icon_file)
            icon_url = f"attachment://{icon_file.name}"
        author = EmbedAuthor(str(name), url, icon_url, icon_file)
        self.author = author

    def set_footer(self, text: str, icon_url: Optional[str] = None, icon_file: Optional[str | File] = None):
        if icon_url is None and icon_file is not None:
            if isinstance(icon_file, str):
                icon_file = File(icon_file)
            self._files.append(icon_file)
            icon_url = f"attachment://{icon_file.name}"
        footer = EmbedFooter(str(text), icon_url, icon_file)
        self.footer = footer
    
    def set_image(self, url: str = None, file: Optional[str | File] = None):
        if url is None and file is not None:
            if isinstance(file, str):
                file = File(file)
            self._files.append(file)
            url = f"attachment://{file.name}"
        image = EmbedImage(url, file)
        self.image = image

    def set_thumbnail(self, url: str = None, file: Optional[str | File] = None):
        if url is None and file is not None:
            if isinstance(file, str):
                file = File(file)
            self._files.append(file)
            url = f"attachment://{file.name}"
        thumbnail = EmbedThumbnail(url, file)
        self.thumbnail = thumbnail

    def set_color(self, color: int | ColorEnum | tuple[int, int, int] | dict[str, int]) -> None:
        result: int = int()
        if isinstance(color, ColorEnum):
            result += color.value
        elif isinstance(color, int):
            if not 0 <= color <= 16777215:
                raise ValueError("Color integer must be >= 0 and <= 16777215")
            result += color
        elif isinstance(color, (tuple, list, dict)):
            t = color
            if isinstance(color, dict):
                try:
                    t = (color["r"], color["g"], color["b"])
                except KeyError as e:
                    raise ValueError("Invalid RGB dictionary") from e

            if len(color) != 3:
                raise ValueError("Invalid RGB tuple")
            h = 16
            for v in t:
                if not 0 <= v <= 255:
                    raise ValueError(f"Invalid RGB value: {v}")
                result += v << h
                h -= 8
        else:
            raise TypeError(f"color must be instance of int | ColorEnum | tuple | dict, not {type(color).__name__}")
        self.color = result
    
    def set_description(self, description: str) -> None:
        self.description = str(description)

    def set_timestamp(self, timestamp: datetime):
        self.timestamp = timestamp

    def set_title(self, title: str) -> None:
        self.title = str(title)

    def set_url(self, url: str) -> None:
        self.url = str(url)

    def to_dict(self) -> dict:
        payload = {
            "color": self.color
        }

        if self.title is not None:
            payload["title"] = self.title
            if self.url is not None:
                payload["url"] = self.url
        if self.description is not None:
            payload["description"] = self.description
        if self.timestamp is not None:
            payload["timestamp"] = self.timestamp.astimezone(timezone.utc).isoformat()

        if self.author is not None:
            author = {
                "name": self.author.name
            }
            if self.author.url is not None:
                author["url"] = self.author.url
            if self.author.icon_url is not None:
                author["icon_url"] = self.author.icon_url
            payload["author"] = author

        if self.footer is not None:
            footer = {
                "text": self.footer.text
            }
            if self.footer.icon_url is not None:
                footer["icon_url"] = self.footer.icon_url
            payload["footer"] = footer
        
        if self.image is not None:
            payload["image"] = {"url": self.image.url}

        if self.thumbnail is not None:
            payload["thumbnail"] = {"url": self.thumbnail.url}

        for field in self.fields:
            if "fields" not in payload:
                payload["fields"] = []
            payload["fields"].append(
                {
                    "name": field.name,
                    "value": field.value,
                    "inline": field.inline
                }
            )

        return payload