from engine.character_library import spawn
from engine.spatial_blocking import SpatialCue, position_at, resolve_positions


BASE = {
    "tunde": (330.0, 1450.0, 1.0),
    "seyi": (570.0, 1450.0, 1.0),
}


def test_position_moves_smoothly_to_target():
    cues = (SpatialCue(2.0, "tunde", (500.0, 1450.0), 2.0),)
    assert position_at("tunde", 1.0, {"tunde": (330.0, 1450.0)}, cues) == (330.0, 1450.0)
    x, y = position_at("tunde", 3.0, {"tunde": (330.0, 1450.0)}, cues)
    assert 330.0 < x < 500.0
    assert y == 1450.0
    assert position_at("tunde", 4.0, {"tunde": (330.0, 1450.0)}, cues) == (500.0, 1450.0)


def test_resolve_positions_preserves_scale():
    cues = (SpatialCue(0.0, "tunde", (420.0, 1400.0), 1.0),)
    result = resolve_positions(1.0, BASE, cues)
    assert result["tunde"] == (420.0, 1400.0, 1.0)
    assert result["seyi"] == BASE["seyi"]


def test_spatial_cues_are_character_specific():
    cues = (SpatialCue(0.0, "tunde", (420.0, 1400.0), 0.0),)
    result = resolve_positions(2.0, BASE, cues)
    assert result["tunde"][:2] == (420.0, 1400.0)
    assert result["seyi"][:2] == BASE["seyi"][:2]


def test_character_instances_remain_identity_objects():
    instance = spawn("tunde", x=330, y=1450)
    assert instance.definition.id == "tunde"
    assert instance.x == 330.0
    assert instance.y == 1450.0
