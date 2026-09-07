from engine.cast_scene import CastScene
from engine.character_library import spawn
from engine.entrance_exit import EntryExitCue, resolve_entry_exit, resolve_entry_exit_states


BASE = {"seyi": (570.0, 1450.0), "mama": (810.0, 1450.0)}


def test_enter_starts_offscreen_and_reaches_authored_position():
    cues = (EntryExitCue(2.0, "seyi", "enter", (-180.0, 1450.0), 2.0),)
    before, visible_before = resolve_entry_exit("seyi", 1.0, BASE, cues)
    middle, visible_middle = resolve_entry_exit("seyi", 3.0, BASE, cues)
    after, visible_after = resolve_entry_exit("seyi", 4.0, BASE, cues)
    assert before == BASE["seyi"]
    assert visible_before is True
    assert -180.0 < middle[0] < 570.0
    assert visible_middle is True
    assert after == BASE["seyi"]
    assert visible_after is True


def test_exit_moves_then_hides():
    cues = (EntryExitCue(2.0, "mama", "exit", (1260.0, 1450.0), 2.0),)
    middle, visible_middle = resolve_entry_exit("mama", 3.0, BASE, cues)
    after, visible_after = resolve_entry_exit("mama", 4.0, BASE, cues)
    assert 810.0 < middle[0] < 1260.0
    assert visible_middle is True
    assert after == (1260.0, 1450.0)
    assert visible_after is False


def test_entry_exit_preserves_scale_and_is_deterministic():
    base = {"seyi": (570.0, 1450.0, 0.78)}
    cues = (EntryExitCue(0.0, "seyi", "enter", (-180.0, 1450.0), 1.0),)
    a = resolve_entry_exit_states(0.5, base, cues)
    b = resolve_entry_exit_states(0.5, base, cues)
    assert a == b
    assert a["seyi"][2] == 0.78


def test_scene_without_entry_exit_preserves_existing_visibility():
    scene = CastScene("plain", 5.0, [spawn("seyi", x=570, y=1450, visible=False)])
    assert scene.state_at(2.0).characters["seyi"].visible is False


def test_scene_entry_overrides_hidden_start_and_keeps_identity():
    scene = CastScene(
        "entrance",
        5.0,
        [spawn("seyi", x=570, y=1450, scale=0.78, visible=False)],
        entry_exit_cues=(EntryExitCue(1.0, "seyi", "enter", (-180.0, 1450.0), 2.0),),
    )
    before = scene.state_at(0.5).characters["seyi"]
    middle = scene.state_at(2.0).characters["seyi"]
    after = scene.state_at(3.0).characters["seyi"]
    assert before.visible is False
    assert middle.visible is True
    assert -180.0 < middle.x < 570.0
    assert after.visible is True
    assert after.x == 570.0
    assert after.scale == 0.78
    assert after.definition.id == "seyi"


def test_scene_exit_hides_only_after_exit_window():
    scene = CastScene(
        "exit",
        5.0,
        [spawn("mama", x=810, y=1450, visible=True)],
        entry_exit_cues=(EntryExitCue(1.0, "mama", "exit", (1260.0, 1450.0), 2.0),),
    )
    assert scene.state_at(2.0).characters["mama"].visible is True
    assert scene.state_at(3.0).characters["mama"].visible is False
