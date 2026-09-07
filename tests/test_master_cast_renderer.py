from pathlib import Path

import pytest

from engine.cast_scene import CastScene
from engine.gaze import interaction_strength
from engine.master_cast_renderer import gaze_direction, render_master_cast
from engine.svg_renderer import SVGRenderUnavailable


POSITIONS = {
    "tunde": (330.0, 1450.0, 1.0),
    "seyi": (570.0, 1450.0, 1.0),
    "mama": (810.0, 1450.0, 1.0),
}


def test_gaze_direction_points_toward_target():
    assert gaze_direction("seyi", "tunde", POSITIONS) == "left"
    assert gaze_direction("mama", "tunde", POSITIONS) == "left"
    assert gaze_direction("tunde", "mama", POSITIONS) == "right"


def test_camera_focus_stays_centered():
    assert gaze_direction("seyi", "camera", POSITIONS) == "center"
    assert gaze_direction("seyi", None, POSITIONS) == "center"


def test_interaction_strength_is_bounded_and_distance_aware():
    near = {"a": (300.0, 1000.0, 1.0), "b": (360.0, 1000.0, 1.0)}
    far = {"a": (300.0, 1000.0, 1.0), "b": (600.0, 1000.0, 1.0)}
    assert interaction_strength("a", "b", near) == 0.0
    assert 0.0 < interaction_strength("a", "b", far) < 1.0
    extreme = {"a": (300.0, 1000.0, 1.0), "b": (900.0, 1000.0, 1.0)}
    assert interaction_strength("a", "b", extreme) == 1.0


def test_missing_or_self_target_has_no_interaction_strength():
    assert interaction_strength("a", None, POSITIONS) == 0.0
    assert interaction_strength("a", "a", POSITIONS) == 0.0
    assert interaction_strength("a", "missing", POSITIONS) == 0.0


def test_master_renderer_uses_scene_positions():
    pytest.importorskip("cairosvg")
    scene = CastScene.from_yaml(Path("scenes/trio_showcase.yaml"))
    frame = render_master_cast(scene, 0.0)
    assert frame.size == (1080, 1920)
    assert frame.mode == "RGBA"


def test_master_renderer_keeps_three_character_identity_paths():
    pytest.importorskip("cairosvg")
    scene = CastScene.from_interaction("trio_problem")
    frame = render_master_cast(scene, 3.2)
    assert frame.size == (1080, 1920)
    assert frame.getbbox() is not None
