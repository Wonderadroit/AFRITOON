from engine.acting import acting_expression


def test_character_acting_defaults_follow_personality():
    assert acting_expression("tunde", "shock", "neutral") == "shocked"
    assert acting_expression("seyi", "look", "neutral") == "deadpan"
    assert acting_expression("mama", "angry", "neutral") == "angry"


def test_authored_expression_overrides_acting_default():
    assert acting_expression("seyi", "look", "happy") == "happy"
    assert acting_expression("tunde", "shock", "sad") == "sad"


def test_unmapped_action_keeps_neutral():
    assert acting_expression("mama", "talk", "neutral") == "neutral"
