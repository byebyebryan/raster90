# Raster 90 — Watch Face Design Direction

Status: the solid single-grid runtime is implemented and live-validated on the
physical 466×466 OnePlus Watch 3 and the 466×466 / 454×454 Wear OS 5 emulators.
It uses one 150×150 framebuffer, solid 3×3 cells, true 16×16 icons, icon-led
single-row values, and centered date text without a calendar icon. Its
unavailable-weather branch uses a neutral icon plus `--` on the same single-row
baseline, while the physical watch proves a fresh available night-weather row.
The project-owned primary variants are now formalized: the selected time cut is
the reviewed clean chamfer, while the square construction and earlier global
fine-chamfer remain named source-only controls. The complete secondary/text
vocabulary remains available for source-only review. The clean-chamfer runtime
has fresh native 466×466 interactive and confirmed Dozing evidence. Physical
clean-chamfer optical judgment, sustained AOD, stale weather, and any animation
or transient color event remain open work.

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

The primary hardware target is the 466×466 OnePlus Watch 3. The current WFF
canvas is also 466×466 so the primary target can be evaluated at 1:1 geometry.
The emulator result is clean, but this must also be proven on the physical watch
before the geometry becomes an implementation invariant.

The packaged runtime places a centered 450×450 fictional framebuffer at `(8,
8)` and treats it as one 150×150 source-pixel display:

```text
physical / WFF canvas: 466×466
active framebuffer:   450×450 at x=8, y=8
source framebuffer:      150×150 pixels
source pixel:                 3×3 solid units
gutter:                       none
```

Every element uses that one physical source pixel. Hierarchy comes from
logical artwork size rather than another pixel tier: 5×7 compact text, true
16×16 icons, and a 32-cell time box. The packaged high-resolution time uses
the directly authored, reviewed clean-chamfer matrices; square and legacy
fine-chamfer variants remain canonical comparison controls with identical box
geometry.

The outer eight-unit margin is overscan, not an information-bearing region. A
provisional circular safe radius of 210 units, centered at `(225, 225)` in
active-framebuffer coordinates, supplies a further 15-unit inset from the
active circle. This is a conservative design margin, not a platform guarantee;
the bezel and physical watch remain authoritative.

### Runtime evidence and remaining gate

The 2026-08-18 solid-grid runtime pass proved crisp solid 3×3 cells at native
466×466, acceptable WFF scaling at 454×454, legible 5×7 compact text, direct
true 16×16 tile geometry, centered/unclipped interactive rows, 12/24-hour time,
and time-only ambient reduction. The 2026-08-20 follow-up promoted the reviewed
clean-chamfer numerals into the runtime and freshly proved the same unclipped
composition in native 466×466 interactive and confirmed Dozing states. The
remaining geometry gate is physical-watch wrist-distance, AMOLED, bezel, AOD,
and low-brightness behavior. Icon recognizability and any later clean-chamfer
optical adjustment remain design judgments rather than runtime geometry
blockers.

The preceding deterministic comparisons selected solid 3×3 cells over both
2×2 solid cells and 3-pitch/2-lit dot-matrix cells. At native mock size, 2×2
cells reduced a 16×16 icon to 32×32 and made the information stack too quiet;
solid 3×3 cells retained the approved 48×48 icon scale while removing the
dither-like one-third gutter. The new emulator captures promote that decision
from design evidence to runtime evidence.

Regenerate or byte-check the runtime mirror and comparison specimens with:

```sh
rtk python3 -B tools/render_raster90_single_grid_study.py
rtk python3 -B tools/render_raster90_single_grid_study.py --check
rtk python3 -B tools/render_raster90_icon_resolution_studies.py --check
rtk python3 -B tools/render_raster90_font_family.py --check
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
rtk python3 -B tools/render_raster90_step_icon_outline_study.py --check
rtk python3 -B -m unittest \
  tools/test_generate_raster90_assets.py \
  tools/test_raster90_fonts.py \
  tools/test_render_raster90_icon_resolution_studies.py \
  tools/test_render_raster90_single_grid_study.py \
  tools/test_raster90_icons.py \
  tools/test_render_raster90_step_icon_outline_study.py
```

