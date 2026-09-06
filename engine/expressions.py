"""Reusable facial-expression definitions for AFRITOON characters."""

from dataclasses import dataclass


SUPPORTED_EXPRESSIONS = {
    "neutral",
    "happy",
    "curious",
    "shocked",
    "deadpan",
    "angry",
    "sad",
    "laughing",
    "surprised",
}


@dataclass(frozen=True)
class Expression:
    name: str
    eyes: str
    brows: str
    mouth: str


EXPRESSIONS = {
    "neutral": Expression("neutral", "normal", "normal", "closed"),
    "happy": Expression("happy", "happy", "raised", "smile"),
    "curious": Expression("curious", "normal", "raised", "small_open"),
    "shocked": Expression("shocked", "wide", "raised", "open"),
    "deadpan": Expression("deadpan", "normal", "flat", "flat"),
    "angry": Expression("angry", "narrow", "furrowed", "tight"),
    "sad": Expression("sad", "sad", "raised_inner", "sad"),
    "laughing": Expression("laughing", "closed", "happy", "wide_smile"),
    "surprised": Expression("surprised", "wide", "raised", "small_open"),
}


def expression(name: str) -> Expression:
    key = str(name).strip().lower()
    if key not in SUPPORTED_EXPRESSIONS:
        raise ValueError(f"Unsupported expression: {name}")
    return EXPRESSIONS[key]


def expression_at(timeline, t: float) -> Expression:
    """Return the active expression at time t from a scene timeline."""
    current = expression("neutral")
    for item in sorted(timeline, key=lambda x: float(x.get("at", 0))):
        at = float(item.get("at", 0))
        if at > t:
            break
        if "expression" in item:
            current = expression(item["expression"])
    return current
