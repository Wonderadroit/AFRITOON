from engine.cast_scene import CastScene


def test_trio_showcase_contains_all_three_characters():
    scene = CastScene.from_interaction("trio_problem")
    assert set(scene.characters) == {"tunde", "seyi", "mama"}


def test_trio_state_updates_characters_independently():
    scene = CastScene.from_interaction("trio_problem")
    state = scene.state_at(3.2)
    assert state.characters["tunde"].pose == "freeze"
    assert state.characters["tunde"].expression == "shocked"
    assert state.characters["seyi"].pose == "look_at_camera"
    assert state.characters["seyi"].expression == "deadpan"
    assert state.characters["mama"].pose == "stand"


def test_interaction_duration_covers_last_cue():
    scene = CastScene.from_interaction("trio_problem")
    assert scene.duration >= 5.5
