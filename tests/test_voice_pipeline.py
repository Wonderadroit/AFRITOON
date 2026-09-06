from pathlib import Path

from engine.cast_scene import CastScene
from engine.voice_director import voice_cues
from engine.voice_manifest import build_voice_manifest


ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenes" / "nepa_please.yaml"


def test_scene_loads_dialogue_and_resolves_character_voices():
    scene = CastScene.from_yaml(SCENE)
    assert len(scene.dialogue) == 10
    cues = voice_cues(scene.dialogue)
    assert [cue.voice.id for cue in cues] == [
        "tunde_v1", "tunde_v1", "tunde_v1", "tunde_v1", "seyi_v1",
        "tunde_v1", "mama_v1", "tunde_v1", "mama_v1", "seyi_v1",
    ]


def test_voice_manifest_contains_mouth_timing():
    scene = CastScene.from_yaml(SCENE)
    manifest = build_voice_manifest(scene.dialogue)
    assert len(manifest) == 10
    assert manifest[0]["voice"]["character"] == "tunde"
    assert manifest[0]["duration"] > 0
    assert manifest[0]["mouth"]


def test_dialogue_at_respects_explicit_duration():
    scene = CastScene.from_yaml(SCENE)
    assert scene.dialogue_at(1.0).character == "tunde"
    assert scene.dialogue_at(3.8) is None
    assert scene.dialogue_at(18.8).character == "mama"
