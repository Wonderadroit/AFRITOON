from engine.view_policy import resolve_view


def test_front_view_resolves_directly():
    result = resolve_view(".", "tunde", "front")
    assert result.requested == "front"
    assert result.resolved == "front"
    assert result.fallback is False


def test_unfinished_view_falls_back_explicitly():
    result = resolve_view(".", "tunde", "three_quarter")
    assert result.requested == "three_quarter"
    assert result.resolved == "front"
    assert result.fallback is True
