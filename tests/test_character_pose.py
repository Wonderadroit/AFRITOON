from engine.character_pose import pose_for
from engine.interactions import INTERACTIONS


def test_core_cast_supports_all_interaction_poses():
    for interaction in INTERACTIONS.values():
        for cue in interaction.cues:
            pose = pose_for(cue.character, cue.pose)
            assert pose.character_id == cue.character
            assert "head" in pose.layers
            assert "torso" in pose.layers


def test_signature_cast_poses_are_distinct():
    assert pose_for("tunde", "look_at_camera").layers != pose_for("mama", "look_at_camera").layers


def test_cast_has_character_specific_conversational_gestures():
    tunde = pose_for("tunde", "talk")
    seyi = pose_for("seyi", "talk")
    mama = pose_for("mama", "talk")
    assert tunde.layers["left_arm"] != seyi.layers["left_arm"]
    assert seyi.layers["right_arm"] != mama.layers["right_arm"]


def test_mama_angry_pose_is_not_a_symmetric_generic_shock():
    angry = pose_for("mama", "angry")
    shock = pose_for("mama", "shock")
    assert angry.layers["left_arm"] != shock.layers["left_arm"]
    assert angry.layers["right_arm"] != shock.layers["right_arm"]
