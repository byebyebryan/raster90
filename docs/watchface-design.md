# Raster 90 — Watch Face Design Direction

Status: Raster 90 V1 is implemented and validated on the 466×466 and 454×454
Wear OS 5 emulators. Physical-watch rendering, live available/stale weather,
and any animation or transient color event remain open validation or post-V1
work.

## Product identity

- Public name: **Raster 90**.
- Optional visual styling: **RASTER/90**.
- `Raster` names the visible bitmap-display language without implying a
  seven-segment or modern high-fidelity screen.
- `90` refers to the provisional 90×90 fine raster while also reading as an
  imagined hardware model number. It remains the product designation if
  physical calibration changes the exact raster geometry.

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
The emulator result is encouraging, but this must also be proven on the
physical watch before it becomes an implementation invariant.

Place a centered 450×450 fictional framebuffer at `(8, 8)`. The post-V1
direction treats it as one 150×150 source-pixel display:

```text
physical / WFF canvas: 466×466
active framebuffer:   450×450 at x=8, y=8
source framebuffer:      150×150 pixels
source pixel pitch:          3×3 units
lit square:                  2×2 units
gutter:                      1 unit right and below each lit square
```

Every element uses that same physical source pixel. Hierarchy comes from its
logical box: an 8-pixel text line, a uniform 16×16 icon tile, or a 32-pixel time
line. The initial high-resolution time study expands the proven V1 numeral
silhouettes only to isolate pixel-pitch behavior; final numerals must be
authored for the finer matrix rather than becoming mechanically enlarged V1
art.

The outer eight-unit margin is overscan, not an information-bearing region. A
provisional circular safe radius of 210 units, centered at `(225, 225)` in
active-framebuffer coordinates, supplies a further 15-unit inset from the
active circle. This is a conservative design margin, not a platform guarantee;
the bezel and physical watch remain authoritative.

### Calibration gate

The 3/2 source pixel is provisional until exact-size studies prove:

- crisp 2×2 lit squares and one-unit gutters at native 466×466;
- acceptable WFF scaling on the official 454×454 reference;
- legible 5×7 compact text inside an 8-pixel line box;
- readable uniform 16×16 icon tiles with comparable optical scale;
- a detailed time treatment using the same physical pixels; and
- physical-watch wrist-distance, AMOLED, and low-brightness behavior.

Regenerate or byte-check the design-only specimens with:

```sh
rtk python3 -B tools/render_raster90_single_grid_study.py
rtk python3 -B tools/render_raster90_single_grid_study.py --check
rtk python3 -B -m unittest tools/test_render_raster90_single_grid_study.py
```

The review PNGs and geometry reports remain under the ignored
`outputs/raster90/studies/single-grid/` directory. They do not modify WFF
geometry or packaged single-grid assets.

The packaged V1 intentionally remains on its earlier two-tier geometry while
this gate is open. That implementation uses a 90×90 5/4 fine raster and an
aligned 45×45 10/8 coarse time tier. It is historical implementation evidence,
not the post-V1 design target.

The historical calibration face established the raster before V1. It contained:

- alternating 4-unit light / 1-unit dark fine runs;
- alternating 8-unit light / 2-unit dark coarse runs;
- adjacent fine and coarse pixels proving their shared origin and exact 2×
  relationship;
- isolated lit cells and horizontal/vertical gutters at both tiers;
- checkerboards and adjacent cell clusters;
- representative bitmap glyphs; and
- marks at the active-framebuffer and circular-safe-area boundaries.

Original-resolution V1 captures now prove crisp cell edges at native 466×466
and clean, unclipped WFF scaling at 454×454. The physical watch remains
authoritative for AMOLED appearance, bezel clearance, brightness, AOD, and
wrist-distance judgment.

The calibration scaffold has been replaced by the functional V1 composition in
`:watchfaces:raster90`, application ID
`io.github.byebyebryan.raster90.watchface`. On 2026-08-17 its live native
466×466 and scaled 454×454 renders preserved the intended hierarchy and reduced
ambient mode to time alone. The system charging indicator still occupies the
bottom-center edge, below V1's information stack. This is emulator evidence;
physical-watch validation remains open.