Runtime review PNGs and geometry reports remain under the ignored
`outputs/raster90/studies/single-grid/` directory. Solid-grid icon sheets and
full-face decision mocks remain under
`outputs/raster90/studies/icon-resolution/`. The single-grid runtime mirror and
selected true 16×16 matrices correspond to packaged WFF assets. The
authoritative selected icon source is `icons/raster90/family.py`; rejected icon
comparisons, the historical solid step control, and calendar art remain design
evidence only.

The tracked icon component presents the selected utility tiles, every WFF
weather condition as day/night pairs, truthful unavailable/stale treatment,
the native 466×466 face, and magnified 16×16/solid-3×3 inspections. Regenerate
or byte-check it with:

```sh
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
```

The approved steps source is the project-owned `four-toe-vertical` matrix:
closed tapered soles, one vertical 1×2 big-toe line, and three separate 1×1
toe marks per footprint. This replaces only the runtime steps tile and derived
previews; weather and battery runtime PNG bytes remain stable.

The earlier two-tier V1 used a 90×90 5/4 fine raster and aligned 45×45 10/8
coarse time tier. It is now historical implementation evidence; the packaged
runtime uses the single solid 3×3 grid.

The historical calibration face established the raster before V1. It contained:

- alternating 4-unit light / 1-unit dark fine runs;
- alternating 8-unit light / 2-unit dark coarse runs;
- adjacent fine and coarse pixels proving their shared origin and exact 2×
  relationship;
- isolated lit cells and horizontal/vertical gutters at both tiers;
- checkerboards and adjacent cell clusters;
- representative bitmap glyphs; and
- marks at the active-framebuffer and circular-safe-area boundaries.

Original-resolution single-grid captures now prove crisp cell edges at native
466×466 and clean, unclipped WFF scaling at 454×454. The physical watch remains
authoritative for AMOLED appearance, bezel clearance, brightness, AOD, and
wrist-distance judgment.

The current composition lives in `:watchfaces:raster90`, application ID
`io.github.byebyebryan.raster90.watchface`. On 2026-08-18 its live native
466×466 and scaled 454×454 renders preserved the intended hierarchy and reduced
ambient mode to time alone. This is emulator evidence; physical-watch
validation remains open.

## Fictional hardware contract

Treat the packaged design as though it runs on the following imaginary display
controller. The historical 3/2 runtime was an earlier implementation of this
fiction rather than the current visual target:

- One 150×150 source framebuffer; every visible cell is one solid 3×3 square
  with no internal gutter.
- Black is unlit; white is the normal illuminated state.
- Text, icons, and time use the same physical source pixels. They gain hierarchy
  from their authored matrices rather than different pixel sizes.
- Persistent icons are authored directly at true 16×16 resolution. Weather,
  steps, and battery use icons; the centered date is text-only. A single weather
  tile may use the indexed-color plane; all other resting content remains
  monochrome.
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
display 256 colors or to use eight bits per RGB channel. The face uses a small fixed
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

V1 deliberately takes the project-owned bitmap path. The authoritative family
matrices live in `fonts/raster90/family.py`; compatibility aliases and non-font
study matrices remain in `design/raster90/matrices.py`.
`tools/generate_raster90_assets.py` expands the approved runtime subsets into
exact-size WFF bitmap-font and sprite resources. The four
approved Pixel Operator source files and their CC0 provenance remain under
`third_party/pixel-operator/`, outside the packaged watch-face resources. The
fictional hardware grid is the authority: the font conforms to the display,
not the other way around.

### Glyph scope

Selected compact-glyph contract:

- 5×7 compact matrices use one line vertically centered inside each 16-cell
  information band. The selected resting face does not stack a header above a
  value.
- Primary/display digits use fixed 26×32 source-cell boxes and a 10×32 colon
  box, with the selected reviewed clean chamfer and a plain closed zero. The
  retained square and legacy fine-chamfer controls share the same geometry;
  total 342-unit WFF time geometry remains unchanged.
- Secondary/text glyphs are project-owned 5×7 matrices: ordinary glyphs advance
  six source cells (18 WFF units), while the literal space advances two cells
  (6 units). The source-only vocabulary includes lowercase and common
  punctuation; the packaged subset is only what current WFF expressions emit.
- The degree mark is a closed ring or box. The earlier open upper semicircle is
  a corrected V1 glyph defect, not part of the visual language.
- Design fixtures and the watch-face setting default use Celsius. The editor
  offers exactly one explicit override, Fahrenheit. Runtime weather converts
  the provider's integer when its preferred unit differs from the selected
  output (using rounded `F -> C` or `C -> F` arithmetic) and always labels the
  selected output unit.
