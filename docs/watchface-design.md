# Watch Face Design Direction

Status: pre-implementation design contract. No public name has been selected.

## Product thesis

Design the impossible schoolyard watch: the digital watch that felt imaginable
before smartphones and broad Internet access, but was beyond what an ordinary
consumer watch could actually do.

This is not a modern smartwatch wearing a retro skin. It is an optimistic
retro-futuristic device whose apparent hardware is sincerely attempting
graphics, color, animation, and useful information beyond its capabilities.
Its limitations are visible, but the result remains dependable and glanceable.

## Emotional qualities

- Curious, optimistic, and technically ambitious.
- Sparse and functional rather than decorative.
- Nostalgic through constraints, not through brand imitation or fake casing.
- Locally surprising: the tiny weather sprite should produce an "I did not know
  it had colors" moment without turning the whole face into a color display.
- Earnest rather than glitchy. The display struggles with fidelity, not with
  correctness.

## Non-goals

- No seven-segment imitation.
- No cyberpunk neon, rainbow digits, gradients, glow, or smooth modern motion.
- No fake terminal commands, diagnostic noise, or hacker-themed decoration.
- No drawn plastic bezel, fake buttons, or skeuomorphic watch body.
- No compromised time legibility for an animation or visual joke.
- No dependence on a phone application.

## Target geometry

The primary hardware target is the 466×466 OnePlus Watch 3. The proposed WFF
canvas is also 466×466 so the primary target can be evaluated at 1:1 geometry.
This must be proven with a renderer calibration before it becomes an
implementation invariant.

Place a centered 450×450 fictional framebuffer at `(8, 8)`. Use one 5-unit
master lattice with two provisional visible pixel tiers:

```text
physical / WFF canvas: 466×466
active framebuffer:   450×450 at x=8, y=8
fine raster:             90×90 source pixels
fine pixel pitch:          5×5 units (4×4 lit + 1-unit gutter)
coarse raster:           45×45 source pixels
coarse pixel pitch:       10×10 units (8×8 lit + 2-unit gutter)
scale relationship:        exact 2×
```

The fine tier carries weather, date, steps, battery, and compact labels. The
coarse tier carries the primary time and its colon. A coarse pixel is one
contiguous 8×8 illuminated block rather than four fine pixels with internal
gutters. Both tiers align to the active framebuffer origin: fine anchors are
multiples of five and coarse anchors are multiples of ten. Do not introduce a
third scale or an independently aligned grid.

The outer eight-unit margin is overscan, not an information-bearing region. A
provisional circular safe radius of 210 units, centered at `(225, 225)` in
active-framebuffer coordinates, supplies a further 15-unit inset from the
active circle. This is a conservative design margin, not a platform guarantee;
the bezel and physical watch remain authoritative.

### Calibration gate

Before building the real composition, render a calibration face containing:

- alternating 4-unit light / 1-unit dark fine runs;
- alternating 8-unit light / 2-unit dark coarse runs;
- adjacent fine and coarse pixels proving their shared origin and exact 2×
  relationship;
- isolated lit cells and horizontal/vertical gutters at both tiers;
- checkerboards and adjacent cell clusters;
- representative bitmap glyphs; and
- marks at the active-framebuffer and circular-safe-area boundaries.

Inspect original-resolution 466×466 screenshots from `wear5-opw3` and the
physical watch. Confirm whether the WFF renderer preserves crisp cell edges or
introduces filtering. The physical watch remains authoritative. The official
454×454 `wear5` AVD is the secondary scaling/portability check.

## Fictional hardware contract

Treat the face as though it runs on the following imaginary display controller:

- One 90×90 monochrome master raster with an aligned 45×45 coarse addressing
  mode for the primary time.
- Black is unlit; white is the normal illuminated state.
- Compact information uses the fine tier; time uses the coarse tier; no third
  visible pixel pitch exists.
- One small indexed-color sprite plane, no larger than a 12×12-fine-pixel
  region.
- At most four flat visible palette entries can be active in that region in one
  frame, including white.
- No alpha blending, antialiasing, gradients, or partial cell brightness as a
  design technique.
- A preferred animation rate of 2 fps and a hard creative ceiling of 4 fps.
- No more than four frames or two seconds for an ordinary animation.
- One animated region at a time.
- No continuous animation in the resting state.
- The indexed-color plane and all animation are disabled in ambient mode.

These are creative constraints, not claims about the real AMOLED hardware.
They should remain stable even if the implementation platform can do more.

## Base plane and color plane

### Interactive resting state

The normal base plane is strictly white on black. Information hierarchy is
created with position, glyph scale, spacing, and density rather than color. The
weather icon is the one exception: it owns the tiny indexed-color plane while
fresh weather is available. Temperature, date, time, steps, and battery remain
white.

