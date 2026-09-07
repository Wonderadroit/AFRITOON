from engine.character_library import spawn
from engine.cast_scene import CastScene
from engine.story_director import StoryBeat, build_story_plan
from engine.story_blocking import entry_exit_cues_for


def test_story_entry_is_derived_from_explicit_language():
    plan = build_story_plan("Untitled", 4.0, [StoryBeat(1.0, "Seyi enters", "seyi", "calm")])
    cues = entry_exit_cues_for(plan, {"tunde": (330, 1450), "seyi": (570, 1450)})
    assert len(cues) == 1
    assert cues[0].action == "enter"
    assert cues[0].character == "seyi"
    assert cues[0].position[0] < 0


def test_story_exit_is_derived_from_explicit_language():
    plan = build_story_plan("Untitled", 4.0, [StoryBeat(1.0, "Mama leaves", "mama", "calm")])
    cues = entry_exit_cues_for(plan, {"tunde": (330, 1450), "mama": (810, 1450)})
    assert len(cues) == 1
    assert cues[0].action == "exit"
    assert cues[0].position[0] > 1080


def test_cast_scene_story_entry_moves_character_into_frame():
    plan = build_story_plan("Untitled", 4.0, [StoryBeat(1.0, "Seyi enters", "seyi", "calm")])
    scene = CastScene("story_entry", 4.0, [
        spawn("tunde", x=330, y=1450),
        spawn("seyi", x=570, y=1450),
    ], story_plan=plan)

    before = scene.state_at(0.9).characters["seyi"]
    during = scene.state_at(1.5).characters["seyi"]
    after = scene.state_at(2.1).characters["seyi"]

    assert before.visible is False
    assert during.visible is True
    assert before.x < during.x < after.x
    assert after.x == 570.0
    assert after.scale == 1.0


def test_cast_scene_story_exit_hides_after_walk_out():
    plan = build_story_plan("Untitled", 4.0, [StoryBeat(1.0, "Mama leaves", "mama", "calm")])
    scene = CastScene("story_exit", 4.0, [
        spawn("tunde", x=330, y=1450),
        spawn("mama", x=810, y=1450),
    ], story_plan=plan)

    during = scene.state_at(1.5).characters["mama"]
    after = scene.state_at(2.1).characters["mama"]

    assert during.visible is True
    assert during.x > 810.0
    assert after.visible is False
    assert after.x > 1080.0


def test_no_story_entry_exit_keeps_existing_visibility():
    plan = build_story_plan("Untitled", 2.0, [StoryBeat(0.0, "Seyi observes", "seyi", "deadpan")])
    scene = CastScene("plain_story", 2.0, [
        spawn("seyi", x=570, y=1450, visible=True),
    ], story_plan=plan)
    state = scene.state_at(1.0).characters["seyi"]
    assert state.visible is True
    assert state.x == 570.0
