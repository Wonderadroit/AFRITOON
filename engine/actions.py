"""Timeline actions for AFRITOON scenes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    time: float
    name: str
    duration: float = 0.0


def action_at(actions: list[Action], t: float) -> Action | None:
    """Return the latest action whose start time is <= t."""
    current = None
    for action in sorted(actions, key=lambda item: item.time):
        if action.time <= t:
            current = action
        else:
            break
    return current
