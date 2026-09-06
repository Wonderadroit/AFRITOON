"""Resolve expression and dialogue mouth state without touching character artwork."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .expressions import Expression, expression
from .mouths import MouthState, mouth


@dataclass(frozen=True)
class FaceState:
    expression: Expression
    mouth: MouthState


def face_state(expression_name: str = "neutral", mouth_name: str | None = None) -> FaceState:
    """Build a validated face state.

    If no explicit mouth is supplied, the mouth implied by the expression is
    used. This keeps expression direction independent from dialogue animation.
    """
    expr = expression(expression_name)
    selected_mouth = mouth(expr.mouth if mouth_name is None else mouth_name)
    return FaceState(expr, selected_mouth)


def face_state_at(
    timeline: Iterable[Mapping[str, object]],
    t: float,
    default_expression: str = "neutral",
) -> FaceState:
    """Resolve the latest expression/mouth cues at time ``t``.

    Timeline records use ``at`` and may contain ``expression`` and/or ``mouth``.
    Unknown states fail loudly instead of silently producing incorrect faces.
    """
    current_expression = expression(default_expression)
    current_mouth: str | None = None

    records = sorted(timeline, key=lambda item: float(item.get("at", 0)))
    for item in records:
        at = float(item.get("at", 0))
        if at > float(t):
            break
        if "expression" in item:
            current_expression = expression(str(item["expression"]))
            current_mouth = None
        if "mouth" in item:
            current_mouth = str(item["mouth"])

    return face_state(current_expression.name, current_mouth)
