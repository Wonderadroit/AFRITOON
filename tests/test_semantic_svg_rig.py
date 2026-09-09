from pathlib import Path

import pytest

from engine.character_pose import pose_for
from engine.semantic_svg_rig import _layer_svgs, render_semantic_character

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


def test_semantic_layer_wrappers_preserve_master_defs():
    for character in ("tunde", "seyi", "mama"):
        path = ROOT / "assets" / "characters" / character / "art" / f"{character}_front.svg"
        layers = _layer_svgs(path)
        assert "torso" in layers
        assert "<linearGradient" in layers["torso"]


def test_semantic_renderer_changes_pixels_between_poses():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    idle = render_semantic_character(path, "tunde", "idle", time=0.0)
    dance = render_semantic_character(path, "tunde", "dance", time=0.0)
    assert idle.size == (600, 1100)
    assert dance.size == idle.size
    assert idle.tobytes() != dance.tobytes()


def test_semantic_renderer_supports_all_canonical_characters():
    pytest.importorskip("cairosvg")
    for character in ("tunde", "seyi", "mama"):
        path = ROOT / "assets" / "characters" / character / "art" / f"{character}_front.svg"
        image = render_semantic_character(path, character, "idle", time=1.0)
        assert image.size == (600, 1100)
        assert image.getbbox() is not None


def test_expression_changes_pixels_without_replacing_master_artwork():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    master_before = path.read_text(encoding="utf-8")
    neutral = render_semantic_character(path, "tunde", "idle", expression_name="neutral", time=1.0)
    shocked = render_semantic_character(path, "tunde", "idle", expression_name="shocked", time=1.0)
    assert neutral.tobytes() != shocked.tobytes()
    assert path.read_text(encoding="utf-8") == master_before


def test_mouth_timing_can_override_expression_mouth():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    closed = render_semantic_character(path, "tunde", "idle", expression_name="neutral", mouth_name="closed", time=1.0)
    open_mouth = render_semantic_character(path, "tunde", "idle", expression_name="neutral", mouth_name="open", time=1.0)
    assert closed.tobytes() != open_mouth.tobytes()


def test_target_aware_geometry_changes_head_and_body_without_new_artwork():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    center = render_semantic_character(path, "tunde", "idle", gaze="center", time=1.0)
    right = render_semantic_character(path, "tunde", "idle", gaze="right", time=1.0)
    assert center.tobytes() != right.tobytes()
    assert center.size == right.size == (600, 1100)
    assert center.getbbox() is not None
    assert right.getbbox() is not None


def test_pupil_gaze_changes_eye_layer_without_translating_the_eye_whites():
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    center = _layer_svgs(path, gaze="center")["left_eye"]
    right = _layer_svgs(path, gaze="right", interaction_strength=1.0)["left_eye"]
    assert "translate(9.0 0)" not in right
    assert "translate(7.000 0)" in right
    assert center != right


def test_target_aware_geometry_is_temporally_gated():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    anticipation = render_semantic_character(path, "tunde", "shock", gaze="right", phase="anticipation", motion_progress=0.0, time=1.0)
    action = render_semantic_character(path, "tunde", "shock", gaze="right", phase="action", motion_progress=1.0, time=1.0)
    recovery = render_semantic_character(path, "tunde", "shock", gaze="right", phase="recovery", motion_progress=0.9, time=1.0)
    assert anticipation.tobytes() != action.tobytes()
    assert recovery.tobytes() != action.tobytes()


def test_time_drives_subtle_life_motion():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    early = render_semantic_character(path, "tunde", "idle", time=0.0)
    later = render_semantic_character(path, "tunde", "idle", time=1.0)
    assert early.tobytes() != later.tobytes()


def test_speaking_produces_a_distinct_arm_performance():
    pytest.importorskip("cairosvg")
    path = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    silent = render_semantic_character(path, "tunde", "talk", expression_name="happy", speaking=False, time=1.0)
    speaking = render_semantic_character(path, "tunde", "talk", expression_name="happy", speaking=True, time=1.0)
    assert silent.tobytes() != speaking.tobytes()
