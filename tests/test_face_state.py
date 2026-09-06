from engine.face_state import face_state, face_state_at


def test_expression_implies_mouth():
    state = face_state("shocked")
    assert state.expression.name == "shocked"
    assert state.mouth.name == "open"


def test_explicit_mouth_overrides_expression():
    state = face_state("happy", "talk_o")
    assert state.expression.name == "happy"
    assert state.mouth.name == "talk_o"


def test_face_state_timeline_changes_expression_and_mouth():
    timeline = [
        {"at": 0.0, "expression": "neutral"},
        {"at": 1.0, "expression": "shocked"},
        {"at": 1.5, "mouth": "talk_o"},
    ]
    assert face_state_at(timeline, 0.5).expression.name == "neutral"
    assert face_state_at(timeline, 1.2).mouth.name == "open"
    assert face_state_at(timeline, 1.7).mouth.name == "talk_o"
