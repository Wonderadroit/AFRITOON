from engine.actions import Action, action_at


def test_action_at():
    actions = [Action(0, "idle"), Action(2, "dance"), Action(4, "shock")]
    assert action_at(actions, 0).name == "idle"
    assert action_at(actions, 3).name == "dance"
    assert action_at(actions, 5).name == "shock"
