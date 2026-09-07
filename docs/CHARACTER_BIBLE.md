# ITANRA Character Bible

**Status:** Canonical production specification  
**Version:** 1.1  
**Scope:** Tunde, Seyi and Mama recurring universe

## Purpose

ITANRA characters must feel like recurring people, not disposable generated assets. The character artwork is the visual source of truth; this document defines the identity, proportions, acting grammar and production constraints that artwork and runtime must preserve.

A character may be animated, posed, cropped, mirrored where explicitly supported, or expressed differently, but those operations must not silently redesign the character.

## Visual target

- Human-looking stylized 2D characters.
- Clean bold linework with simple cel-style shading.
- Designed for phone screens and vertical 9:16 framing.
- Expressive eyes, eyebrows, mouth and hands matter more than decorative detail.
- Humor comes from acting, timing, contrast and recognition, not degrading caricature.
- Tunde, Seyi and Mama must remain distinguishable by silhouette, wardrobe and facial construction.
- Base artwork must remain pose-neutral and expression-neutral enough to support independent animation.

## Canonical cast

### Tunde — the confident mistake

**Role:** protagonist  
**Age band:** young adult

**Personality:** confident, mischievous, optimistic, often wrong.

**Canonical visual identity**

- Medium-dark brown skin.
- Short low-fade black hair.
- Slightly oversized head relative to body.
- Young-adult build with slightly broad shoulders.
- Warm-gold graphic T-shirt.
- Deep-blue denim trousers.
- Off-white sneakers.
- Bold readable eyebrows and eyes.
- Clear cheek and jaw contour.
- Default posture communicates chest-out confidence.

**Recognition hierarchy**

1. Head-to-body ratio.
2. Low-fade hairstyle.
3. Warm-gold shirt.
4. Expressive eyebrows/eyes.
5. Confident posture.

**Acting grammar**

`confidence -> certainty -> discovery -> panic -> forced smile -> camera look`

**Signature actions**

- empty-pocket check
- forced smile
- camera look
- sudden shock
- overconfident pointing

**Comedy rule:** Tunde is funny because he believes himself before reality catches him, not because he is visually foolish.

### Seyi — the deadpan human reaction button

**Role:** best friend  
**Age band:** young adult

**Personality:** observant, deadpan, smart, patient, quietly sarcastic.

**Canonical visual identity**

- Dark-brown skin.
- Slightly taller and leaner than Tunde.
- Neat short black haircut.
- Muted-teal casual shirt.
- Deep-blue jeans.
- Off-white sneakers.
- Restrained facial movement.
- Highly readable eyes.
- Cleaner, understated silhouette than Tunde.

**Recognition hierarchy**

1. Taller/leaner silhouette than Tunde.
2. Muted-teal shirt.
3. Neat short haircut.
4. Restrained expression.
5. Highly readable eyes.

**Acting grammar**

`observe -> predict -> wait -> deadpan -> look at Tunde -> camera look`

**Signature actions**

- side-eye
- slow head turn
- knowing smile
- long pause
- look at Tunde, then camera
- walk away without explaining

**Comedy rule:** Seyi's restraint is the joke. Do not animate him as constantly expressive.

### Mama — the final boss of information

**Role:** mother  
**Age band:** older adult

**Personality:** perceptive, commanding, warm, funny, unshakable.

**Canonical visual identity**

- Medium-dark brown skin.
- Strong maternal, fuller silhouette.
- Stable plum-toned headwrap/hair treatment.
- Soft-rose blouse.
- Earth-brown wrapper.
- Cream house shoes.
- Authoritative eyes and eyebrows.
- Expressive hands.
- Grounded posture and controlled movement.

**Recognition hierarchy**

1. Fuller maternal silhouette.
2. Stable headwrap.
3. Soft-rose blouse / earth-brown wrapper.
4. Authoritative eyes and brows.
5. Grounded posture.

**Acting grammar**

`enter -> notice -> silence -> stare -> one question -> everybody exposed`

**Signature actions**

- hands on hips
- silent stare
- raised eyebrow
- slow turn
- instant interrogation
- knowing look

**Comedy rule:** Mama wins through anticipation, intelligence and authority. Never use uglification or stereotypes as the joke mechanism.

## Canonical proportions

The current front masters use a shared `600 x 1100` coordinate space. Their body proportions are intentionally related but not identical:

| Character | Head ratio | Silhouette | Primary distinction |
|---|---:|---|---|
| Tunde | 1.15 | young adult, slightly broad | oversized head + gold shirt |
| Seyi | 1.05 | taller, leaner | teal shirt + restrained face |
| Mama | 1.08 | fuller, grounded | headwrap + maternal shape |

