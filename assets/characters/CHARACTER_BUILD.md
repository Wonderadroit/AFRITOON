# AFRITOON Character Build Contract

The recurring cast is **Tunde, Seyi and Mama**. Their identity lives in the character artwork and character bible; scene timing does not redefine their appearance.

## Production layers

Every production view uses the same 16-layer contract:

`back_hair`, `legs`, `shoes`, `torso`, `left_arm`, `right_arm`, `neck`, `head`, `ears`, `front_hair`, `left_eye`, `right_eye`, `left_brow`, `right_brow`, `nose`, `mouth`.

The front SVG masters are the canonical artwork currently checked into the repository. `tools/build_character_layers.py` deterministically derives front-view SVG layers from those masters. Optional PNG rasterization can be enabled with CairoSVG.

## Character state

The runtime contract already supports:

- front / three-quarter / side view identifiers
- reusable poses/actions
- reusable expressions
- independent mouth states
- emotion beats
- interaction cues
- cast composition
- 9:16 rendering

The renderer must not pretend a missing artwork view or expression asset exists. Missing art is an explicit build state.

## Current canonical masters

- Tunde: `assets/characters/tunde/art/tunde_front.svg`
- Seyi: `assets/characters/seyi/art/seyi_front.svg`
- Mama: `assets/characters/mama/art/mama_front.svg`

## Build

From the repository root:

```bash
python tools/validate_characters.py
python tools/build_character_layers.py --character all
```

For PNG layers when CairoSVG is available:

```bash
python tools/build_character_layers.py --character all --png
```

## Character rules

- Human-looking first.
- Funny through silhouette, timing, posture, facial reaction and behavior.
- No uglification or ethnic stereotypes as the comedy mechanism.
- Original artwork only.
- Do not bake poses or expressions into the base body artwork.
- Keep Tunde, Seyi and Mama visually distinct at phone-sized 9:16 resolution.
