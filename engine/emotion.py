"""Emotion state selection for AFRITOON storytelling beats.

Emotion is intentionally separate from body action. A character can dance while
happy, freeze while deadpan, or remain still while becoming sad.
"""

from dataclasses import dataclass

from .expressions import Expression, expression


SUPPORTED_EMOTIONS = {
    "calm",
    "happy",
    "curious",
    "nostalgic",
    "sad",
    "hopeful",
    "angry",
    "surprised",
    "shocked",
    "funny",
}


EMOTION_TO_EXPRESSION = {
    "calm": "neutral",
    "happy": "happy",
    "curious": "curious",
    "nostalgic": "sad",
    "sad": "sad",
    "hopeful": "happy",
    "angry": "angry",
    "surprised": "surprised",
    "shocked": "shocked",
    "funny": "deadpan",
}


@dataclass(frozen=True)
class EmotionBeat:
    at: float
    emotion: str
    intensity: float = 1.0

    @property
    def expression(self) -> Expression:
        return expression(EMOTION_TO_EXPRESSION[self.emotion])


def emotion_beat(item: dict) -> EmotionBeat:
    emotion_name = str(item.get("emotion", "calm")).strip().lower()
    if emotion_name not in SUPPORTED_EMOTIONS:
        raise ValueError(f"Unsupported emotion: {emotion_name}")
    intensity = max(0.0, min(1.0, float(item.get("intensity", 1.0))))
    return EmotionBeat(float(item.get("at", 0)), emotion_name, intensity)


def emotion_at(timeline, t: float) -> EmotionBeat:
    """Return the latest active emotion beat at time t."""
    current = EmotionBeat(0.0, "calm", 1.0)
    for item in sorted(timeline or [], key=lambda x: float(x.get("at", 0))):
        if "emotion" not in item:
            continue
        beat = emotion_beat(item)
        if beat.at > t:
            break
        current = beat
    return current