- One-source-pixel minimum spacing between glyphs.
- Weather icons must cover every WFF condition on uniform 16×16 tiles and be
  judged at actual wrist distance.

Each glyph cell resolves to exactly one solid 3×3 source pixel; it must not be
smoothed into a conventional typeface. The source glyph matrices should remain
human-reviewable so bitmap resources and the complete tracked font presentation
can be regenerated deterministically:

```sh
rtk python3 -B tools/render_raster90_font_family.py
rtk python3 -B tools/render_raster90_font_family.py --check
```
The generated overview and specimen sheets live under
`fonts/raster90/preview/` and embed no external assets or runtime dependencies.

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

The selected direction has one icon resource class: a true 16×16 source matrix
rendered with solid 3×3 cells as a 48×48 WFF tile. Weather, steps, battery,
unknown, stale-state, and event art use that canvas or an explicitly registered
overlay within it. There is no utility-versus-feature size split. The calendar
icon is intentionally absent because `SAT 15 AUG` is already semantically
complete.

The art should occupy broadly comparable optical bounds instead of forcing
every shape into an identical square silhouette. A wide battery and the paired
footprints may have different bounding rectangles, but neither should read as
a small marker beside a dominant weather illustration. Transparent edge cells
remain available for centering, animation registration, and condition-to-
condition stability.

The historical 3/2 runtime exposed why this redesign was required: its weather
art was integer-expanded from 8×8 and much of its utility geometry followed
paired cells, so a nominal 16×16 canvas still carries roughly 8×8 effective
detail. Fractional nearest-neighbour scaling is also forbidden because it gives
opposing strokes different thicknesses. Canvas dimensions and effective art
resolution must never be described as the same thing.

Deterministic studies under
`outputs/raster90/studies/icon-resolution/` compared true 8×8 solid art, true
16×16 dot-matrix art, and the same true 16×16 art with solid cells. The selected
solid 16×16 family was then polished for centered calendar geometry, a readable
walking figure, a flat battery terminal, and a weather stale marker shown in
context. Subsequent full-face mocks selected 3×3 over 2×2 cells, one text row
over two, removal of `WX`/`STP`/`BAT`, and finally removal of the calendar icon.
After wearer review of the physical-watch runtime rejected the walking figure,
a focused native-size study selected direct-authored paired footprints. Their
separated toe pads and vertically offset, tapered soles remain recognizable
beside the count at the native 3×3-cell scale.
The generated footprint asset was then live-validated in the packaged WFF on
the native 466×466 `wear5-opw3` emulator; physical-watch appearance remains a
separate wearer-review gate.

The selected project-owned matrices in
`design/raster90/icon_resolution_studies.py` are now consumed directly by the
packaged generator so study, preview, and runtime art cannot drift. A validator
rejects 16×16 candidates that are merely duplicated 8×8 blocks. Opposing
structural edges must retain balanced source-cell weight before whole-face WFF
scaling is considered.

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

Resting-face information priority:

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

Use short, period-plausible values and fixed-width alignment. Do not add a text
header where the selected icon already communicates the field. The face may be
information-dense in small regions, but black space is part of the design.

## Resting composition

### Packaged solid-grid composition

The packaged available-weather layout uses the following centered stack:

```text
              [weather] 21°C
                 SAT 15 AUG

                    10:08

           [footprints] 03642
              [battery] 82%
```

- The weather, steps, and battery icons carry their own semantics, so `WX`,
  `STP`, and `BAT` are intentionally absent.
- `SAT 15 AUG` is centered without a calendar icon. `SAT` remains because it is
  day-of-week data, not a field header.
- Weather temperature is Celsius by default with an explicit Fahrenheit choice
  in the editable watch-face configuration. The WFF provider's preferred unit
  is a data source, not the user's selected display unit: a mismatched provider
  value is converted with integer rounding before formatting.
- Each ordinary value uses one 5×7 line vertically centered inside its existing
  16-cell band.
- The runtime retains the established row bands and time position to
  isolate the approved content changes. Weather/date spacing may receive a
  later explicit optical pass.
- The available-state layout is implemented. The unavailable branch keeps the
  same row and time position while showing a neutral icon plus `--` on one
  line. The stale marker is implemented but still lacks live-data validation.

### Historical 3/2 runtime baseline

