from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_character_layers import CHARACTERS, LAYERS, semantic_nodes  # noqa: E402


EXPECTED_LAYERS = {
    cid: {"back_hair", "legs", "shoes", "torso", "left_arm", "right_arm", "neck", "head", "ears", "front_hair", "left_eye", "right_eye", "left_brow", "right_brow", "nose", "mouth"}
    for cid in ("tunde", "seyi", "mama")
}


def test_runtime_contract_has_16_layers():
    assert len(LAYERS) == 16
    assert len(set(LAYERS)) == 16


def test_masters_use_semantic_layer_names():
    for cid in CHARACTERS:
        master = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        root = ET.parse(master).getroot()
        outer = next(node for node in root if node.tag.rsplit("}", 1)[-1] == "g")
        semantic = semantic_nodes(list(outer), cid)
        assert set(semantic) == EXPECTED_LAYERS[cid]
        assert all(len(nodes) == 1 for nodes in semantic.values())


def test_semantic_mapping_preserves_both_arms_and_brows():
    for cid in CHARACTERS:
        master = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        root = ET.parse(master).getroot()
        outer = next(node for node in root if node.tag.rsplit("}", 1)[-1] == "g")
        semantic = semantic_nodes(list(outer), cid)
        for layer in ("left_arm", "right_arm", "left_brow", "right_brow"):
            assert semantic[layer]


def test_back_hair_is_a_canonical_layer():
    for cid in CHARACTERS:
        master = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        root = ET.parse(master).getroot()
        outer = next(node for node in root if node.tag.rsplit("}", 1)[-1] == "g")
        semantic = semantic_nodes(list(outer), cid)
        assert "back_hair" in semantic
