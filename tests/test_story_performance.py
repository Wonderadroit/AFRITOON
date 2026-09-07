from engine.cast_scene import CastScene
from engine.character_spec import character
from engine.story_director import StoryBeat, build_story_plan
from engine.story_performance import cue_at, cues_for


def test_story_beat_maps_to_character_action_and_expression():
    plan = build_story_plan(
        "Test",
        10,
        [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")],
    )
    cue = cue_at(cues_for(plan, "tunde"), 3)
    assert cue is not None
    assert cue.action == "shock"
    assert cue.expression == "shocked"


def test_story_cue_is_valid_for_character_contract():
    plan = build_story_plan(
        "Test",
        10,
        [StoryBeat(2, "silent look", "seyi", "deadpan", "look")],
    )
    cue = cues_for(plan, "seyi")[0]
    assert cue.action in character("seyi").actions
    assert cue.expression in character("seyi").expressions


def test_cast_scene_uses_story_when_no_interaction_exists():
    plan = build_story_plan(
        "Story only",
        5,
        [StoryBeat(2, "power goes off", "tunde", "shocked", "panic")],
    )
    from engine.character_library import DEFAULT_LIBRARY
    scene = CastScene("story_only", 5, [DEFAULT_LIBRARY.spawn("tunde")], story_plan=plan)
    state = scene.state_at(2)
    assert state.characters["tunde"].pose == "shock"
    assert state.characters["tunde"].expression == "shocked"


def test_explicit_interaction_still_overrides_story_performance():
    plan = build_story_plan(
        "NEPA",
        24,
        [StoryBeat(7, "power goes off", "tunde", "shocked", "panic")],
    )
    scene = CastScene.from_interaction("nepa_panic", 24)
    scene.story_plan = plan
    state = scene.state_at(7)
    assert state.characters["tunde"].pose == "shock"
    assert state.characters["tunde"].expression == "shocked"
