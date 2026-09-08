# ITANRA Character Bible

**Status:** Canonical production specification  
**Version:** 2.0  
**Scope:** Tunde, Seyi and Mama recurring universe

## Purpose

ITANRA characters must feel like recurring people, not disposable generated assets. The approved character-sheet direction is the visual reference for identity; production artwork must be clean, authored, layered artwork derived from that reference.

A character may be animated, posed, cropped, or expressed differently, but those operations must not silently redesign the character.

## Visual target

- Human-looking stylized 2D characters.
- Clean bold linework with controlled cel-style shading.
- Warm, polished illustrated finish; not photorealistic and not Pixar-like.
- Designed for phone screens and vertical 9:16 framing.
- Expressive eyes, eyebrows, mouth and hands matter more than decorative detail.
- Humor comes from acting, timing, contrast and recognition, not degrading caricature.
- Tunde, Seyi and Mama must remain distinguishable by silhouette, wardrobe, hair and facial construction.
- Generated reference sheets are design references, not runtime assets.
- Production masters must remain deterministic and reusable across episodes.

## Canonical cast

### Tunde — the dreamer / overthinker

**Role:** big brother / friend  
**Age:** 24

**Personality:** confident, funny, mischievous, optimistic, often wrong.

**Canonical visual identity**

- Medium-dark brown skin.
- Short textured black low-fade haircut.
- Slightly oversized head relative to body.
- Young-adult build with slightly broad shoulders.
- Black hoodie as the stable core wardrobe cue.
- Deep olive/green cargo trousers.
- Off-white sneakers.
- Highly expressive eyes and eyebrows.
- Confident, chest-out posture.

**Recognition hierarchy**

1. Head-to-body ratio.
2. Short textured low-fade hairstyle.
3. Black hoodie + cargo trousers.
4. Expressive eyebrows/eyes.
5. Confident posture.

**Acting grammar**

`confidence -> certainty -> discovery -> panic -> forced smile -> camera look`

**Signature actions**

- big hand gestures
- empty-pocket check
- forced smile
- sudden shock
- camera look

### Seyi — the realist / observer

**Role:** friend / confidant  
**Age:** 22

**Personality:** smart, calm, sarcastic, observant, quietly loyal.

**Canonical visual identity**

- Dark-brown skin.
- Slightly taller and leaner than Tunde.
- Long black braids.
- Small gold hoop earrings.
- Black fitted top.
- Lilac cargo trousers.
- Off-white sneakers.
- Restrained facial movement with highly readable eyes.

**Recognition hierarchy**

1. Taller/leaner silhouette than Tunde.
2. Long braids.
3. Lilac cargo trousers + black top.
4. Gold hoop earrings.
5. Restrained/deadpan expression.

**Acting grammar**

`observe -> predict -> wait -> deadpan -> look at Tunde -> camera look`

**Signature actions**

- side-eye
- dry humor
- arms crossed
- slow head turn
- knowing smile
- long pause

**Comedy rule:** Seyi's restraint is the joke. Do not animate her as constantly expressive.

### Mama — the backbone / wisdom

**Role:** mother / matriarch  
**Age:** 50+

**Personality:** strong, caring, funny, straight-talking, no-nonsense.

**Canonical visual identity**

- Medium-dark brown skin.
- Strong maternal, fuller silhouette.
- Patterned green-and-orange headwrap.
- Matching green-and-orange patterned dress.
- Cream house shoes.
- Authoritative eyes and eyebrows.
- Expressive hands.
- Grounded posture and controlled movement.

**Recognition hierarchy**

1. Fuller maternal silhouette.
2. Green-and-orange headwrap.
3. Matching patterned dress.
4. Authoritative eyes/brows.
5. Grounded posture.

**Acting grammar**

`enter -> notice -> silence -> stare -> one question -> everybody exposed`

**Signature actions**

- raised eyebrow
- hands on hips
- knowing look
- deep sigh
- slow turn
- instant interrogation

**Comedy rule:** Mama wins through anticipation, intelligence and authority. Never use uglification or stereotypes as the joke mechanism.

## Canonical proportions

Production artwork uses a shared `600 x 1100` source space. Proportions remain related but character-specific:

| Character | Head ratio | Silhouette | Primary distinction |
|---|---:|---|---|
| Tunde | 1.15 | young adult, slightly broad | oversized head + hoodie/cargo silhouette |
| Seyi | 1.05 | taller, leaner | braids + lilac cargos + restrained face |
| Mama | 1.08 | fuller, grounded | patterned headwrap + dress |

These values describe identity, not a requirement that every pose use identical pixel dimensions.

## Rig contract

Every production view uses the stable 16-layer contract:

`back_hair, legs, shoes, torso, left_arm, right_arm, neck, head, ears, front_hair, left_eye, right_eye, left_brow, right_brow, nose, mouth`

The contract is an engine interface. Artwork may internally use additional vector groups, but exported production layers must resolve to these semantic names.

## View contract

Each character is planned for:

- `front`
- `three_quarter`
- `side`

A view is production-ready only when it preserves the canonical design. A missing view must not be faked by skewing or stretching another view.

Until genuine production views are authored, runtime fallback to the canonical front master remains explicit.

## Expression contract

Runtime semantic states:

`neutral, happy, curious, shocked, deadpan, angry, sad, laughing, surprised`

Expression changes must be independent of body-pose changes whenever the renderer supports the separation.

Character-specific performance overrides generic expression intensity. Seyi's shock, for example, can be much more restrained than Tunde's.

## Mouth contract

Mouth animation is independent from the base head whenever possible. Dialogue systems may drive reusable semantic mouth/viseme states without replacing the character artwork.

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
4. their signature wardrobe/hair cues survive;
5. the artwork remains legible at small-screen viewing size;
6. the three characters still look like the same people across scenes.

## Master artwork rules

- SVG/vector masters are canonical production assets.
- The approved generated character sheets are visual references only.
- Do not silently replace production masters with generated raster images.
- Do not bake poses, expressions or dialogue into base artwork.
- Keep artwork independent from scene YAML and timing logic.
- Preserve the 16-layer production interface.
- Original artwork only; do not reproduce real people or copyrighted characters.

## Change control

A character redesign is a product-level change, not an episode-level decision.

Changes to proportions, face construction, hair, wardrobe, palette, silhouette, canonical expressions or action grammar must be made here first and then propagated through the asset pipeline.

Episode-specific scenes may change **performance**, but may not redefine **identity**.

## Production asset status

The approved reference direction is locked as follows:

- Tunde: black hoodie, cargo trousers, short textured low-fade.
- Seyi: young Nigerian woman, long braids, gold hoops, black top, lilac cargo trousers.
- Mama: Nigerian matriarch, green-and-orange patterned headwrap and dress.

The existing SVG masters and semantic layer pipeline remain engine infrastructure, but they must be re-authored/updated to match this locked visual direction before they are treated as final production artwork. No fake turnaround views should be generated from the old masters.

## Production principle

**Identity is authored once. Performance is generated repeatedly.**

The engine should make one canonical Tunde, one canonical Seyi and one canonical Mama perform hundreds of different stories without making them look like different people.