The preceding 3/2 runtime used this centered stack rather than a simulated
rectangular device casing:

```text
             [weather] WX
                       21°C
            [calendar] SAT
                       15 AUG

                    10:08

              [walker] STP
                       03642
             [battery] BAT
                       82%
```

- The time occupies the optical center and largest glyph scale.
- Weather is the top status row, with the quieter date immediately below it;
  steps and battery occupy the lower status region.
- `[weather]` is a uniform 16×16 indexed-color condition sprite, not a literal
  label. It uses at most four flat palette entries; the adjacent temperature
  remains white. Calendar, walker, and battery use monochrome 16×16 tiles.
- Temperature follows the user's unit and includes the degree mark.
- Step counts through 99,999 use the fixed-width `STP 03642` treatment. Six
  digits use the same narrow separator as `STP 123456`; values above 999,999
  clamp instead of clipping.
- The weather-icon region doubles as the visual event bay, but any transient
  sprite or color must return to the truthful current condition.
- Top and bottom rows narrow as they approach the circular bezel.
- Nothing important enters the eight-unit overscan region.

### Historical 3/2 single-grid composition

V1 proves the bitmap typography, live data bindings, and ambient reduction, but
its unavailable-weather state and `STP` / `BAT` labels leave the resting face
too close to a text-only segmented watch. That composition is an implementation
baseline, not the final visual-density target.

That candidate used an exact 1:2:4 logical rhythm on the single 3/2 pixel grid:

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

Each 16-cell information row contained one icon and two 8-cell text lines. The
layout was one centered vertical stack, not a two-column face. Those baseline
matrices and integer-normalized weather art are retained as comparison evidence.

### Packaged solid-grid fit budget

The packaged solid-grid runtime uses the following bands relative to the
450×450 active framebuffer. They remain subject to physical-watch optical
adjustment. For the provisional safe circle with radius `r = 210`, the usable
chord at vertical coordinate `y` is:

```text
usable width = 2 × sqrt(r² - (y - 225)²)
```

The estimate uses 18-unit ordinary compact-glyph advances, a 6-unit literal
space, solid 48×48 icon tiles, 78-unit time digits, and a 30-unit colon. The
chord is evaluated at the edge of each band farthest from the center.

| Region | Active-frame y band | Conservative content | Needed width | Safe chord | Spare |
|---|---:|---|---:|---:|---:|
| Weather | 45–93 | 16×16 icon + `-100°F` | 162 | 216.3 | 54.3 |
| Date | 111–159 | centered `SAT 31 DEC` | 156 | 352.7 | 196.7 |
| Time | 177–273 | `23:59` | 342 | 408.9 | 66.9 |
| Steps | 291–339 | 16×16 icon + `123456` | 162 | 352.7 | 190.7 |
| Battery | 357–405 | 16×16 icon + `100%` | 126 | 216.3 | 90.3 |

Every adjacent row box retains an explicit 18-unit gap. The visible stack leaves
45 units above weather and below battery, while the 96-unit time box is centered
exactly at active-frame `y=225`. The time width is four 78-unit digit advances
plus a 30-unit colon separator in one low-cost `TimeText`.

This calculation exposes real constraints:

- Weather, steps, and battery use the same true 16×16 tile; date is text-only.
- Integrate stale/error state into the weather sprite instead of appending a
  new field.
- The current `%d°%s` formatter fits the documented `-100°F` width budget;
  broader out-of-contract extremes require a deliberate compact policy.
- Do not add another top or bottom information field without recalculating the
  circular fit.
- Do not append an `AM`/`PM` suffix to the time without budgeting it.
- The arithmetic and emulator captures do not prove physical bezel clearance or
  AMOLED appearance; those remain physical-watch checks.

Current weather has explicit states:

- available and fresh: show the condition icon and temperature;
- available but refresh failed: retain the last value with a small monochrome
  stale marker integrated into the weather-sprite region;
- unavailable: show the neutral icon plus `--` on one line without moving the
  row or time; and
- unknown condition: show a neutral, truthful icon rather than guessing.

The available-state generated preview is deterministic. Live emulator testing
proves the unavailable branch at 466×466 and 454×454; available and stale live
data still need a connected/location-capable target. A future event or
storyboard must preserve this resting layout.

## Exploratory concept mockups

