from engine.story_director import StoryBeat, build_story_plan, story_plan_from_yaml


def test_story_plan_orders_beats_and_resolves_state():
    plan = build_story_plan(
        "NEPA, Please!",
        24,
        [
            StoryBeat(8, "power goes off", "tunde", "shocked"),
            StoryBeat(0, "everyone leaves", "tunde", "calm"),
        ],
    )
    assert [beat.at for beat in plan.beats] == [0, 8]
    assert plan.at(7).event == "everyone leaves"
    assert plan.at(8).emotion == "shocked"


def test_story_plan_yaml_shape():
    plan = story_plan_from_yaml(
        {
            "story": {
                "title": "Test",
                "duration": 10,
                "beats": [
                    {"at": 0, "event": "start", "character": "tunde"},
                    {"at": 9, "event": "payoff", "character": "mama", "emotion": "deadpan", "payoff": True},
                ],
            }
        }
    )
    assert plan.title == "Test"
    assert plan.beats[-1].payoff is True
