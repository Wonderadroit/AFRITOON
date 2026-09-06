from engine.actions import Action
from engine.mouth_timing import mouth_cues
from engine.performance import performance_at


def test_performance_combines_body_face_and_mouth():
    result = performance_at(
        1.2,
        actions=[Action(0.0, "talk"), Action(1.0, "shock")],
        face_timeline=[{"at": 0.0, "expression": "neutral"}, {"at": 1.0, "expression": "shocked"}],
        mouth_cues=mouth_cues("Ah!", 1.0, 0.8),
    )
    assert result.pose == "shock"
    assert result.action == "shock"
    assert result.expression == "shocked"
    assert result.mouth in {"talk_a", "talk_rest"}


def test_performance_defaults_are_stable():
    result = performance_at(0.0)
    assert result.pose == "idle"
    assert result.action == "idle"
    assert result.expression == "neutral"
    assert result.mouth == "closed"
