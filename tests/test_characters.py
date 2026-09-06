from engine.character_spec import all_characters, character
from engine.character_library import spawn
from engine.interactions import INTERACTIONS, interaction


def test_core_cast_exists():
    assert {c.id for c in all_characters()} == {"tunde", "seyi", "mama"}


def test_character_identity_is_distinct():
    assert character("tunde").visual.silhouette != character("seyi").visual.silhouette
    assert character("seyi").visual.silhouette != character("mama").visual.silhouette


def test_instances_validate_shared_contract():
    for name in ("tunde", "seyi", "mama"):
        instance = spawn(name)
        assert instance.view == "front"
        assert instance.pose in character(name).actions
        assert instance.expression in character(name).expressions


def test_signature_comedy_features_exist():
    assert "camera_look" in character("tunde").visual.signature
    assert "deadpan_stare" in character("seyi").visual.signature
    assert "silent_stare" in character("mama").visual.signature


def test_interactions_cover_all_cast_members():
    for item in INTERACTIONS.values():
        assert item.cues
        assert {cue.character for cue in item.cues}.issubset({"tunde", "seyi", "mama"})


def test_named_interaction_lookup():
    assert interaction("trio_problem").name == "trio_problem"
