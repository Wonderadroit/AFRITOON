from engine.character_spec import all_characters, character


def test_core_cast_has_distinct_visual_identity():
    cast = {item.id: item for item in all_characters()}
    assert set(cast) == {"tunde", "seyi", "mama"}
    assert cast["tunde"].visual.signature != cast["seyi"].visual.signature
    assert cast["mama"].visual.hair == "headwrap"
    assert cast["tunde"].visual.head_ratio > cast["seyi"].visual.head_ratio


def test_character_visual_contract_is_phone_friendly():
    for item in all_characters():
        assert item.visual.design_notes
        assert item.visual.palette
        assert len(item.visual.signature) >= 3
        assert "front" in item.views
        assert "three_quarter" in item.views
        assert "side" in item.views


def test_character_defaults_are_valid():
    for item in all_characters():
        assert item.default_pose in item.actions
        assert item.default_expression in item.expressions
        assert character(item.id) is item
