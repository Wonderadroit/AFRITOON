from pathlib import Path

from PIL import Image

from engine.camera_director import apply_camera, camera_at
from engine.cast_scene import CastScene


def test_camera_stays_inside_output_and_tracks_dialogue():
    scene = CastScene.from_yaml(Path("scenes/nepa_please.yaml"))
    opening = camera_at(scene, 1.0)
    tunde = camera_at(scene, 8.0)
    mama = camera_at(scene, 21.2)

    assert opening.shot in {"wide", "medium"}
    assert tunde.focus == "tunde"
    assert tunde.scale > 1.0
    assert mama.focus == "mama"
    assert 1.0 <= mama.scale <= 1.18
    for state in (opening, tunde, mama):
        assert 0.0 < state.scale <= 1.18
        assert 0.0 <= state.center_x <= 1080.0
        assert 0.0 <= state.center_y <= 1920.0


def test_camera_crop_preserves_vertical_output_size():
    image = Image.new("RGBA", (1080, 1920), (255, 255, 255, 255))
    camera = camera_at(CastScene.from_yaml(Path("scenes/nepa_please.yaml")), 8.0)
    rendered = apply_camera(image, camera)
    assert rendered.size == (1080, 1920)
    assert rendered.mode == "RGBA"
