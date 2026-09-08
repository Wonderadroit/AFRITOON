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


def _pulse(t: float, period: float, width: float) -> float:
    phase = (float(t) % period) / period
    if phase < width:
        x = phase / width
        return math.sin(math.pi * x) ** 2
    return 0.0


def micro_motion(character: str, time: float) -> MicroMotion:
    """Return deterministic breathing, weight-shift and blink cues."""
    cid = str(character).strip().lower()
    t = max(0.0, float(time))
    rhythm = {"tunde": 3.15, "seyi": 3.55, "mama": 4.05}.get(cid, 3.5)
    breath = math.sin((2.0 * math.pi * t / rhythm) + {"tunde": 0.0, "seyi": 0.8, "mama": 1.4}.get(cid, 0.0))
    weight = math.sin((2.0 * math.pi * t / (rhythm * 1.7)) + 0.5) * {"tunde": 1.0, "seyi": 0.55, "mama": 0.35}.get(cid, 0.5)
    # Blink every ~3.8s, with character-specific phase offsets. The engine
    # never blinks both eyes independently yet; the short symmetric blink is
    # intentional and can later be replaced by authored blink choreography.
    blink = _pulse(t + {"tunde": 0.0, "seyi": 1.15, "mama": 2.1}.get(cid, 0.0), 3.8, 0.085)
    return MicroMotion(breath=breath, weight=weight, blink=blink)
