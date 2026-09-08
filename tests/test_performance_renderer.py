from pathlib import Path

import pytest
from PIL import Image

from engine.performance import PerformanceState
from engine.performance_renderer import apply_performance, performance_for_character
from engine.master_cast_renderer import render_master_cast
from engine.cast_scene import CastScene


def test_performance_changes_face_pixels():
    image = Image.new("RGBA", (600, 1100), (247, 243, 235, 255))
    neutral = apply_performance(
        image.copy(), PerformanceState("idle", "idle", "neutral", "closed"), "tunde"
    )
    shocked = apply_performance(
        image.copy(), PerformanceState("shock", "shock", "shocked", "open"), "tunde"
    )
    assert neutral.tobytes() != shocked.tobytes()


def test_performance_resolves_scene_pose_expression_and_dialogue_mouth():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    state = performance_for_character(scene, "tunde", 1.0)
    assert state.pose == "talk"
    assert state.expression == "happy"
    assert state.mouth != "closed"


def test_performance_keeps_mouth_closed_without_active_dialogue():
    scene = CastScene.from_yaml(Path("scenes/trio_showcase.yaml"))
    state = performance_for_character(scene, "tunde", 1.0)
    assert state.mouth == "closed"


def test_character_motion_profiles_are_not_identical():
    state = PerformanceState("shock", "shock", "shocked", "open")
    source = Image.new("RGBA", (600, 1100), (247, 243, 235, 255))
    tunde = apply_performance(source.copy(), state, "tunde")
    seyi = apply_performance(source.copy(), state, "seyi")
    mama = apply_performance(source.copy(), state, "mama")
    assert tunde.size != seyi.size or tunde.tobytes() != seyi.tobytes()
    assert mama.size != seyi.size or mama.tobytes() != seyi.tobytes()


def test_master_renderer_produces_different_performance_frames():
    pytest.importorskip("cairosvg")
    scene = CastScene.from_yaml(Path("scenes/trio_showcase.yaml"))
    first = render_master_cast(scene, 0.0)
    later = render_master_cast(scene, 3.0)
    assert first.size == (1080, 1920)
    assert later.size == first.size
    assert first.tobytes() != later.tobytes()


def test_nepa_checkpoint_frames_render_with_expected_cast_visibility():
    pytest.importorskip("cairosvg")
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    expected = {
        1.0: {"tunde": True, "seyi": False, "mama": False},
        8.0: {"tunde": True, "seyi": False, "mama": False},
        13.0: {"tunde": True, "seyi": True, "mama": False},
        19.0: {"tunde": True, "seyi": True, "mama": True},
        22.0: {"tunde": True, "seyi": True, "mama": True},
    }
    for at, visibility in expected.items():
        frame = render_master_cast(scene, at)
        assert frame.size == (1080, 1920)
        assert frame.getbbox() is not None
        state = scene.state_at(at)
        assert {cid: item.visible for cid, item in state.characters.items()} == visibility


def test_shock_has_anticipation_before_dialogue_interrupts_it():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    early = performance_for_character(scene, "tunde", 7.35)
    after = performance_for_character(scene, "tunde", 7.95)
    assert early.pose == "shock"
    assert after.pose == "talk"


def test_listener_gazes_at_current_speaker():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    state = performance_for_character(scene, "tunde", 13.5)
    assert state.focus == "seyi"


def test_speaker_focuses_on_visible_listener():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    state = performance_for_character(scene, "seyi", 13.5)
    assert state.focus == "tunde"