### Indexed-color plane

"8-bit color" describes the sprite's visual language, not a requirement to
display 256 colors or to use eight bits per RGB channel. The production face
will use a small fixed palette, with at most four flat visible entries in one
weather sprite. The initial partly-cloudy study uses yellow, pale cyan, medium
blue, and white; exact display-tested values remain undecided.

Outside the weather icon, color remains an event rather than a theme. It may
appear briefly and locally, then return to the normal monochrome base plus the
truthful weather sprite. Candidate transient colors include cyan, magenta,
amber, and red.

Suitable events include:

- a short color cursor during the on-visible reveal;
- a one- or two-frame write marker at a minute boundary;
- a rare top-of-hour sprite;
- a small red low-battery state; and
- a future complication update that can be represented honestly by WFF data.

Do not assign permanent colors to the date, temperature, labels, or individual
digits. Do not let multiple independent color regions compete for attention.
Red is reserved for a real exceptional state, not routine weather decoration.

## Motion language

Animation represents a low-powered controller replacing discrete frames. Use
hard frame changes and visible redraw steps; do not simulate dropped frames or
corrupt information.

Preferred characteristics:

- 2 fps by default, up to 4 fps only when necessary.
- Two to four authored sprite frames.
- Hard cuts with no easing, fading, smooth rotation, or sub-cell motion.
- `ON_VISIBLE`, minute, or hour boundaries as plausible triggers.
- A stable resting frame before and after playback: monochrome base plus the
  localized indexed-color weather sprite when weather is available.
- Time remains readable throughout, or the animation stays outside the primary
  time region.

WFF v2 supports event-controlled animated image sequences and explicit frame
rates, so this constraint can be implemented directly rather than by asking a
smooth renderer to imitate low frame rate.

## Typography and iconography

### Starting family: Pixel Operator

Pixel Operator is the approved starting type family as of 2026-08-17. This is
a starting point, not approval of one untouched font file as the final face.
The family is small, includes proportional, monospaced, half-bold, bold, and
8-series variants, and is released under CC0 1.0, which permits the project to
adapt its shapes to the fictional display grid.

Begin the calibration specimen with:

- `PixelOperatorMonoHB` for the primary time because its fixed advances prevent
  the clock from shifting as digits change and its intermediate weight remains
  open at small sizes;
- `PixelOperatorMono` for compact values and labels; and
- `PixelOperatorMono8` and `PixelOperatorMonoHB8` as coarse-display alternatives
  for the oversized time.

First test the original TTF files through WFF's custom-font renderer at sizes
where every apparent source pixel maps to exactly one fine or coarse display
pixel. Accept direct TTF rendering only if 466×466 captures show hard cell
edges, stable baselines and advances, exact tier alignment, and no gray
antialiasing or filtering on both the emulator and physical watch.

If the renderer softens or misaligns the TTF, use Pixel Operator as CC0 design
source material for a project-owned bitmap glyph system. Store the selected
glyphs as human-reviewable cell matrices and generate exact-size WFF bitmap or
drawable resources deterministically. The fictional hardware grid remains the
authority in either implementation; the font must conform to the display, not
the other way around.

### Glyph scope

Provisional glyph families:

- 5×7 matrix on the fine tier for labels, date, weather, steps, battery, and
  compact values.
- 7×9 or similarly compact matrix on the coarse tier for the primary time.
- Uppercase Latin letters, digits, colon, percent, degree and temperature-unit
  marks, basic punctuation, and a deliberately small set of symbols.
- One-pixel minimum spacing between glyphs within the selected tier.
- Weather icons constrained to 8×8 or 12×12 fine pixels, covering every WFF
  weather condition, and judged at actual wrist distance.

Each glyph pixel resolves to exactly one pixel in its selected tier; it must
not be smoothed into a conventional typeface. The source glyph matrices should
be kept in a human-reviewable form so bitmap resources can be regenerated
deterministically.

### Alternatives reviewed

- Pix32 remains interesting research for a future Chinese/Japanese locale mode,
  but it is not a baseline dependency. Its broad glyph set is unnecessary for
  the first face, and its current license does not grant the modification and
  redistribution freedom needed for subsetting or generated bitmap assets.
- The Minecraft font is not part of the direction. Its highly recognizable game
  identity would turn the design into a themed watch face rather than the
  imagined constrained computer-watch.

## Information hierarchy

Initial information priority:

1. Hour and minute, always dominant.
2. Day and date.
3. Current weather condition and temperature.
4. Step count.
5. Battery state.

