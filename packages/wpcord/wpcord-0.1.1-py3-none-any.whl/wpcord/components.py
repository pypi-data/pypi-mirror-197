from typing import Optional

from .emoji import Emoji
from .enums import ButtonStyle, ComponentType
from .utils import JSONObject

class Component:
    def __init__(self, type: ComponentType, custom_id: Optional[str] = None) -> None:
        self.type: ComponentType = type
        if isinstance(self.type, int):
            self.type = ComponentType.from_value(self.type)
        self.custom_id: Optional[str] = custom_id

    def to_dict(self) -> JSONObject:
        payload = {
            "type": int(self.type)
        }
        if self.custom_id is not None:
            payload["custom_id"] = self.custom_id
        return payload

    def _type(self):
        d = {
            ComponentType.action_row: ActionRow,
            ComponentType.button: Button,
            ComponentType.select_menu: SelectMenu
        }
        return d[self.type]



class Button(Component):
    def __init__(self, 
        custom_id: Optional[str] = None,
        *,
        style: ButtonStyle = ButtonStyle.primary,
        label: Optional[str] = None,
        emoji: Optional[str | Emoji] = None,
        url: Optional[str] = None,
        disabled: bool = False,
        next_row: bool = False
    ) -> None:
        super().__init__(ComponentType.button, custom_id)
        if isinstance(style, int):
            style = ButtonStyle.from_value(style)
        self.style: ButtonStyle = style
        self.label: Optional[str] = str(label) if label is not None else None
        if isinstance(emoji, str):
            emoji = Emoji.from_str(emoji)
        self.emoji: Optional[Emoji] = emoji
        self.url: Optional[str] = url
        self.disabled: bool = disabled
        self.next_row: bool = next_row
    
    @property
    def enabled(self):
        return not self.disabled

    def disable(self):
        self.disabled = True
    
    def enable(self):
        self.disabled = False

    def to_dict(self) -> JSONObject:
        payload = super().to_dict()
        payload.update(
            style = int(self.style),
            disabled = self.disabled
        )
        if self.style is ButtonStyle.link and self.url is not None:
            payload.pop("custom_id", None)
            payload["url"] = self.url
        if self.label is not None:
            payload["label"] = self.label
        if self.emoji is not None:
            payload["emoji"] = self.emoji.partial_dict()
        return payload



class SelectMenuOption:
    def __init__(self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[str | Emoji] = None,
        default: bool = False
    ) -> None:
        self.label: str = str(label)
        self.value: str = str(value)
        self.description: Optional[str] = description
        if isinstance(emoji, str):
            emoji = Emoji.from_str(emoji)
        self.emoji: Optional[Emoji] = emoji
        self.default: bool = default
    
    def to_dict(self) -> JSONObject:
        payload = {
            "label": self.label,
            "value": self.value,
            "default": self.default
        }
        if self.description is not None:
            payload["description"] = self.description
        if self.emoji is not None:
            payload["emoji"] = self.emoji.partial_dict()
        return payload

class SelectMenu(Component):
    def __init__(self, 
        custom_id: str,
        options: list[SelectMenuOption] = [],
        *,
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False
    ) -> None:
        super().__init__(ComponentType.select_menu, custom_id)
        if not options:
            raise ValueError("A select menu must have at least one option")
        if len(options) > 25:
            raise ValueError("Options limit is 25")
        self.options: list[SelectMenuOption] = options
        self.placeholder: Optional[str] = placeholder
        self.min_values: int = min_values
        self.max_values: int = max_values
        self.disabled: bool = disabled

    def add_option(self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[str | Emoji] = None,
        default: bool = False
    ) -> None:
        if len(self.options) == 25:
            raise ValueError("Options limit is 25")
        self.options.append(SelectMenuOption(label, value, description, emoji, default))

    def to_dict(self) -> JSONObject:
        payload = super().to_dict()
        payload.update(
            options = [option.to_dict() for option in self.options],
            min_values = self.min_values,
            max_values = self.max_values,
            disabled = self.disabled
        )
        if self.placeholder is not None:
            payload["placeholder"] = self.placeholder
        return payload



class ActionRow(Component):
    def __init__(self, buttons: list[Button] = [], select_menu: Optional[SelectMenu] = None) -> None:
        super().__init__(ComponentType.action_row, None)
        self.components: list[Button] | list[SelectMenu] = []
        if select_menu is not None:
            self.components.append(select_menu)
        else:
            for button in buttons:
                if len(self.components) == 5:
                    raise ValueError("Limit of buttons is 5")
                self.components.append(button)

    def add_component(self, component: Button):
        if self.components and type(self.components[0]) == SelectMenu:
            raise ValueError("You cannot add components to the action row if it already has a select menu")
        if len(self.components) == 5:
            raise ValueError("Limit of components is 5")
        self.components.append(component)
    
    def to_dict(self):
        payload = super().to_dict()
        payload["components"] = [component.to_dict() for component in self.components]
        return payload