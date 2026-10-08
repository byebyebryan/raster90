# Design evolution and earlier planning

Historical excerpts retained during the 2026-10-07 reconciliation. They record
previous visual decisions, studies, and acceptance notes and are not the
current product contract. Use [Design](../watchface-design.md) and
[Validation](../validation.md) for current intent and evidence.

# Raster 90 — Watch Face Design Direction

Status: the solid single-grid design is implemented. Runtime checkpoints cover
native 466×466 physical rendering and native 466×466 / 454×454 Wear OS
emulation, using one 150×150 framebuffer, solid 3×3 cells, 16×16 icon storage
tiles with 15×15 drawable fields centered on cell `(7,7)`,
icon-led single-row values, and centered date text without a calendar icon. The
unavailable-weather branch uses a neutral icon plus `--` on the same single-row
baseline. The 2026-08-26 physical checkpoint now proves the exact packaged
tree's interactive composition with the final footprint tile, clean-chamfer
time, refreshed clear-night crescent, and live available weather at `18°C`.

The project-owned primary variants are formalized: the selected time cut is the
reviewed clean chamfer, while the square construction and earlier global
fine-chamfer remain named source-only controls. The 2026-08-20 native
`wear5-opw3` checkpoint freshly proved clean-chamfer interactive and Dozing
rendering after `b7ffa65`. Commit `33e2912` then promoted the canonical icon
family and changed the packaged steps PNG and tracked previews. A fresh
2026-08-21 capture of then-current HEAD `cf597af` proves the final
`four-toe-vertical` tile and clean-chamfer time together, including simulated
available weather at `15°C` and time-only Dozing. The later physical checkpoint
at packaged runtime `4a90116` proves the refreshed static weather art and full
interactive composition on the watch. Sustained physical AOD, perceived AMOLED
and wrist-distance judgment, stale weather, low-battery tint branches, battery
impact, and any transient color event remain open work. The weather animation
is now promoted into the current source tree, but fresh emulator and physical-
device evidence for that animated tree remains open.



### Runtime evidence and remaining gate

The 2026-08-18 solid-grid runtime pass proved crisp solid 3×3 cells at native
466×466, acceptable WFF scaling at 454×454, legible 5×7 compact text, direct
true 16×16 tile geometry, centered/unclipped interactive rows, 12/24-hour time,
and time-only ambient reduction. The 2026-08-20 follow-up promoted the reviewed
clean-chamfer numerals into the runtime and freshly proved the same unclipped
composition in native 466×466 interactive and confirmed Dozing states. Those
two checkpoints predate `33e2912`'s final icon-family promotion. The
2026-08-21 checkpoint closed that tree's emulator gap: it proves the final
steps tile, clean-chamfer time, complete rows, simulated available weather, and
Dozing time-only behavior. The 2026-08-26 physical checkpoint then proved the
refreshed packaged tree's interactive geometry, live clear-night weather, and
complete rows without clipping. The remaining gates are sustained physical
AOD, wrist-distance, AMOLED, bezel, and low-brightness behavior. Icon
recognizability and any later clean-chamfer optical adjustment remain design
judgments rather than runtime geometry blockers.

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
selected 16×16 storage matrices with 15×15 drawable fields correspond to
packaged WFF assets. The
authoritative selected icon source is `icons/raster90/family.py`; rejected icon
comparisons, the historical solid step control, and calendar art remain design
evidence only.

The tracked icon component presents the selected utility tiles, every WFF
weather condition as day/night pairs, truthful unavailable/stale treatment,
and a native-size 466×466 face presentation view, plus magnified
16×16/solid-3×3 inspections. These are tracked source/presentation fixtures,
not a post-promotion WFF runtime capture. Regenerate or byte-check it with:

```sh
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
```

The approved steps source is the project-owned `four-toe-vertical` matrix:
closed tapered soles, one vertical 1×2 big-toe line, and three separate 1×1
toe marks per footprint. The `33e2912` promotion replaced only the runtime steps
tile and derived previews at that checkpoint. It followed the earlier clean-
chamfer emulator capture, and the 2026-08-21 checkpoint then proved the promoted
steps tile in WFF with weather from a simulated GPS test provider. The later
`fccd4ef` / `4a90116` refresh changed the authored weather matrices and their
packaged PNGs while preserving the WFF mapping and behavior. The 2026-08-26
physical capture proves the final footprints and refreshed outlined clear-night
crescent together with live provider weather.

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

The historical original-resolution single-grid captures prove crisp cell edges
at native 466×466 and clean, unclipped WFF scaling at 454×454. The current
physical checkpoint proves native interactive renderer geometry; the watch
remains authoritative for perceived AMOLED appearance, bezel clearance,
brightness, sustained AOD, and wrist-distance judgment.

The current composition lives in `:watchfaces:raster90`, application ID
`io.github.byebyebryan.raster90.watchface`. The 2026-08-18 live native 466×466
and scaled 454×454 renders preserved the intended hierarchy and reduced ambient
mode to time alone; the 2026-08-20 checkpoint additionally proved the selected
clean-chamfer time. The 2026-08-21 emulator capture proves that checkpoint's
complete 466×466 composition with simulated available weather and confirms
time-only Dozing. The 2026-08-26 checkpoint proves packaged runtime `4a90116`
physically in interactive mode; sustained physical AOD and wearer judgment
remain open.



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
- `[weather]` is a uniform 16×16 storage tile with a 15×15 indexed-color
  condition sprite centered on cell `(7,7)`, not a literal
  label. It uses at most four flat palette entries; the adjacent temperature
  remains white. Steps and battery use monochrome 16×16 storage tiles; the
  selected runtime may tint only the battery icon by state.
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



