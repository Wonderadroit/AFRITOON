from engine.cast_scene import CastScene
from engine.character_spec import character
from engine.story_director import StoryBeat, build_story_plan
from engine.story_performance import cue_at, cues_for


def test_story_beat_maps_to_character_action_and_expression():
    plan = build_story_plan("Test", 10, [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")])
    cue = cue_at(cues_for(plan, "tunde"), 3)
    assert cue is not None and cue.action == "shock" and cue.expression == "shocked"


def test_story_cue_is_valid_for_character_contract():
    plan = build_story_plan("Test", 10, [StoryBeat(2, "silent look", "seyi", "deadpan", "look")])
    cue = cues_for(plan, "seyi")[0]
    assert cue.action in character("seyi").actions
    assert cue.expression in character("seyi").expressions


def test_cast_scene_uses_story_when_no_interaction_exists():
    plan = build_story_plan("Story only", 5, [StoryBeat(2, "power goes off", "tunde", "shocked", "panic")])
    from engine.character_library import DEFAULT_LIBRARY
    scene = CastScene("story_only", 5, [DEFAULT_LIBRARY.spawn("tunde")], story_plan=plan)
    state = scene.state_at(2)
    assert state.characters["tunde"].pose == "shock"
    assert state.characters["tunde"].expression == "shocked"


def test_explicit_interaction_still_overrides_story_performance():
    plan = build_story_plan("NEPA", 24, [StoryBeat(7, "power goes off", "tunde", "shocked", "panic")])
    scene = CastScene.from_interaction("nepa_panic", 24)
    scene.story_plan = plan
    state = scene.state_at(7)
    assert state.characters["tunde"].pose == "shock"
    assert state.characters["tunde"].expression == "shocked"


def test_tunde_shock_generates_seyi_and_mama_reactions():
    plan = build_story_plan("Reaction test", 10, [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")])
    seyi = cue_at(cues_for(plan, "seyi"), 3.35)
    mama = cue_at(cues_for(plan, "mama"), 3.65)
    assert seyi is not None and seyi.action == "look" and seyi.expression == "deadpan"
    assert mama is not None and mama.action == "turn" and mama.expression == "curious"


def test_reactions_do_not_recursively_trigger_more_reactions():
    plan = build_story_plan("Reaction test", 10, [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")])
    seyi_cues = cues_for(plan, "seyi")
    assert len(seyi_cues) == 1
    assert seyi_cues[0].at == 3.35


def test_contextual_reaction_expires_after_its_acting_window():
    plan = build_story_plan("Reaction test", 10, [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")])
    reaction = cues_for(plan, "seyi")[0]
    assert reaction.duration == 1.16
    assert cue_at((reaction,), 3.35) == reaction
    assert cue_at((reaction,), 4.50) is None


def test_contextual_reaction_focuses_on_source_character():
    plan = build_story_plan("Reaction test", 10, [StoryBeat(3, "power goes off", "tunde", "shocked", "panic")])
    seyi = cue_at(cues_for(plan, "seyi"), 3.35)
    mama = cue_at(cues_for(plan, "mama"), 3.65)
    assert seyi is not None and seyi.focus == "tunde"
    assert mama is not None and mama.focus == "tunde"


def test_approach_story_creates_target_reaction_and_focus():
    plan = build_story_plan("Approach", 8, [StoryBeat(2, "Seyi approaches Tunde", "seyi", "calm", "observe Tunde")])
    seyi = cue_at(cues_for(plan, "seyi"), 2.0)
    tunde = cue_at(cues_for(plan, "tunde"), 2.25)
    assert seyi is not None and seyi.focus == "tunde"
    assert tunde is not None and tunde.action == "look" and tunde.focus == "seyi"


def test_camera_intent_becomes_camera_focus():
    plan = build_story_plan("Camera", 5, [StoryBeat(1, "Seyi looks at camera", "seyi", "deadpan", "address audience")])
    cue = cue_at(cues_for(plan, "seyi"), 1)
    assert cue is not None and cue.focus == "camera"
