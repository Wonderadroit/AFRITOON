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
            assert -1.0 <= state.speech <= 1.0
            assert -1.0 <= state.body_sway <= 1.0


def test_attention_and_shock_reduce_blink_hold():
    normal = micro_motion("tunde", 0.0)
    attentive = micro_motion("tunde", 0.0, attention=True)
    shocked = micro_motion("tunde", 0.0, attention=True, expression="shocked")
    assert attentive.blink <= normal.blink
    assert shocked.blink <= attentive.blink


def test_speaking_adds_bounded_micro_motion():
    silent = micro_motion("seyi", 1.0)
    speaking = micro_motion("seyi", 1.0, speaking=True)
    assert speaking.speech != silent.speech
    assert abs(speaking.speech) <= 0.5


def test_strong_reactions_dampen_body_sway():
    calm = micro_motion("tunde", 1.25)
    shocked = micro_motion("tunde", 1.25, expression="shocked")
    assert abs(shocked.body_sway) < abs(calm.body_sway)
