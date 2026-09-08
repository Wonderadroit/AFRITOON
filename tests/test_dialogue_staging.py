from engine.cast_scene import CastScene
from engine.character_library import DEFAULT_LIBRARY
from engine.dialogue import DialogueLine
from engine.performance_renderer import performance_for_character


def test_listener_focuses_on_visible_speaker():
    scene = CastScene(
        "dialogue_stage",
        4,
        [DEFAULT_LIBRARY.spawn("tunde", x=330, y=1450), DEFAULT_LIBRARY.spawn("seyi", x=570, y=1450)],
        dialogue=[DialogueLine("tunde", "Seyi, listen.", 1.0, 1.5)],
    )
    state = performance_for_character(scene, "seyi", 1.4)
    assert state.focus == "tunde"


def test_speaker_focuses_on_visible_listener():
    scene = CastScene(
        "dialogue_stage",
        4,
        [DEFAULT_LIBRARY.spawn("tunde", x=330, y=1450), DEFAULT_LIBRARY.spawn("seyi", x=570, y=1450)],
        dialogue=[DialogueLine("tunde", "Seyi, listen.", 1.0, 1.5)],
    )
    state = performance_for_character(scene, "tunde", 1.4)
    assert state.focus == "seyi"


def test_listener_does_not_focus_hidden_speaker():
    scene = CastScene(
        "dialogue_stage",
        4,
        [DEFAULT_LIBRARY.spawn("tunde", x=330, y=1450, visible=False), DEFAULT_LIBRARY.spawn("seyi", x=570, y=1450)],
        dialogue=[DialogueLine("tunde", "Seyi, listen.", 1.0, 1.5)],
    )
    state = performance_for_character(scene, "seyi", 1.4)
    assert state.focus is None
