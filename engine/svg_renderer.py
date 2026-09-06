"""Optional bridge from AFRITOON SVG master artwork to RGBA images.

The dependency is deliberately optional. Scene direction and tests do not
require SVG rasterization, while production environments can install
CairoSVG to render the human-looking master artwork.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image


class SVGRenderUnavailable(RuntimeError):
    """Raised when SVG rasterization was requested without CairoSVG."""


def rasterize_svg(path: str | Path, width: int, height: int) -> Image.Image:
    """Rasterize an SVG file into a PIL RGBA image."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)
    try:
        import cairosvg
    except ImportError as exc:
        raise SVGRenderUnavailable(
            "CairoSVG is required for SVG master rendering. "
            "Install it with: pip install cairosvg"
        ) from exc

    png = cairosvg.svg2png(
        url=str(source), output_width=int(width), output_height=int(height)
    )
    return Image.open(BytesIO(png)).convert("RGBA")


def master_path(repo_root: str | Path, character_id: str, view: str = "front") -> Path:
    """Resolve a canonical character SVG master."""
    root = Path(repo_root)
    return root / "assets" / "characters" / character_id / "art" / f"{character_id}_{view}.svg"
