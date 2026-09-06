from engine.cast_renderer import render_cast
from engine.cast_scene import CastScene


def test_cast_renderer_returns_vertical_rgba_frame():
    scene = CastScene.from_interaction("trio_problem")
    frame = render_cast(scene, 3.2)
    assert frame.size == (1080, 1920)
    assert frame.mode == "RGBA"


def test_cast_renderer_accepts_each_interaction_phase():
    scene = CastScene.from_interaction("trio_problem")
    for t in (0.0, 1.5, 2.5, 3.2, 4.0, 5.0):
        frame = render_cast(scene, t)
        assert frame.size == (1080, 1920)
