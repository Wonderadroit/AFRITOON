from engine.dialogue import DialogueLine, dialogue_at
from engine.mouth_timeline import text_mouth_timeline
from engine.voice import character_voice, voice_profile
from engine.voice_director import voice_cues


def test_character_voices_are_stable():
    assert character_voice("tunde").id == "tunde_v1"
    assert character_voice("seyi").id == "seyi_v1"
    assert character_voice("mama").id == "mama_v1"


def test_dialogue_timeline_resolves_active_line():
    lines = [
        DialogueLine("tunde", "One", 0.0, 2.0),
        DialogueLine("seyi", "Two", 2.0, 2.0),
    ]
    assert dialogue_at(lines, 1.0).text == "One"
    assert dialogue_at(lines, 2.5).text == "Two"


def test_voice_director_rejects_wrong_character_voice():
    lines = [DialogueLine("tunde", "Hello", 0.0, voice="mama_v1")]
    try:
        voice_cues(lines)
    except ValueError as exc:
        assert "belongs to mama" in str(exc)
    else:
        raise AssertionError("Expected mismatched voice to fail")


def test_voice_profile_and_mouth_planner():
    assert voice_profile("tunde_v1").language == "en-NG"
    cues = text_mouth_timeline("Mama, wait!")
    assert cues
    assert all(cue.mouth.startswith("talk_") for cue in cues)
