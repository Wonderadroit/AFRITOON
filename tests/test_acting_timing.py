from engine.acting_timing import ActingTiming, acting_phase, timing_for


def test_tunde_shock_has_four_temporal_phases():
    timing = timing_for("tunde", "shock")
    assert timing.total == 0.82
    assert acting_phase("tunde", "shock", 0.05) == "anticipation"
    assert acting_phase("tunde", "shock", 0.20) == "action"
    assert acting_phase("tunde", "shock", 0.40) == "hold"
    assert acting_phase("tunde", "shock", 0.80) == "recovery"


def test_seyi_reaction_is_slower_than_tunde_shock():
    tunde = timing_for("tunde", "shock")
    seyi = timing_for("seyi", "look")
    assert seyi.action > tunde.action
    assert seyi.hold > tunde.hold


def test_unknown_action_uses_stable_default_timing():
    assert timing_for("tunde", "unknown").total == 0.75
    assert acting_phase("tunde", "unknown", 0.11) == "action"


def test_negative_durations_are_rejected():
    try:
        ActingTiming(-0.1, 0.1, 0.1, 0.1)
    except ValueError as exc:
        assert "negative" in str(exc)
    else:
        raise AssertionError("negative phase duration should fail")