These values describe identity, not a requirement that every pose use identical pixel dimensions.

## Canonical palette

The palette is a recognition system, not merely decoration.

### Tunde

- skin: medium-dark brown
- hair: black
- shirt: warm gold
- denim: deep blue
- shoes: off-white

### Seyi

- skin: dark brown
- hair: black
- shirt: muted teal
- denim: deep blue
- shoes: off-white

### Mama

- skin: medium-dark brown
- headwrap: plum
- blouse: soft rose
- wrapper: earth brown
- shoes: cream

Do not arbitrarily swap wardrobe colors between recurring characters.

## Rig contract

Every production view uses the stable 16-layer contract:

`back_hair, legs, shoes, torso, left_arm, right_arm, neck, head, ears, front_hair, left_eye, right_eye, left_brow, right_brow, nose, mouth`

The contract is an engine interface. Artwork may internally use additional vector groups, but exported production layers must resolve to these semantic names.

## View contract

Each character is planned for:

- `front`
- `three_quarter`
- `side`

A view is production-ready only when it preserves:

- head/body proportions;
- skin tone and line language;
- canonical wardrobe;
- hair/headwrap construction;
- facial spacing;
- silhouette;
- character-specific recognition cues.

If a genuine view has not been authored, runtime fallback to the canonical front master is allowed and must remain explicit. Do not fabricate a fake side or three-quarter identity by silently stretching the front artwork.

## Expression contract

Runtime semantic states:

`neutral, happy, curious, shocked, deadpan, angry, sad, laughing, surprised`

Expression changes must be independent of body-pose changes whenever the renderer supports the separation.

### Expression priority

At phone size, expression readability should be preserved in this order:

1. eyes / gaze
2. eyebrows
3. mouth
4. head angle
5. body posture

Character-specific acting overrides generic expression intensity. For example, Seyi's `shocked` state can be substantially more restrained than Tunde's.

## Mouth contract

Mouth animation is independent from the base head whenever possible. Dialogue systems may drive semantic mouth states without replacing the character artwork.

The current engine may map dialogue into reusable mouth/viseme states. Do not bake dialogue-specific mouth shapes into master body artwork.

## Pose and action rules

Supported runtime action vocabulary currently includes:

`idle, walk, sit, stand, talk, point, look, turn, wave, laugh, cry, shock, shocked, angry, surprise, dance, vibe, freeze, check_pocket, shrug, look_at_camera`

Actions describe behavior; they do not redefine appearance.

Character-specific performance must remain recognizable:

- Tunde tends toward larger, more confident motion.
- Seyi tends toward smaller, delayed reactions and pauses.
- Mama tends toward controlled, deliberate movement with strong hand and eye emphasis.

## Interaction rules

Recurring comedy depends on relational timing, not isolated character animation.

### Tunde → Seyi

Tunde creates the situation. Seyi often understands the problem first.

### Seyi → Tunde

Seyi's reaction should often arrive slightly before or after Tunde's realization to create anticipation or payoff.

### Mama → both

Mama can collapse the situation with one look, question or movement. Her entrance should feel like a change in authority, not merely another character entering frame.

## Phone-size recognition test

A character design passes when rendered in a simple 9:16 scene if:

1. Tunde, Seyi and Mama can be identified without labels;
2. their emotional state is readable;
3. their silhouettes remain distinct;
4. their signature wardrobe/hair cue survives;
5. the artwork remains legible at small-screen viewing size;
6. the three characters still look like the same people across scenes.

## Master artwork rules

- SVG/vector masters are canonical.
- Do not use generated images as silent replacements for canonical masters.
- Do not bake poses, expressions or dialogue into base artwork.
- Keep artwork independent from scene YAML and timing logic.
- Preserve the 16-layer production interface.
- Original artwork only; do not reproduce real people or copyrighted characters.

## Change control

A character redesign is a product-level change, not an episode-level decision.

Changes to any of the following must be made here first and then propagated through the asset pipeline:

- proportions
- face construction
- hair/headwrap
- wardrobe
- palette
- silhouette
- canonical expressions
- canonical action grammar

Episode-specific scenes may change **performance**, but may not redefine **identity**.

## Current artwork sources

Canonical front masters:

- `assets/characters/tunde/art/tunde_front.svg`
- `assets/characters/seyi/art/seyi_front.svg`
- `assets/characters/mama/art/mama_front.svg`

The repository currently derives deterministic front-view layer files from these masters. Three-quarter and side views remain explicit authored-artwork states rather than being implied to exist.

## Production principle

**Identity is authored once. Performance is generated repeatedly.**

The engine should make one canonical Tunde, one canonical Seyi and one canonical Mama perform hundreds of different stories without making them look like different people.
