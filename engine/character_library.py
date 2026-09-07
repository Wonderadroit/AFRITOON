"""Runtime character library shared by the AFRITOON renderer and scene director."""

from dataclasses import dataclass
from typing import Dict

from .character_spec import CharacterDefinition, character


@dataclass(frozen=True)
class CharacterInstance:
    definition: CharacterDefinition
    x: float = 540.0
    y: float = 1150.0
    scale: float = 1.0
    view: str = "front"
    pose: str = "idle"
    expression: str = "neutral"
    visible: bool = True

    @property
    def id(self) -> str:
        return self.definition.id

    def with_state(self, *, pose=None, expression=None, view=None, visible=None):
        next_view = self.view if view is None else view
        next_pose = self.pose if pose is None else pose
        next_expression = self.expression if expression is None else expression
        next_visible = self.visible if visible is None else bool(visible)

        if next_view not in self.definition.views:
            raise ValueError(f"Unsupported view for {self.id}: {next_view}")
        if next_pose not in self.definition.actions:
            raise ValueError(f"Unsupported action for {self.id}: {next_pose}")
        if next_expression not in self.definition.expressions:
            raise ValueError(f"Unsupported expression for {self.id}: {next_expression}")

        return CharacterInstance(
            definition=self.definition,
            x=self.x,
            y=self.y,
            scale=self.scale,
            view=next_view,
            pose=next_pose,
            expression=next_expression,
            visible=next_visible,
        )


class CharacterLibrary:
    """Create validated reusable instances without coupling scenes to artwork."""

    def __init__(self):
        self._definitions: Dict[str, CharacterDefinition] = {}

    def register(self, definition: CharacterDefinition) -> None:
        if definition.id in self._definitions:
            raise ValueError(f"Character already registered: {definition.id}")
        self._definitions[definition.id] = definition

    def get(self, name: str) -> CharacterDefinition:
        key = name.strip().lower()
        if key in self._definitions:
            return self._definitions[key]
        return character(key)

    def spawn(self, name: str, **kwargs) -> CharacterInstance:
        definition = self.get(name)
        view = kwargs.get("view", "front")
        pose = kwargs.get("pose", definition.default_pose)
        expression = kwargs.get("expression", definition.default_expression)
        if view not in definition.views:
            raise ValueError(f"Unsupported view for {name}: {view}")
        if pose not in definition.actions:
            raise ValueError(f"Unsupported action for {name}: {pose}")
        if expression not in definition.expressions:
            raise ValueError(f"Unsupported expression for {name}: {expression}")
        return CharacterInstance(
            definition=definition,
            x=float(kwargs.get("x", 540)),
            y=float(kwargs.get("y", 1150)),
            scale=float(kwargs.get("scale", 1.0)),
            view=view,
            pose=pose,
            expression=expression,
            visible=bool(kwargs.get("visible", True)),
        )


DEFAULT_LIBRARY = CharacterLibrary()


def spawn(name: str, **kwargs) -> CharacterInstance:
    return DEFAULT_LIBRARY.spawn(name, **kwargs)
