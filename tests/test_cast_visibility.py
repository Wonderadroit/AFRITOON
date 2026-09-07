from pathlib import Path

from engine.cast_scene import CastScene


def test_nepa_characters_enter_at_story_beats():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))

    early = scene.state_at(5.0)
    seyi_entry = scene.state_at(13.0)
    mama_entry = scene.state_at(19.0)

    assert early.characters["tunde"].visible is True
    assert early.characters["seyi"].visible is False
    assert early.characters["mama"].visible is False
    assert seyi_entry.characters["seyi"].visible is True
    assert seyi_entry.characters["mama"].visible is False
    assert mama_entry.characters["mama"].visible is True


def test_nepa_story_beat_drives_contextual_reactions():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))

    seyi = scene.state_at(7.4).characters["seyi"]
    mama = scene.state_at(7.7).characters["mama"]

    assert seyi.pose == "look"
    assert seyi.expression == "deadpan"
    assert mama.pose == "turn"
    assert mama.expression == "curious"
