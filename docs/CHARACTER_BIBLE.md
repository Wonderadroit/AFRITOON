# ITANRA Character Bible

**Status:** Canonical production specification

## Purpose

ITANRA characters must feel like recurring people, not disposable cartoon assets. Artwork, rigging and acting can evolve, but the identity rules below are stable unless the character bible is intentionally revised.

## Visual target

- Human-looking stylized 2D characters.
- Clean bold linework with simple cel-style shading.
- Designed for phone screens and vertical 9:16 framing.
- Expressive eyes, eyebrows, mouth and hands are more important than visual detail.
- Humor comes from acting, timing, contrast and recognition, not from degrading caricature.
- The three characters must remain visually distinguishable in silhouette.

## Canonical cast

### Tunde — the confident mistake

**Role:** protagonist  
**Age band:** young adult

Personality: confident, mischievous, optimistic, often wrong.

Recognition cues:
- short low-fade hair
- slightly oversized head
- expressive eyebrows and eyes
- warm-gold graphic T-shirt
- deep-blue jeans
- off-white sneakers
- chest-out confident posture
- forced smile when caught

Acting grammar:

`confidence -> certainty -> discovery -> panic -> forced smile -> camera look`

Signature actions:
- empty-pocket check
- forced smile
- camera look
- sudden shock
- overconfident pointing

### Seyi — the deadpan human reaction button

**Role:** best friend  
**Age band:** young adult

Personality: observant, deadpan, smart, patient, quietly sarcastic.

Recognition cues:
- slightly taller and leaner than Tunde
- neat short haircut
- muted-teal casual shirt
- deep-blue jeans
- restrained facial movement
- highly readable eyes

Acting grammar:

`observe -> predict -> wait -> deadpan -> look at Tunde -> camera look`

Signature actions:
- side-eye
- slow head turn
- knowing smile
- long pause
- look at Tunde, then camera

### Mama — the final boss of information

**Role:** mother  
**Age band:** older adult

Personality: perceptive, commanding, warm, funny, unshakable.

Recognition cues:
- strong maternal silhouette
- stable headwrap
- soft-rose blouse / earth-toned wrapper
- expressive hands
- authoritative eyes and eyebrows

Acting grammar:

`enter -> notice -> silence -> stare -> one question -> everybody exposed`

Signature actions:
- hands on hips
- silent stare
- raised eyebrow
- slow turn
- instant interrogation
- knowing look

## Rig contract

Every canonical front artwork uses the existing 16-layer contract:

`back_hair, legs, shoes, torso, left_arm, right_arm, neck, head, ears, front_hair, left_eye, right_eye, left_brow, right_brow, nose, mouth`

The contract remains stable so existing pose/render code does not break when artwork is improved.

## View contract

Each character is planned for:

- `front`
- `three_quarter`
- `side`

A view is not considered production-ready merely because a file exists. It must preserve the character's canonical proportions, clothing, hair/headwrap and facial recognition cues.

## Expression contract

Expressions must remain compatible with the engine's semantic states:

`neutral, happy, curious, shocked, deadpan, angry, sad, laughing, surprised`

Face animation should be layered independently from body motion so dialogue can change the mouth without replacing the whole pose.

## Phone-size test

A character design passes the recognition test when, at small vertical-video scale:

1. the three characters can be identified without labels;
2. the emotional state is readable from eyes/brows/mouth;
3. the silhouette remains distinct;
4. the signature wardrobe/hair cue survives;
5. the design still reads when rendered in a simple scene.

## Change rule

Do not redesign a character inside an episode. Changes to proportions, wardrobe, hair/headwrap or core facial identity belong here first, then propagate through the asset pipeline.
