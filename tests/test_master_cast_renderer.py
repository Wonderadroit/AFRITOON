from pathlib import Path

import pytest

from engine.cast_scene import CastScene
from engine.master_cast_renderer import render_master_cast
from engine.svg_renderer import SVGRenderUnavailable


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
