from engine.cast_scene import CastScene


def test_yaml_entry_and_exit_are_first_class(tmp_path):
    scene_file = tmp_path / "blocking.yaml"
    scene_file.write_text(
        """
scene:
  duration: 6.0
  characters:
    - id: seyi
      position: [570, 1450]
      scale: 0.78
      visible: false
    - id: mama
      position: [810, 1450]
      visible: true
  blocking:
    - at: 1.0
      character: seyi
      action: enter
      from: [-180, 1450]
      duration: 2.0
    - at: 4.0
      character: mama
      action: exit
      to: [1260, 1450]
      duration: 1.0
""",
        encoding="utf-8",
    )
    scene = CastScene.from_yaml(scene_file)

    assert scene.state_at(0.5).characters["seyi"].visible is False
    seyi = scene.state_at(2.0).characters["seyi"]
    assert seyi.visible is True
    assert -180.0 < seyi.x < 570.0
    assert seyi.scale == 0.78
    assert scene.state_at(3.0).characters["seyi"].x == 570.0

    mama = scene.state_at(4.5).characters["mama"]
    assert mama.visible is True
    assert 810.0 < mama.x < 1260.0
    assert scene.state_at(5.0).characters["mama"].visible is False
