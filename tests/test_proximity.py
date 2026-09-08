from engine.proximity import conversational_stop_x, distance_between, interaction_zone
from engine.story_blocking import cues_for
from engine.story_director import StoryBeat, build_story_plan


POSITIONS = {"tunde": (330, 1450), "seyi": (570, 1450), "mama": (810, 1450)}


def test_conversational_stop_is_stable():
    assert conversational_stop_x(570, 330) == 400.0
    assert conversational_stop_x(330, 570) == 500.0


def test_distance_and_zone_use_current_scene_geometry():
    positions = {"tunde": (330, 1450), "seyi": (400, 1450)}
    assert distance_between("seyi", "tunde", positions) == 70.0
    assert interaction_zone("seyi", "tunde", positions) == "close"


def test_story_approach_stops_at_natural_conversational_distance():
    plan = build_story_plan(
        "Conversation", 5, [StoryBeat(2, "Seyi approaches Tunde", "seyi", "calm", "talk to Tunde")]
    )
    cues = cues_for(plan, POSITIONS)
    assert len(cues) == 1
    cue = cues[0]
    assert cue.target == "tunde"
    assert cue.interaction_distance == 280.0
    assert cue.x == 610.0


def test_story_approach_can_be_classified_from_its_final_geometry():
    plan = build_story_plan(
        "Conversation", 5, [StoryBeat(2, "Seyi approaches Tunde", "seyi", "calm", "talk to Tunde")]
    )
    cue = cues_for(plan, POSITIONS)[0]
    positions = dict(POSITIONS)
    positions["seyi"] = (cue.x, cue.y)
    assert interaction_zone("seyi", "tunde", positions) == "near"
