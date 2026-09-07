from pathlib import Path

import pytest

from engine.character_pose import pose_for
from engine.semantic_svg_rig import render_semantic_character


ROOT = Path(__file__).resolve().parents[1]


def test_master_artwork_contains_semantic_layers():
    for character in ("tunde", "seyi", "mama"):
        path = ROOT / "assets" / "characters" / character / "art" / f"{character}_front.svg"
        text = path.read_text(encoding="utf-8")
        assert 'data-layer="head"' in text
        assert 'data-layer="torso"' in text
        assert 'data-layer="left_arm"' in text
        assert 'data-layer="right_arm"' in text


def test_signature_pose_moves_individual_layers():
    idle = pose_for("tunde", "idle")
    dance = pose_for("tunde", "dance")
    assert idle.layers["torso"] != dance.layers["torso"]
    assert idle.layers["left_arm"] != dance.layers["left_arm"]
    assert idle.layers["right_arm"] != dance.layers["right_arm"]


def test_character_pose_profiles_remain_distinct():
    tunde = pose_for("tunde", "look_at_camera")
    seyi = pose_for("seyi", "look_at_camera")
    mama = pose_for("mama", "look_at_camera")
    assert tunde.layers != seyi.layers
    assert seyi.layers != mama.layers


def test_semantic_renderer_changes_pixels_between_poses():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    idle = render_semantic_character(path, "tunde", "idle")
    dance = render_semantic_character(path, "tunde", "dance")
    assert idle.size == (600, 1100)
    assert dance.size == idle.size
    assert idle.tobytes() != dance.tobytes()
