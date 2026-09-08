"""Small deterministic human-motion cues layered under authored performance."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class MicroMotion:
    """Subtle motion values; deliberately bounded so acting stays readable."""

    breath: float
    weight: float
    blink: float
    speech: float = 0.0


def _pulse(t: float, period: float, width: float) -> float:
    phase = (float(t) % period) / period
    if phase < width:
        x = phase / width
        return math.sin(math.pi * x) ** 2
    return 0.0


def _natural_blink(t: float, offset: float, attention: bool, speaking: bool) -> float:
    """Produce irregular-looking but reproducible blink windows."""
    base = _pulse(t + offset, 4.7, 0.075)
    secondary = _pulse(t * 1.013 + offset * 0.71 + 1.9, 7.1, 0.055)
    blink = max(base, secondary * 0.72)
    if attention:
        blink *= 0.72
    if speaking:
        blink *= 0.82
    return max(0.0, min(1.0, blink))


def micro_motion(
    character: str,
    time: float,
    *,
    attention: bool = False,
    speaking: bool = False,
    expression: str = "neutral",
) -> MicroMotion:
    """Return deterministic breathing, weight, blink and speech cues."""
    cid = str(character).strip().lower()
    t = max(0.0, float(time))
    rhythm = {"tunde": 3.15, "seyi": 3.55, "mama": 4.05}.get(cid, 3.5)
    phase_offset = {"tunde": 0.0, "seyi": 0.8, "mama": 1.4}.get(cid, 0.0)
    breath = math.sin((2.0 * math.pi * t / rhythm) + phase_offset)
    weight = math.sin((2.0 * math.pi * t / (rhythm * 1.7)) + 0.5) * {
        "tunde": 1.0,
        "seyi": 0.55,
        "mama": 0.35,
    }.get(cid, 0.5)
    blink = _natural_blink(
        t,
        {"tunde": 0.0, "seyi": 1.15, "mama": 2.1}.get(cid, 0.0),
        attention,
        speaking,
    )
    if str(expression).strip().lower() in {"shocked", "surprised"}:
        blink *= 0.18
    speech = 0.0
    if speaking:
        speech = math.sin((2.0 * math.pi * t * 2.35) + phase_offset) * 0.5
    return MicroMotion(breath=breath, weight=weight, blink=blink, speech=speech)
