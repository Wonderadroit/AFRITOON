from engine.cast_scene import CastScene


def test_trio_showcase_loads_real_cast_composition():
    scene = CastScene.from_yaml("scenes/trio_showcase.yaml")
    assert scene.duration == 6.0
    assert set(scene.characters) == {"tunde", "seyi", "mama"}
    assert scene.characters["tunde"].x == 300
    assert scene.characters["mama"].scale == 1.05


def test_trio_showcase_interaction_updates_character_state():
    scene = CastScene.from_yaml("scenes/trio_showcase.yaml")
    state = scene.state_at(3.2)
    assert state.characters["tunde"].pose == "freeze"
    assert state.characters["tunde"].expression == "shocked"
    assert state.characters["mama"].pose == "stand"
