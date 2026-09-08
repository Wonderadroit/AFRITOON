from pathlib import Path

from PIL import Image

from engine.scene_background import render_background
from engine.semantic_svg_rig import render_semantic_character

ROOT = Path(__file__).resolve().parents[1]
MOUTH_VARIANTS = (
    "closed", "smile", "small_open", "open", "flat", "tight", "sad",
    "wide_smile", "talk_a", "talk_e", "talk_o", "talk_m", "talk_rest",
)


def test_production_masters_use_controlled_line_weight_and_semantic_layers():
    for cid in ("tunde", "seyi", "mama"):
        path = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        text = path.read_text(encoding="utf-8")
        assert 'data-layer="head"' in text
        assert 'data-layer="mouth"' in text
        assert 'data-mouth="closed"' in text
        assert 'data-mouth="talk_a"' in text
        assert 'data-mouth="talk_o"' in text
        assert 'data-mouth="wide_smile"' in text
        assert 'stroke-width="12"' not in text
        assert "linearGradient" in text


def test_authored_mouth_variants_produce_distinct_renders():
    master = ROOT / "assets" / "characters" / "tunde" / "art" / "tunde_front.svg"
    renders = {
        name: render_semantic_character(
            master,
            "tunde",
            "idle",
            expression_name="neutral",
            mouth_name=name,
            time=0.0,
            speaking=name.startswith("talk_") or name in {"open", "small_open"},
        )
        for name in MOUTH_VARIANTS
    }
    assert all(image.size == (600, 1100) for image in renders.values())
    baseline = renders["closed"].tobytes()
    assert sum(image.tobytes() != baseline for name, image in renders.items() if name != "closed") >= 10


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
