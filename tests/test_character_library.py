import pytest

from engine.character_library import DEFAULT_LIBRARY


def test_character_state_transition_is_validated():
    tunde = DEFAULT_LIBRARY.spawn("tunde")
    updated = tunde.with_state(pose="talk", expression="happy")
    assert updated.pose == "talk"
    assert updated.expression == "happy"


def test_character_state_rejects_unknown_pose():
    tunde = DEFAULT_LIBRARY.spawn("tunde")
    with pytest.raises(ValueError, match="Unsupported action"):
        tunde.with_state(pose="not_a_real_pose")


def test_character_state_rejects_unknown_expression():
    tunde = DEFAULT_LIBRARY.spawn("tunde")
    with pytest.raises(ValueError, match="Unsupported expression"):
        tunde.with_state(expression="not_a_real_expression")