## Fictional hardware contract

Treat the face as though it runs on the following imaginary display controller:

- One 150×150 source framebuffer; every visible cell has a 3-unit pitch, a 2×2
  lit square, and a one-unit gutter.
- Black is unlit; white is the normal illuminated state.
- Text, icons, and time use the same physical source pixels. They gain hierarchy
  from 8-, 16-, and 32-pixel logical boxes rather than different pixel sizes.
- Every persistent icon uses one uniform 16×16 tile. A single weather tile may
  use the indexed-color plane; all other resting content remains monochrome.
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
display 256 colors or to use eight bits per RGB channel. V1 uses a small fixed
palette, with at most four flat visible entries in one weather sprite: yellow
`#FFD800`, pale cyan `#49DFFF`, medium blue `#2474FF`, and white. Physical
AMOLED judgment can refine these values later without changing the indexed
color contract.

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

The historical calibration specimen compared:

- `PixelOperatorMonoHB` for the primary time because its fixed advances prevent
  the clock from shifting as digits change and its intermediate weight remains
  open at small sizes;
- `PixelOperatorMono` for compact values and labels; and
- `PixelOperatorMono8` and `PixelOperatorMonoHB8` as coarse-display alternatives
  for the oversized time.

V1 deliberately takes the project-owned bitmap path. Human-reviewable matrices
live in `design/raster90/matrices.py`; `tools/generate_raster90_assets.py`
expands them into exact-size WFF bitmap-font and sprite resources. The four
approved Pixel Operator source files and their CC0 provenance remain under
`third_party/pixel-operator/`, outside the packaged watch-face resources. The
fictional hardware grid is the authority: the font conforms to the display,
not the other way around.

### Glyph scope

Provisional glyph families:

- 5×7 compact matrices centered in 8-pixel-high line boxes for labels and
  values. Two such lines fit beside one 16×16 icon tile.
- Approximately 26×30 live digit matrices inside a 32-pixel-high time line.
  Time uses the same 3/2 source pixels as every other element; it does not have
  a coarse physical pixel mode.
- Uppercase Latin letters, digits, colon, percent, degree and temperature-unit
  marks, basic punctuation, and a deliberately small set of symbols.
- Compact ordinary glyphs provisionally advance six source pixels (18 WFF
  units); the literal space is two source pixels (6 units).
- The degree mark is a closed ring or box. The earlier open upper semicircle is
  a corrected V1 glyph defect, not part of the visual language.
- Design fixtures use Celsius. Live weather remains synchronized to the user's
  preferred unit unless a future explicit Raster 90 unit setting is approved.
- One-source-pixel minimum spacing between glyphs.
- Weather icons must cover every WFF condition on uniform 16×16 tiles and be
  judged at actual wrist distance.

Each glyph pixel resolves to exactly one pixel in its selected tier; it must
not be smoothed into a conventional typeface. The source glyph matrices should
be kept in a human-reviewable form so bitmap resources can be regenerated
deterministically.

### Icon source and canvas roles

