from engine.acting_timing import ActingTiming, acting_motion, acting_phase, motion_curve, timing_for
from engine.character_pose import pose_for_motion


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


def test_motion_curves_are_bounded():
    for character in ("tunde", "seyi", "mama"):
        for phase in ("anticipation", "action", "hold", "recovery"):
            values = [motion_curve(character, phase, step / 10) for step in range(11)]
            assert all(0.0 <= value <= 1.0 for value in values)
            assert values[0] <= values[-1] or phase == "hold"


def test_tunde_shock_moves_continuously_into_action():
    early = acting_motion("tunde", "shock", 0.16)
    mid = acting_motion("tunde", "shock", 0.21)
    assert early[0] == "action"
    assert 0.15 <= early[2] < mid[2] <= 1.0


def test_recovery_returns_toward_idle():
    phase, progress, amount = acting_motion("tunde", "shock", 0.81)
    assert phase == "recovery"
    assert progress > 0.0
    assert 0.0 <= amount < 1.0


def test_motion_pose_preserves_layer_contract():
    pose = pose_for_motion("mama", "angry", 0.5)
    idle = pose_for_motion("mama", "idle", 0.0)
    assert set(pose.layers) == set(idle.layers)
    assert pose.layers["left_arm"].rotation < 0
