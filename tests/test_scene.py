from engine.scene import Scene


def test_scene_load(tmp_path):
    p = tmp_path / "scene.yaml"
    p.write_text('title: Test\nscene:\n  duration: 3\n  timeline:\n    - time: 0\n      action: idle\n', encoding='utf-8')
    scene = Scene.load(str(p))
    assert scene.title == "Test"
    assert scene.duration == 3
    assert scene.timeline[0].name == "idle"
