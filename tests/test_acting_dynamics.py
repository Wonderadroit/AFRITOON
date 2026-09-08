from engine.acting_dynamics import micro_motion


def test_micro_motion_is_deterministic():
    assert micro_motion("tunde", 1.25) == micro_motion("tunde", 1.25)


def test_characters_have_distinct_motion_rhythms():
    tunde = micro_motion("tunde", 1.25)
    seyi = micro_motion("seyi", 1.25)
    mama = micro_motion("mama", 1.25)
    assert tunde != seyi
    assert seyi != mama


def test_motion_stays_bounded():
    for character in ("tunde", "seyi", "mama"):
        for time in (0, 0.5, 1.0, 2.5, 3.8, 7.7):
            state = micro_motion(character, time)
            assert -1.0 <= state.breath <= 1.0
            assert -1.0 <= state.weight <= 1.0
            assert 0.0 <= state.blink <= 1.0
