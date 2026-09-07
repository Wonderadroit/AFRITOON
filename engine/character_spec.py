"""Canonical ITANRA character definitions and visual invariants."""

from dataclasses import dataclass, field
from typing import Dict, Tuple


DEFAULT_ACTIONS = (
    "idle", "walk", "sit", "stand", "talk", "point", "look", "turn",
    "wave", "laugh", "cry", "shock", "shocked", "angry", "surprise",
    "dance", "vibe", "freeze", "check_pocket", "shrug", "look_at_camera",
)

DEFAULT_EXPRESSIONS = (
    "neutral", "happy", "curious", "shocked", "deadpan", "angry", "sad",
    "laughing", "surprised",
)

DEFAULT_VIEWS = ("front", "three_quarter", "side")


@dataclass(frozen=True)
class CharacterVisual:
    """Stable visual identity; these values describe the design, not rendering."""

    skin: str
    hair: str
    wardrobe: str
    silhouette: str
    head_ratio: float = 1.0
    signature: Tuple[str, ...] = ()
    design_notes: Tuple[str, ...] = ()
    palette: Tuple[str, ...] = ()


@dataclass(frozen=True)
class CharacterDefinition:
    id: str
    name: str
    role: str
    age_band: str
    personality: Tuple[str, ...]
    visual: CharacterVisual
    default_pose: str = "idle"
    default_expression: str = "neutral"
    actions: Tuple[str, ...] = field(default_factory=lambda: DEFAULT_ACTIONS)
    expressions: Tuple[str, ...] = field(default_factory=lambda: DEFAULT_EXPRESSIONS)
    views: Tuple[str, ...] = field(default_factory=lambda: DEFAULT_VIEWS)


CHARACTERS: Dict[str, CharacterDefinition] = {
    "tunde": CharacterDefinition(
        id="tunde", name="Tunde", role="protagonist", age_band="young_adult",
        personality=("confident", "mischievous", "optimistic", "often_wrong"),
        visual=CharacterVisual(
            skin="medium_dark_brown", hair="short_low_fade",
            wardrobe="graphic_tshirt_jeans_sneakers",
            silhouette="slightly_oversized_head_confident_chest_out",
            head_ratio=1.15,
            signature=("expressive_eyebrows", "forced_smile", "empty_pocket_check", "camera_look"),
            design_notes=(
                "human-looking stylized 2D proportions",
                "slightly broad shoulders with relaxed young-adult build",
                "clear cheek and jaw contour",
                "eyes and brows must remain readable at phone size",
            ),
            palette=("skin-medium-dark", "hair-black", "shirt-warm-gold", "denim-deep-blue", "shoe-off-white"),
        ),
    ),
    "seyi": CharacterDefinition(
        id="seyi", name="Seyi", role="best_friend", age_band="young_adult",
        personality=("observant", "deadpan", "smart", "patient", "quietly_sarcastic"),
        visual=CharacterVisual(
            skin="dark_brown", hair="neat_short_cut",
            wardrobe="casual_shirt_jeans_sneakers",
            silhouette="slightly_taller_lean_observant",
            head_ratio=1.05,
            signature=("deadpan_stare", "side_eye", "slow_head_turn", "knowing_smile"),
            design_notes=(
                "slightly taller and leaner than Tunde",
                "restrained facial movement with highly readable eyes",
                "clean simple haircut and understated wardrobe",
            ),
            palette=("skin-dark-brown", "hair-black", "shirt-muted-teal", "denim-deep-blue", "shoe-off-white"),
        ),
        default_expression="deadpan",
    ),
    "mama": CharacterDefinition(
        id="mama", name="Mama", role="mother", age_band="older_adult",
        personality=("perceptive", "commanding", "warm", "funny", "unshakable"),
        visual=CharacterVisual(
            skin="medium_dark_brown", hair="headwrap",
            wardrobe="blouse_wrapper_house_shoes",
            silhouette="strong_maternal_fuller_shape",
            head_ratio=1.08,
            signature=("silent_stare", "hands_on_hips", "knowing_look", "instant_interrogation"),
            design_notes=(
                "strong maternal silhouette without caricature",
                "headwrap is a stable recognition cue",
                "hands and eyes must support silent-comedy acting",
                "warm authority; never designed as an ugly or degrading stereotype",
            ),
            palette=("skin-medium-dark", "headwrap-plum", "blouse-soft-rose", "wrapper-earth-brown", "shoe-cream"),
        ),
    ),
}


def character(name: str) -> CharacterDefinition:
    """Return a character definition by id or raise a clear error."""
    key = name.strip().lower()
    try:
        return CHARACTERS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown ITANRA character: {name}") from exc


def all_characters() -> Tuple[CharacterDefinition, ...]:
    return tuple(CHARACTERS.values())
