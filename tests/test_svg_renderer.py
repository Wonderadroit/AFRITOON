from pathlib import Path

from engine.svg_renderer import master_path


def test_master_path_is_canonical():
    path = master_path(".", "tunde", "front")
    assert path == Path("assets/characters/tunde/art/tunde_front.svg")


def test_master_artwork_exists_for_core_cast():
    for character_id in ("tunde", "seyi", "mama"):
        assert master_path(".", character_id).exists()
