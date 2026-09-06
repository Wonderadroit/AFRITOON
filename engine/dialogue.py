"""Dialogue timeline primitives for AFRITOON scenes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DialogueLine:
    character: str
    text: str
    at: float
    duration: float | None = None
    voice: str | None = None

    def __post_init__(self) -> None:
        if self.at < 0:
            raise ValueError("Dialogue start time cannot be negative")
        if not self.character.strip():
            raise ValueError("Dialogue character cannot be empty")
        if not self.text.strip():
            raise ValueError("Dialogue text cannot be empty")
        if self.duration is not None and self.duration <= 0:
            raise ValueError("Dialogue duration must be positive")


def dialogue_at(lines: Iterable[DialogueLine], t: float) -> DialogueLine | None:
    """Return the dialogue line active at time t, if one exists."""
    current: DialogueLine | None = None
    for line in sorted(lines, key=lambda item: item.at):
        if line.at > float(t):
            break
        if line.duration is None:
            current = line
            continue
        if line.at <= float(t) < line.at + line.duration:
            current = line
    return current