These generated mockups reflect the current no-seconds information hierarchy,
but still test mood and composition only. They are not production assets or
evidence of renderer geometry. Their exact glyph proportions, weather icon,
spacing, and cell construction are exploratory output rather than approved
requirements. They motivated the eventual single-grid hierarchy but do not
measure or prove it. Production cells, glyphs, and frames are generated
deterministically from the fictional hardware grid.

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

For the historical 3/2 runtime, an intentionally pessimistic full-box bound was
`114 × 32 × 4 = 14,592` lit units. For the packaged solid grid that same bound
is too pessimistic at `114 × 32 × 9 = 32,832`, so ambient review uses actual
glyph occupancy. Across every 24-hour `HH:MM` value, the approved primary cut
peaks at `08:08`: 1,526 live source cells, or 13,734 solid units, about 8.64% of
the centered 225-radius active circle's 159,043 units. That is below the 15%
design limit. For the packaged solid runtime, the official evaluator reports
155,520 maximum ambient bytes conservatively; its optional optimization estimate
reports 104,004 bytes. Any later optical revision must repeat the occupancy and
evaluator checks.

## WFF v2 feasibility boundaries

The current implementation uses:

- a 466×466 `WatchFace` coordinate space;
- exact-size bitmap/drawable-backed glyphs derived from reviewable matrices;
- direct `WEATHER.*`, `STEP_COUNT`, and `BATTERY_PERCENT` data sources
  rather than application code or a required phone companion;
- conditions for truthful weather availability, stale state, day/night and all
  condition enum values, using the selected temperature unit (Celsius by
  default, with an explicit Fahrenheit override); and
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
8. Solid 3×3 cell consistency, the provisional 210-unit safe circle, actual
   ambient glyph occupancy, and the worst-case width strings from the fit
   budget.

## Implementation slices

The implementation has reached these emulator-proven slices:

1. Historical fine/coarse renderer and Pixel Operator specimen calibration.
2. Deterministic glyph and sprite asset pipeline.
3. Functional V1 data bindings and truthful fallback behavior.
4. Single-grid geometry, icon, and time studies.
5. Packaged single-grid composition and matching generated preview.
6. Live WFF time, date, weather, step, and battery bindings with truthful
   weather fallback states.
7. Time-only ambient composition, 12/24-hour sync, dual-size renderer checks,
   validator, and memory-footprint gates.
8. Packaged solid 3×3 cells, direct true 16×16 icons, icon-led one-line values,
   text-only date, deterministic preview parity, and live 466×466 / 454×454
   interactive and ambient validation.
9. Canonical project-owned square and clean-chamfer primary cuts, with the
   reviewed clean chamfer selected and freshly renderer-validated in native
   466×466 interactive and confirmed Dozing states.

Later slices remain separately gated:

10. Live-test stale weather after proving fresh available and truthful,
   header-free unavailable states.
11. Complete physical-watch wearer, sustained-AOD, and battery validation and
    adjustment.
12. Clean-chamfer and icon-family optical polish driven by physical wear.
13. One on-visible low-frame-rate animation.
14. One rare color event.
15. Optional complication/configuration work only after the identity is stable.

## Open decisions

- Wearer confirmation of the packaged solid 3×3 cells, AMOLED appearance, and
  wrist-distance legibility; native physical-device rendering is proven.
- Whether weather/date spacing needs an explicit optical adjustment after the
  calendar icon is removed.
- Physical-watch adjustment of the single-grid bands, optical time position,
  safe radius, solid cells, and indexed weather palette.
- Whether physical wear calls for a further clean-chamfer optical adjustment;
  the selected cut is already directly authored and emulator-proven.
- Optical refinement of the selected true 16×16 icon family.
- Live verification of stale, day-family, explicit-Fahrenheit-selection, and
  extreme-value weather branches; fresh available, night-family, and the provider's
  Fahrenheit surface are proven. The emulator editor proves the Celsius
  default and both choices are reachable; resource tests cover both conversion
  directions, and the physical watch proves a live converted `17°C` default.
  Physical Fahrenheit selection is not required for the Celsius-default gate.
- The physical WFF provider returned `63°F` under the watch's `en-US` locale
  while the separate OnePlus Weather tile displayed `20°` under its own
  Celsius preference/setting; the capture did not literally show `20°C`. These
  are separate provider/cache surfaces; the Raster 90 setting converts and
  labels its own WFF value but does not synchronize those readings.
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
