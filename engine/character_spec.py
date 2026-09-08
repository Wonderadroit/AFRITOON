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
        id="tunde", name="Tunde", role="big_brother_friend", age_band="24",
        personality=("confident", "funny", "mischievous", "optimistic", "often_wrong"),
        visual=CharacterVisual(
            skin="medium_dark_brown", hair="short_textured_low_fade",
            wardrobe="black_hoodie_cargo_pants_sneakers",
            silhouette="slightly_oversized_head_confident_young_adult_build",
            head_ratio=1.15,
            signature=("forced_smile", "big_gestures", "empty_pocket_check", "camera_look"),
            design_notes=(
                "human-looking stylized 2D proportions",
                "slightly broad shoulders with relaxed young-adult build",
                "clean expressive face with readable eyes and brows",
                "black hoodie is the stable core wardrobe cue; printed text is optional artwork detail",
                "comedy comes from confidence and acting, never visual foolishness",
            ),
            palette=("skin-medium-dark", "hair-black", "hoodie-charcoal", "pants-deep-olive", "shoe-off-white"),
        ),
    ),
    "seyi": CharacterDefinition(
        id="seyi", name="Seyi", role="friend_confidant", age_band="22",
        personality=("smart", "calm", "sarcastic", "observant", "quietly_loyal"),
        visual=CharacterVisual(
            skin="dark_brown", hair="long_black_braids",
            wardrobe="black_fitted_top_lilac_cargo_pants_sneakers",
            silhouette="slightly_taller_lean_feminine_observant",
            head_ratio=1.05,
            signature=("side_eye", "dry_humor", "arms_crossed", "knowing_smile", "slow_head_turn"),
            design_notes=(
                "human-looking stylized 2D young Nigerian woman",
                "long braids are a stable recognition cue",
                "small gold hoop earrings are a stable accessory cue",
                "black fitted top and lilac cargo trousers form the core wardrobe language",
                "restrained facial movement with highly readable eyes",
                "no eyewear is part of the canonical design",
            ),
            palette=("skin-dark-brown", "hair-black", "top-charcoal", "pants-lilac", "accent-gold", "shoe-off-white"),
        ),
        default_expression="deadpan",
    ),
    "mama": CharacterDefinition(
        id="mama", name="Mama", role="mother_matriarch", age_band="50_plus",
        personality=("strong", "caring", "funny", "straight_talking", "no_nonsense"),
        visual=CharacterVisual(
            skin="medium_dark_brown", hair="patterned_headwrap",
            wardrobe="green_orange_patterned_dress_house_shoes",
            silhouette="strong_maternal_fuller_grounded_shape",
            head_ratio=1.08,
            signature=("raised_eyebrow", "hands_on_hips", "knowing_look", "deep_sigh", "instant_interrogation"),
            design_notes=(
                "human-looking stylized 2D Nigerian matriarch",
                "green-and-orange patterned headwrap and dress are stable recognition cues",
                "expressive eyes and hands support silent-comedy acting",
                "warm authority; never designed as an ugly or degrading stereotype",
                "controlled movement with strong posture and deliberate turns",
            ),
            palette=("skin-medium-dark", "headwrap-deep-green", "dress-orange-green", "accent-gold", "shoe-cream"),
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