[Pixelarticons](https://github.com/halfmage/pixelarticons) is a visual-research
reference, not a Raster 90 dependency or asset source. Its public/free subset
and paid catalog have different distribution boundaries, and its nominal
24×24 SVG canvas generally produces a much smaller, roughly 12×12 visual
density through two-unit marks. For the current design pass:

- do not add its package, vendor its SVGs, or mechanically trace or downsample
  them;
- use it to study how recognizable symbols are reduced to a sparse pixel
  vocabulary; and
- continue authoring Raster 90 icons independently as project-owned,
  human-reviewable matrices. If direct reuse is proposed later, pin the exact
  upstream revision and review the license of every selected asset first.

The post-V1 direction has one icon resource class: a 16×16 source matrix on the
3/2 grid, rendered as a 48×48 WFF tile. Weather, calendar, steps, battery,
unknown, and event art all use that canvas. There is no utility-versus-feature
size split.

The art should occupy broadly comparable optical bounds instead of forcing
every shape into an identical square silhouette. A wide battery and a tall
walker may have different bounding rectangles, but neither should read as a
small marker beside a dominant weather illustration. Transparent edge cells
remain available for centering, animation registration, and condition-to-
condition stability.

The implemented V1 8×8 weather sprites and the subsequent 8×8/12×12 studies are
retained as evidence: they showed that the smaller grid could not express
weather and figures consistently, while a physically larger weather-only tile
made the composition top-heavy. They are not the selected post-V1 system.

### Alternatives reviewed

- Pix32 remains interesting research for a future Chinese/Japanese locale mode,
  but it is not a baseline dependency. Its broad glyph set is unnecessary for
  the first face, and its current license does not grant the modification and
  redistribution freedom needed for subsetting or generated bitmap assets.
- The Minecraft font is not part of the direction. Its highly recognizable game
  identity would turn the design into a themed watch face rather than the
  imagined constrained computer-watch.

## Information hierarchy

V1 information priority:

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

V1 uses a centered stack rather than a simulated rectangular device casing:

```text
             [WX]  21°C
              SAT 15 AUG

                 10:08

              STP 03642
              BAT 82%
```

- The time occupies the optical center and largest glyph scale.
- Weather is the top status row, with the quieter date immediately below it;
  steps and battery occupy the lower status region.
- `[WX]` is an 8×8 or 12×12 fine-tier indexed-color condition sprite, not a
  literal label. It uses at most four flat palette entries; the adjacent
  temperature remains white.
- Temperature follows the user's unit and includes the degree mark.
- Step counts through 99,999 use the fixed-width `STP 03642` treatment. Six
  digits use the same narrow separator as `STP 123456`; values above 999,999
  clamp instead of clipping.
- The weather-icon region doubles as the visual event bay, but any transient
  sprite or color must return to the truthful current condition.
- Top and bottom rows narrow as they approach the circular bezel.
- Nothing important enters the eight-unit overscan region.

### Post-V1 single-grid revision

V1 proves the bitmap typography, live data bindings, and ambient reduction, but
its unavailable-weather state and `STP` / `BAT` labels leave the resting face
too close to a text-only segmented watch. That composition is an implementation
baseline, not the final visual-density target.

The next study uses an exact 1:2:4 logical rhythm on the single 3/2 pixel grid:

```text
15 cells  top margin
16 cells  weather icon plus two 8-cell text lines
 6 cells  gap
16 cells  calendar icon plus two 8-cell text lines
 6 cells  gap
32 cells  high-resolution time on the same source pixels
 6 cells  gap
16 cells  walking icon plus two 8-cell text lines
 6 cells  gap
16 cells  battery icon plus two 8-cell text lines
15 cells  bottom margin
────────
150 cells
```

The first text arrangement to test is:

```text
[ weather ]  WX       [ calendar ]  SAT
[  16×16  ]  21°C     [   16×16  ]  15 AUG

                  10:08

[  walker  ]  STP      [ battery ]  BAT
[  16×16   ]  03642    [  16×16  ]  82%
```

This notation illustrates the two-line relationship, not a two-column face;
the initial runtime study retains one centered vertical stack. All icons are
independently authored project matrices, the degree mark is closed, and study
fixtures default to Celsius.

Review the 3/2 system at native 466×466 and scaled 454×454 size before changing
runtime geometry, then repeat it on the physical watch. The following table is
retained only as the implemented V1 fit budget; a selected single-grid layout
must replace it with newly calculated geometry.

### V1 fit budget

The following implemented bands are relative to the 450×450 active framebuffer.
They remain subject to physical-watch optical adjustment. For the provisional
safe circle with radius `r = 210`, the usable chord at vertical coordinate `y`
is:

```text
usable width = 2 × sqrt(r² - (y - 225)²)
```

The estimate assumes a 30-unit ordinary fine-glyph advance (with the shared
10-unit literal-space separator) for 5×7 status glyphs and a 7×9 coarse time
matrix. The chord is evaluated at the edge of each band farthest from the
center.

| Region | V1 y band | Conservative content | Needed width | Safe chord | Spare |
|---|---:|---|---:|---:|---:|
| Weather | 65–105 | 8×8 icon + `-100°F` | 230 | 272.0 | 42.0 |
| Date | 125–160 | `SAT 15 AUG` | 260 | 369.3 | 109.3 |
| Time | 180–270 | `23:59` | 350 | 410.2 | 60.2 |
| Steps | 290–325 | `STP 123456` | 280 | 369.3 | 89.3 |
| Battery | 345–380 | `BAT 100%` | 220 | 283.4 | 63.4 |

Every adjacent row box has an explicit 20-unit gap. The visible stack leaves
65 units above weather and 70 below battery, while the 90-unit time box is
centered exactly at active-frame `y=225`. The time width is four 80-unit digit
advances plus a 30-unit colon separator. Its two lit coarse cells are followed
by one blank cell; the preceding digit's trailing blank supplies the matching
leading separation, preventing the colon from fusing with minute digits while
retaining a single low-cost `TimeText`.

This calculation exposes real constraints:

- Weather uses the 8×8 sprite. A 12×12 sprite combined with the extreme
  temperature string would exceed the revised top-row budget.
- Integrate stale/error state into the weather sprite instead of appending a
  new field.
- Define compact formatting for extreme temperatures before implementation.
- Do not add another top or bottom information field without recalculating the
  circular fit.
- Do not append an `AM`/`PM` suffix to the coarse time without budgeting it.
- The arithmetic and emulator captures do not prove physical bezel clearance or
  AMOLED appearance; those remain physical-watch checks.

V1 weather has explicit states:

- available and fresh: show the condition icon and temperature;
- available but refresh failed: retain the last value with a small monochrome
  stale marker integrated into the weather-sprite region;
- unavailable: show `WX --` without moving the time; and
- unknown condition: show a neutral, truthful icon rather than guessing.

The available-state generated preview is deterministic. Live emulator testing
proved the unavailable `WX --` branch; available and stale live data still need
a connected/location-capable target. A future event or storyboard must preserve
this resting layout.

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
- white hour/minute only;
- no seconds or blinking colon;
- no weather, steps, or routine battery field;
- no indexed-color plane;
- no animation; and
- no decorative border or inactive status field.

The result must remain below the Wear OS 15% illuminated-pixel limit throughout
a full day and within the WFF ambient memory budget.

As an intentionally pessimistic full-digit-cell bound, four fully lit 7×9
coarse digit matrices contribute `4 × 7 × 9 × 64 = 16,128` square units. The
colon's two 2×2 dots contribute eight lit coarse cells, or `8 × 64 = 512`
square units; together they consume 16,640 square units, about 10.5% of the
centered 225-radius active circle's 159,043 square units. Real outlined glyphs
are substantially lower. The official evaluator reports 149,400 maximum
ambient bytes for the current typography revision.

## WFF v2 feasibility boundaries

The V1 implementation uses:

- a 466×466 `WatchFace` coordinate space;
- exact-size bitmap/drawable-backed glyphs derived from reviewable matrices;
- direct `WEATHER.*`, `STEP_COUNT`, and `BATTERY_PERCENT` data sources
  rather than application code or a required phone companion;
- conditions for truthful weather availability, stale state, day/night and all
  condition enum values, using the user's temperature unit; and
- an ambient variant that hides every non-time field.

WFF v2 event controllers and `SequenceImages` remain feasible post-V1 tools,
not part of the resting-face implementation.

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

## Implementation slices

Slices 1–5 form V1 and are complete on both emulators:

1. Fine/coarse renderer and Pixel Operator specimen calibration.
2. Deterministic glyph and sprite asset pipeline.
3. Static base composition and matching generated preview.
4. Live WFF time, date, weather, step, and battery bindings with truthful
   weather fallback states.
5. Time-only ambient composition plus validator and memory-footprint gates.

Later slices remain separately gated:

6. Physical-watch validation and adjustment.
7. One on-visible low-frame-rate animation.
8. One rare color event.
9. Optional complication/configuration work only after the identity is stable.

## Open decisions

- Confirmation of the provisional 4+1 fine and 8+2 coarse pixel construction
  after physical-watch calibration.
- Physical-watch adjustment of the V1 bands, optical time position, safe radius,
  square cells, and indexed weather palette.
- Live verification of available, stale, day/night, Celsius/Fahrenheit, and
  extreme-value weather branches.
- Which single animation best introduces the face's personality.

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