## Implementation slices

The implementation has reached these slices; the evidence qualifier on each
slice matters. The earlier 2026-08-18 and 2026-08-20 checkpoints predated the
icon-family promotion; the 2026-08-21 emulator checkpoint closed that gap for
the final steps tile and clean-chamfer time. The 2026-08-26 physical checkpoint
adds exact-tree interactive proof after the static weather refresh.

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
   text-only date, deterministic preview parity, and historical live 466×466 /
   454×454 interactive and ambient validation. The 2026-08-21 emulator capture
   adds native WFF proof for the final steps tile and clean-chamfer time with
   simulated available weather; the 2026-08-26 physical capture proves the
   refreshed packaged tree interactively with live available night weather.
9. Canonical project-owned square and clean-chamfer primary cuts, with the
   reviewed clean chamfer selected and freshly renderer-validated in native
   466×466 interactive and confirmed Dozing states.
10. Canonical eight-phase weather motion for all 16 recognized day/night-
    resolved families, generated into the WFF v2 resource surface and played
    once on visibility for fresh data. Schema, deterministic-source, resource,
    and memory gates are complete; emulator and physical-device capture remain
    open.

Later slices remain separately gated:

11. Live-test stale weather after proving fresh available and truthful,
   header-free unavailable states.
12. Complete physical-watch wearer, sustained-AOD, and battery validation and
    adjustment.
13. Clean-chamfer and icon-family optical polish driven by physical wear.
14. One rare color event.
15. Optional complication/configuration work only after the identity is stable.

## Open decisions

- Wearer confirmation of the exact current solid 3×3 cells, AMOLED appearance,
  and wrist-distance legibility. Native physical-device rendering is now proven
  for the current packaged tree, but an ADB screenshot cannot close those
  perceived-quality gates.
- Whether weather/date spacing needs an explicit optical adjustment after the
  calendar icon is removed.
- Physical-watch adjustment of the single-grid bands, optical time position,
  safe radius, solid cells, and indexed weather palette.
- Whether physical wear calls for a further clean-chamfer optical adjustment;
  the selected cut is already directly authored and emulator-proven.
- Optical refinement of the selected 15×15 drawable icon family.
- Live verification of stale, day-family, explicit-Fahrenheit-selection, and
  extreme-value weather branches. Fresh available night-family weather is
  proven on the exact 2026-08-26 physical tree; the provider's Fahrenheit
  surface remains proven on the earlier physical deployment.
  The emulator editor proves the Celsius
  default and both choices are reachable; resource tests cover both conversion
  directions, and the physical watch proves a live converted `17°C` default.
  Physical Fahrenheit selection is not required for the Celsius-default gate.
- The physical WFF provider returned `63°F` under the watch's `en-US` locale
  while the separate OnePlus Weather tile displayed `20°` under its own
  Celsius preference/setting; the capture did not literally show `20°C`. These
  are separate provider/cache surfaces; the Raster 90 setting converts and
  labels its own WFF value but does not synchronize those readings.
- Emulator and physical-watch validation of the promoted on-visible weather
  animation, including trigger behavior, frame cadence, and return to rest.

## Starting typography comparison

The historical calibration specimen compared:

- `PixelOperatorMonoHB` for the primary time because its fixed advances prevent
  the clock from shifting as digits change and its intermediate weight remains
  open at small sizes;
- `PixelOperatorMono` for compact values and labels; and
- `PixelOperatorMono8` and `PixelOperatorMonoHB8` as coarse-display alternatives
  for the oversized time.

## Icon resolution and steps evolution

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
After review of the earlier walking-figure study, a focused native-size study
selected direct-authored paired footprints. Their separated toe pads and
vertically offset, tapered soles remain recognizable beside the count at the
native 3×3-cell scale. The final `four-toe-vertical` asset was promoted after
the earlier clean-chamfer emulator capture. The 2026-08-21 emulator checkpoint
and 2026-08-26 physical checkpoint prove it in the packaged WFF; physical
wearer review remains pending.

## Retained alternatives

The implemented V1 8×8 weather sprites and the subsequent 8×8/12×12 studies are
retained as evidence: they showed that the smaller grid could not express
weather and figures consistently, while a physically larger weather-only tile
made the composition top-heavy. They are not the selected post-V1 system.

### Alternatives reviewed

- Pix32 remains interesting research for a future Chinese/Japanese locale mode,
  but it is not a baseline dependency. Its broad glyph set is unnecessary for
  the first face, and its license at the time of review did not grant the modification and
  redistribution freedom needed for subsetting or generated bitmap assets.
- The Minecraft font is not part of the direction. Its highly recognizable game
  identity would turn the design into a themed watch face rather than the
  imagined constrained computer-watch.

The licensing judgment above is historical, not a current upstream audit.
Recheck the [upstream terms](https://github.com/32comic/Pix32/blob/main/LICENSE.md)
if direct reuse is ever proposed.
