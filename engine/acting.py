"""Deterministic character-specific acting rules for ITANRA performances."""

from __future__ import annotations

from .expressions import expression


# These are defaults only. An explicitly authored expression always wins.
# The rule maps actions to the character's recognizable acting grammar.
CHARACTER_ACTING = {
    "tunde": {
        "shock": "shocked",
        "shocked": "shocked",
        "check_pocket": "curious",
        "dance": "happy",
        "laugh": "laughing",
        "look_at_camera": "curious",
    },
    "seyi": {
        "look": "deadpan",
        "turn": "deadpan",
        "look_at_camera": "deadpan",
        "laugh": "laughing",
    },
    "mama": {
        "angry": "angry",
        "turn": "curious",
        "look_at_camera": "deadpan",
        "laugh": "laughing",
    },
}


def acting_expression(character: str, pose: str, authored_expression: str) -> str:
    """Resolve the visible expression without overriding authored intent.

    ``neutral`` means no explicit reaction was authored, so the character's
    acting grammar may supply one from the current action. Any other valid
    expression is preserved exactly.
    """
    resolved = str(authored_expression).strip().lower()
    expression(resolved)  # validate before applying acting policy
    if resolved != "neutral":
        return resolved
    return CHARACTER_ACTING.get(character, {}).get(pose, resolved)
