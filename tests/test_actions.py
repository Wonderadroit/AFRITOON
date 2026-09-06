from engine.actions import Action, action_at


def test_action_at_uses_latest_started_action():
    actions = [Action(0, "idle"), Action(2, "dance"), Action(4, "shock")]
    assert action_at(actions, 0).name == "idle"
    assert action_at(actions, 3).name == "dance"
    assert action_at(actions, 5).name == "shock"


def test_action_at_before_first_action():
    actions = [Action(2, "dance")]
    assert action_at(actions, 1) is None
