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
