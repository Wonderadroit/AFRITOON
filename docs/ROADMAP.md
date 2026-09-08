# ITANRA Roadmap

## Principle

Content quality and production speed come before feature count.

ITANRA is a code-first storytelling and animation engine for short-form African relatable stories. The engine itself owns the deterministic story/performance state. Optional external assistants may help a human create or interpret inputs later, but they are never the storytelling brain or runtime authority.

## Phase 1 — Foundation

- Reusable Tunde / Seyi / Mama cast
- Timeline-driven actions
- 9:16 rendering
- YAML scenes
- SVG semantic layers
- Expression and mouth states
- Multi-character composition

## Phase 2 — Character Performance

- Character-specific motion profiles
- Better gestures and reactions
- Eye direction
- Expression transitions
- Dialogue-driven mouth timing
- Camera reactions
- Story beat → performance intent → deterministic character state
- Explicit interaction choreography overrides derived performance

## Phase 2.5 — Visual production gate

The first full NEPA render exposed a critical gap: correct story behavior is not enough if the final animation still looks like a rough prototype.

- Approved human-looking stylized 2D character direction
- Production-grade canonical character artwork
- Distinct silhouettes and clothing language
- Controlled line weight and clean vector edges
- Reusable illustrated environments
- Story-driven lighting changes
- Contact shadows and depth cues
- Stronger vertical composition
- Semantic SVG rasterization cache
- Visual regression tests
- Human visual review before production approval

**Gate:** a scene does not advance to production merely because automated tests pass. The rendered video must also look intentionally designed, consistent and readable at phone size.

## Phase 3 — Story Brain

- Story beats
- Emotional timeline
- Character-state transitions
- Character intent
- Dialogue intent
- Scene/camera intent
- Reusable comedy and storytelling patterns
- Deterministic story rules and validation
- Story continuity across scenes and episodes

The story brain remains code-first and deterministic. An LLM, if used later, is an optional assistant for turning a human idea into structured input; it does not replace ITANRA's state, rules, validation or execution.

## Phase 4 — Production Loop

```text
IDEA / TREND / STORY
        ↓
STORY DIRECTOR
        ↓
EMOTIONAL + CHARACTER STATE
        ↓
PERFORMANCE DIRECTOR
        ↓
SCENE / CAMERA DIRECTOR
        ↓
VOICE / AUDIO TIMELINE
        ↓
ANIMATION ENGINE
        ↓
RENDER
        ↓
VISUAL REVIEW
        ↓
IMPROVE
        ↓
PUBLISH
```

## First production target

Produce the first complete short, **NEPA, Please!**, then use a small batch of additional episodes to measure retention, completion, rewatches, shares, comments and follows.

Do not build large features without evidence that they improve production speed or content quality.
