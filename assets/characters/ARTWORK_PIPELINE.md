# AFRITOON Character Artwork Pipeline

The character artwork is the source of truth for appearance. Movement logic must never redraw or redefine the character identity.

## Master → Rig

1. Master artwork is authored as original SVG/vector artwork.
2. Each character keeps front, three-quarter and side masters.
3. Masters are separated into the 16 rig layers defined by `engine/assets.py`.
4. Layers are rasterized as transparent PNGs when the production asset pack is prepared.
5. `LayeredRig` applies transforms from `pose_mapper.py` and interpolation.
6. Expressions and mouth states are applied independently from body poses.
7. Scene/interaction data controls timing; artwork remains reusable.

## Current master artwork

- `tunde/art/tunde_front.svg`
- `seyi/art/seyi_front.svg`
- `mama/art/mama_front.svg`

These SVGs are original human-looking vector masters and are intentionally simple enough to slice into reusable rig layers.

## Required layer contract

`back_hair`, `legs`, `shoes`, `torso`, `left_arm`, `right_arm`, `neck`, `head`, `ears`, `front_hair`, `left_eye`, `right_eye`, `left_brow`, `right_brow`, `nose`, `mouth`.

## Design rule

Funny comes from silhouette, timing, posture, facial reactions and character behavior — not from making the characters ugly or stereotypical.
