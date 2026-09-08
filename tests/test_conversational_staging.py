from pathlib import Path

from engine.cast_scene import CastScene
from engine.performance_renderer import performance_for_character


def test_nepa_approach_completes_after_entry():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))

    entering = scene.state_at(12.5).characters["seyi"]
    arrived = scene.state_at(13.1).characters["seyi"]

    assert entering.visible is True
    assert entering.x < 570.0
    assert arrived.visible is True
    assert arrived.x == 610.0
    assert arrived.y == 1650.0


def test_nepa_dialogue_uses_conversational_focus_after_approach():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))

    tunde_listens = performance_for_character(scene, "tunde", 13.5)
    seyi_listens = performance_for_character(scene, "seyi", 15.0)

    assert tunde_listens.focus == "seyi"
    assert seyi_listens.focus == "tunde"


def test_nepa_approach_preserves_conversational_distance():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    state = scene.state_at(13.5)

    assert abs(state.characters["seyi"].x - state.characters["tunde"].x) == 280.0