Seconds are intentionally absent. The colon is static rather than blinking, so
the time display needs no once-per-second visual update. Do not add heart rate,
calendar events, notification-like content, or a generic complication to the
first composition. Weather and steps use fixed WFF system data so their glyphs,
fallbacks, and alignment remain under the face's control. Consider at most one
configurable complication only after the core identity is proven.

Use short, period-plausible labels and fixed-width alignment. The face may be
information-dense in small regions, but black space is part of the design.

## Baseline composition

Start with a centered stack rather than a simulated rectangular device casing:

```text
             [WX]  21 C
              SAT 15 AUG

                 10:08

              STP 03642
               BAT 82
```

- The time occupies the optical center and largest glyph scale.
- Weather is the top status row, with the quieter date immediately below it;
  steps and battery occupy the lower status region.
- `[WX]` is an 8×8 or 12×12 fine-tier indexed-color condition sprite, not a
  literal label. It uses at most four flat palette entries; the adjacent
  temperature remains white.
- Temperature follows the user's unit. Test both `21 C` / `70 F` and the degree
  mark after Pixel Operator calibration.
- The first step treatment is a fixed-width five-digit counter. Compare
  `STP 03642` with a right-aligned, non-padded value before final approval, and
  define an unclipped six-digit treatment for unusually high counts.
- The weather-icon region doubles as the visual event bay, but any transient
  sprite or color must return to the truthful current condition.
- Top and bottom rows narrow as they approach the circular bezel.
- Nothing important enters the eight-unit overscan region.

### Preliminary fit budget

The two-tier proposal has been checked mathematically, but the following bands
are feasibility evidence rather than approved final placement. Coordinates are
relative to the 450×450 active framebuffer. For the provisional safe circle
with radius `r = 210`, the usable chord at vertical coordinate `y` is:

```text
usable width = 2 × sqrt(r² - (y - 225)²)
```

The estimate assumes a six-fine-pixel fixed advance for 5×7 status glyphs and
a 7×9 coarse time matrix. The chord is evaluated at the edge of each band
farthest from the center.

| Region | Provisional y band | Conservative content | Needed width | Safe chord | Spare |
|---|---:|---|---:|---:|---:|
| Weather | 75–135 | 12×12 icon + `-100 °F` | 280 | 293.9 | 13.9 |
| Date | 145–180 | `SAT 15 AUG` | 300 | 388.3 | 88.3 |
| Time | 190–280 | `23:59` | 330 | 405.3 | 75.3 |
| Steps | 305–340 | `STP 123456` | 300 | 351.4 | 51.4 |
| Battery | 355–390 | `BAT 100%` | 240 | 259.8 | 19.8 |

The time width is `(4 × 7 digit columns + 1 colon column + 4 gaps) × 10 =
330` units. The status estimates allocate six fine pixels, or 30 units, per
character slot. The full vertical allocation leaves 75 units above the weather
band and 60 below the battery band. Its time is ten units below geometric
center; exact optical placement remains open.

This calculation exposes real constraints:

- Weather is the tightest row. Prefer an 8×8 sprite and treat 12×12 as the
  maximum, not the default.
- Integrate stale/error state into the weather sprite instead of appending a
  new field.
- Define compact formatting for extreme temperatures before implementation.
- Do not add another top or bottom information field without recalculating the
  circular fit.
- Do not append an `AM`/`PM` suffix to the coarse time without budgeting it.
- The arithmetic does not prove bezel clearance, renderer sharpness, or 454×454
  scaling; those remain calibration checks.

Weather must have explicit states:

- available and fresh: show the condition icon and temperature;
- available but refresh failed: retain the last value with a small monochrome
  stale marker integrated into the weather-sprite region;
- unavailable: show `WX --` or collapse the weather row without moving the
  time; and
- unknown condition: show a neutral, truthful icon rather than guessing.

This is a starting composition, not a final wireframe. The design pass should
compare the indexed-color interactive state, a localized write-event state,
and a short frame-sequence storyboard without changing the underlying layout.

## Exploratory concept mockups

These generated mockups reflect the current no-seconds information hierarchy,
but still test mood and composition only. They are not production assets or
evidence of renderer geometry. Their exact glyph proportions, weather icon,
spacing, and cell construction are exploratory output rather than approved
requirements. They motivated the two-tier proposal but do not measure or prove
it. The eventual cells, glyphs, and frames must be generated deterministically
from the fictional hardware grid after calibration.

- [Interactive resting state with indexed-color weather](../design/concepts/interactive-indexed-weather.png)
- [Indexed-color weather refresh event](../design/concepts/indexed-weather-refresh.png)
- [Four-frame on-visible storyboard](../design/concepts/on-visible-four-frame-storyboard.png)
- [Reduced ambient state](../design/concepts/ambient-monochrome.png)

## Ambient mode

Ambient mode exposes the machine's base hardware:

- pure black background;
- white hour/minute, with optional compact date only if the pixel budget allows;
- no seconds or blinking colon;
- no weather, steps, or routine battery field;
- no indexed-color plane;
- no animation; and
- no decorative border or inactive status field.

The result must remain below the Wear OS 15% illuminated-pixel limit throughout
a full day and within the WFF ambient memory budget.

As an intentionally pessimistic sanity check, fully illuminating all cells in
four 7×9 coarse digit boxes plus a two-cell colon consumes 16,256 square units.
Fully illuminating eight 5×7 fine date glyph boxes adds 4,480, for a total of
20,736. That is about 13.0% of the centered 225-radius active circle's 159,043
square units. Real outlined glyphs should be substantially lower, but only the
generated ambient frame and WFF validation can establish compliance.

## WFF v2 feasibility boundaries

The intended implementation uses:

- a 466×466 `WatchFace` coordinate space;
- a Pixel Operator TTF during calibration, followed by either a proven crisp
  custom-font rendering or exact-size bitmap/drawable-backed glyphs;
- direct `WEATHER.*`, `STEP_COUNT`, `STEP_GOAL`, and `STEP_PERCENT` data sources
  rather than application code or a required phone companion;
- conditions for weather availability, stale/error state, every condition enum,
  and the user's temperature unit;
- `SequenceImages` / animated image controllers for authored low-frame-rate
  sprites;
- on-visible and time-boundary triggers where supported;
- conditions for actual states such as battery; and
- ambient variants that hide every animation and color event.

Do not use smooth transform animation merely because WFF supports it. Do not
invent notification access or data that a resource-only WFF face cannot obtain;
future external data must arrive through a real complication provider.

## Design validation matrix

Review every serious design on:

1. `wear5-opw3` at 466×466 for primary pixel fidelity.
2. Physical OnePlus Watch 3 at 466×466 for authoritative rendering, bezel,
   brightness, AOD, and wrist-distance judgment.
3. Official `wear5` at 454×454 for WFF scaling behavior.
4. Interactive and ambient modes.
5. 12- and 24-hour time, representative dates, step counts from zero through
   six digits, and low-battery state.
6. Every weather condition plus fresh, stale, unavailable, unknown, Celsius,
   and Fahrenheit cases.
7. Static interactive, localized color-event, and every animation frame.
8. Fine/coarse tier alignment, the provisional 210-unit safe circle, and the
   worst-case width strings from the fit budget.

## Planned implementation slices after design approval

1. Fine/coarse renderer and Pixel Operator specimen calibration only.
2. Deterministic glyph and sprite asset pipeline.
3. Static base composition using fixed representative values, with weather
   above date and the weather sprite as the only persistent color region.
4. Bind WFF weather and step data with complete fallback states.
5. Ambient composition and illuminated-pixel validation.
6. One on-visible low-frame-rate animation.
7. One rare color event.
8. Physical-watch validation and adjustment.
9. Optional complication/configuration work only after the identity is stable.

## Open decisions

- Final Pixel Operator variant or derived primary digit matrix, plus layout
  proportions.
- Confirmation of the provisional 4+1 fine and 8+2 coarse pixel construction
  after physical-watch calibration.
- Final status-region bands, optical time position, safe radius, and weather
  icon size.
- Zero-padded versus right-aligned natural step count, including six-digit
  overflow treatment.
- Square versus subtly rounded illuminated cells; square is the current default.
- Exact indexed weather palette and transient-event colors after AMOLED
  testing.
- Which single animation best introduces the face's personality.
- Public watch-face name and permanent application ID.

## References

- [WFF WatchFace coordinate space](https://developer.android.com/reference/wear-os/wff/watch-face)
- [WFF custom fonts](https://developer.android.com/reference/wear-os/wff/group/part/text/font)
- [WFF bitmap fonts](https://developer.android.com/reference/wear-os/wff/bitmap-fonts)
- [WFF weather data](https://developer.android.com/training/wearables/wff/weather)
- [WFF system data sources](https://developer.android.com/reference/wear-os/wff/common/attributes/source-type)
- [WFF complications](https://developer.android.com/training/wearables/wff/complications)
- [WFF SequenceImages](https://developer.android.com/reference/wear-os/wff/group/part/animated-image/sequence-image)
- [WFF AnimationController](https://developer.android.com/reference/wear-os/wff/group/part/animated-image/animation-controller)
- [Wear OS watch-face quality requirements](https://developer.android.com/docs/quality-guidelines/wear-app-quality)
- [Pixel Operator family and CC0 license](https://www.dafont.com/pixel-operator.font)
- [Pix32 license](https://github.com/32comic/Pix32/blob/main/LICENSE.md)
