from pathlib import Path

from PIL import Image

from engine.scene_background import render_background

ROOT = Path(__file__).resolve().parents[1]


def test_production_masters_use_controlled_line_weight_and_semantic_layers():
    for cid in ("tunde", "seyi", "mama"):
        path = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        text = path.read_text(encoding="utf-8")
        assert 'data-layer="head"' in text
        assert 'data-layer="mouth"' in text
        assert 'stroke-width="12"' not in text
        assert "linearGradient" in text


def test_nepa_background_changes_lighting_state():
    lit = render_background("nepa_panic", 3.0)
    blackout = render_background("nepa_panic", 10.0)
    assert lit.size == (1080, 1920)
    assert blackout.size == lit.size
    assert lit.tobytes() != blackout.tobytes()


def test_non_nepa_background_is_stable():
    first = render_background("trio_showcase", 0.0)
    later = render_background("trio_showcase", 8.0)
    assert isinstance(first, Image.Image)
    assert first.tobytes() == later.tobytes()
