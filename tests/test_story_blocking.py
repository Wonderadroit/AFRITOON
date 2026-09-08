from engine.story_blocking import cues_for, position_at
from engine.story_director import StoryBeat, StoryPlan


def test_story_intent_creates_approach_cue():
    plan = StoryPlan("Untitled", 5.0, (StoryBeat(1.0, "Seyi comes over to Tunde", "seyi", "calm", "approach Tunde"),))
    cues = cues_for(plan, {"seyi": (800, 1450), "tunde": (300, 1450)})
    assert len(cues) == 1
    assert cues[0].character == "seyi"
    assert cues[0].target == "tunde"
    assert cues[0].x == 580.0


def test_story_blocking_interpolates_deterministically():
    plan = StoryPlan("Untitled", 5.0, (StoryBeat(1.0, "Seyi comes over to Tunde", "seyi", "calm", "approach Tunde"),))
    cue = cues_for(plan, {"seyi": (800, 1450), "tunde": (300, 1450)})[0]
    x0, y0 = position_at((800, 1450), cue, 1.0)
    x1, y1 = position_at((800, 1450), cue, 1.5)
    x2, y2 = position_at((800, 1450), cue, 2.0)
    assert (x0, y0) == (800, 1450)
    assert 580 < x1 < 800
    assert (x2, y2) == (580.0, 1450.0)
