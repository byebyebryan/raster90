# Wear OS validation history — 2026-08-15 through 2026-08-19

These are dated records of earlier trees, retained from the original device
log. References to current or remaining work describe the state at each
checkpoint; use [the validation index](../validation.md) for current status.
Commands, measurements, failures, and evidence qualifiers are historical.

## Raster 90 temperature-unit editor checkpoint — 2026-08-19

Implemented and freshly validated the Celsius-default temperature setting on
the primary Wear OS 5 emulator:

- The resource-only WFF v2 bundle declares one editable `ListConfiguration`
  with exactly two choices: Celsius by default and an explicit Fahrenheit
  override. Focused resource contracts cover pass-through and rounded
  conversion in both provider-unit directions without changing weather
  availability, stale-state, fallback, geometry, or ambient behavior.
- All deterministic asset/study checks, 30 Python tests, XML parsing,
  debug/release builds, lint, WFF validator 1.7.0, and the official 10 MB
  ambient / 100 MB active memory-limit evaluation passed on the reviewed tree.
- `wear5-opw3` was identity-proven as Android 14 / API 34, circular 466×466 at
  320 dpi with the watch and WFF runtime features before installation. The APK
  installed and selected through debug surface runtime version 2.
- The watch-face picker exposed its Edit action. The editor opened with
  `Temperature unit` set to `Celsius`, showed exactly the `Celsius` and
  `Fahrenheit` choices, and accepted a switch to `Fahrenheit`. The emulator was
  returned to Celsius before the editor was closed.
- A fresh face selection after clearing earlier boot/install noise produced no
  WFF runtime warnings or errors. The emulator had no usable weather data, so
  it truthfully rendered the neutral icon-plus-`--` fallback. The physical
  follow-up below subsequently closed the Celsius-output validation gate.
- Ignored review evidence is retained under
  `outputs/raster90/captures/temperature-unit-setting/`, including the native
  interactive capture and editor hierarchy dumps for the Celsius default,
  two-choice list, and Fahrenheit selection.

The emulator was stopped only after re-proving the `wear5-opw3` AVD name.

## Raster 90 physical Celsius checkpoint — 2026-08-19

After the watch re-advertised Wireless debugging, the temperature-unit build
was deployed and checked on the physical OnePlus Watch 3:

This physical record predates both `b7ffa65`'s clean-chamfer runtime and
`33e2912`'s final `four-toe-vertical` icon promotion. It proves live converted
Celsius weather on that earlier deployment, not the current exact packaged art.

- The selected ADB endpoint was independently identity-proven as `OPWWE251`,
  Android 14 / API 34, 466×466 at 320 dpi, with `armeabi-v7a,armeabi` and the
  watch/WFF runtime features before installation. No transient endpoint is
  recorded.
- The validated debug APK installed successfully, and the WFF debug surface
  selected `io.github.byebyebryan.raster90.watchface` using runtime version 2.
- The unobscured native capture rendered the live night-family weather icon
  with `17°C`. This is consistent with the setting's rounded conversion of the
  same provider surface that previously rendered `63°F`, and proves the
  Celsius-default output with real physical-watch weather data.
- After clearing earlier install noise, a fresh re-selection produced no WFF
  runtime warnings or errors. Raster 90 was left active in Celsius.
- The physical capture and window evidence are retained under
  `outputs/raster90/captures/temperature-unit-setting/`. Physical selection of
  the Fahrenheit override is unnecessary for the Celsius-default gate and was
  not performed; both editor choices remain emulator-proven.

## Raster 90 physical-watch interactive checkpoint — 2026-08-19

Deployed the committed solid-grid runtime to the paired OnePlus Watch 3 and
validated the physical WFF renderer without changing the watch's time, weather,
or always-on-display preferences:

This was the latest physical capture at that checkpoint, but it predates both
the clean-chamfer time cut and the final `four-toe-vertical` footprint tile.
Treat it as physical WFF, live-weather, and device-behavior evidence for the
earlier solid-grid tree only; the [2026-08-26 checkpoint](2026-08-26-weather-icons.md) supersedes it for
current exact-tree interactive rendering.

- The sole ADB target was identity-proven before installation as `OPWWE251`,
  Android 14 / API 34, 466×466 at 320 dpi, with `armeabi-v7a,armeabi` and the
  watch/WFF runtime features.
- Fresh asset verification, WFF validator 1.7.0, debug/release builds, lint, and
  the official memory-footprint limit check passed before deployment.
- The APK installed successfully and the WFF debug surface selected
  `io.github.byebyebryan.raster90.watchface` using runtime version 2.
- The native interactive capture showed a live clear-night-family icon and
  `63°F`, centered `WED 19 AUG`, live 12-hour time, `00000` steps, and `76%`
  battery. The 3×3 cells, 16×16 icon tiles, colon separation, row centering, and
  circular edge clearance all rendered without clipping.
- The fresh physical runtime log contained no weather, WFF parse, resource,
  expression, exception, or fatal error. No stale marker was visible, so this
  proves an available/fresh night-weather state in addition to the emulator-
  proven unavailable fallback. A real stale state remains untested.
- Official WFF documentation defines temperature-unit value `1` as Celsius and
  `2` as Fahrenheit. Raster 90 correctly rendered the WFF provider's Fahrenheit
  value under the watch's `en-US` locale. The separate OnePlus Weather tile
  displayed `20°` under its own Celsius preference/setting; the capture did not
  literally show `20°C`. These are separate provider/cache surfaces, not
  synchronized readings. The current product decision is Celsius by default
  with an explicit Fahrenheit override in the editable WFF v2 setting;
  resource tests cover rounded conversion in both directions, and the later
  physical Celsius checkpoint above proves the selected default with live data.
- The watch had sustained AOD disabled (`ambient_enabled=0`, `doze_enabled=0`).
  Interactive information disappeared during the sleep transition as designed,
  but the display then slept fully; no AOD preference was changed, so sustained
  physical ambient rendering remains unproven.
- Forcing sleep caused the watch's Wi-Fi debugging advertisement to disappear.
  This is recoverable by waking the watch physically and allowing the stored
  trusted mDNS connection to return; no transient endpoint is recorded here.
- Screenshots can prove native renderer output but not perceived AMOLED quality,
  bezel appearance, wrist-distance legibility, or battery drain. Those remain
  wearer-observation gates.

Ignored evidence is retained under
`outputs/raster90/captures/physical-watch/2026-08-19-solid-grid/`, including the
interactive screenshot, power/battery state, window dump, and clean runtime
log. The watch was left with Raster 90 selected; its Wi-Fi debugging transport
requires a physical wake before final reconnection verification.

## Raster 90 solid-grid runtime — 2026-08-18

Implemented and freshly validated the selected solid single-grid composition on
both Wear OS 5 targets:

- The packaged 450×450 active frame remains one 150×150 source framebuffer,
  now using solid 3×3 cells without gutters. Compact text, provisional expanded
  time, and every icon use that one physical cell scale.
- The exact generated surface contains 89 PNGs. Direct-authored true 16×16
  weather, walker, and battery matrices produce 48×48 tiles; the calendar asset
  is removed, and the generated preview shares source art and coordinates with
  the runtime.
- Available weather, steps, and battery use one vertically centered value
  without `WX`, `STP`, or `BAT`; `SAT 15 AUG` is centered as one text row without
  a calendar icon. The unavailable branch initially retained the neutral icon
  with `WX` over `--`; the follow-up header-free pass replaced it with the same
  icon plus `--` on one vertically centered line.
- All four deterministic asset/study checks, 28 unit tests, XML parsing,
  debug/release builds, lint, and WFF validator 1.7.0 passed. Regression tests
  cover solid-cell fill, the exact asset surface, direct true 16×16 condition
  coverage, preview/WFF row parity, centered date geometry, data bindings, and
  ambient isolation.
- The official memory-footprint evaluator passed the 10 MB ambient / 100 MB
  active limits. Its conservative report measured 687,024 maximum active bytes
  and 155,520 maximum ambient bytes; `--estimate-optimization` measured 493,732
  and 104,004 bytes respectively.
- `wear5-opw3` was identity-proven as Android 14 / API 34, circular 466×466 at
  320 dpi with the watch and WFF runtime features. Its unobscured interactive
  capture showed the truthful unavailable-weather branch, centered one-line
  date, `00000` steps, and `100%` battery with solid cells and no clipping. A
  fresh follow-up deploy proved the header-free neutral icon plus `--` on one
  vertically centered line. Device-synchronized 12-hour time and forced
  24-hour time both fit; the automatic setting was restored. Confirmed Dozing
  reduced the face to dimmed monochrome time only.
- `wear5` was independently identity-proven as Android 14 / API 34, circular
  454×454 at 320 dpi with the same runtime features. Interactive and confirmed
  Dozing ambient captures remained centered and unclipped after WFF scaling. A
  fresh follow-up deploy proved the same header-free fallback remained centered
  and legible at 454×454.
- Runtime logs contained no WFF parse, resource, expression, or fatal failure.
  Both emulators emitted a startup complication-cache `ClassCastException`
  warning and weather-provider error code 5; neither had usable weather data,
  so both selected the neutral icon-plus-`--` fallback. Each AVD name was
  re-proven before shutdown; no physical device was connected or modified.

Local review artifacts are retained under the Git-ignored
`outputs/raster90/captures/solid-grid-runtime/` directory:

- `raster90-solid-grid-wear5-opw3-interactive-466.png`
- `raster90-solid-grid-wear5-opw3-ambient-466.png`
- `raster90-solid-grid-wear5-opw3-24h-466.png`
- `raster90-solid-grid-wear5-interactive-454.png`
- `raster90-solid-grid-wear5-ambient-454.png`
- matching `*-window.xml`, `*-ambient-power.txt`, and `*-logcat.txt` evidence

The header-free follow-up captures and matching window/log evidence are under
`outputs/raster90/captures/header-free-weather/`.

This historical checkpoint supersedes the icon-weight and 3/2 single-grid
runtime records below for its then-current packaged geometry, resource count,
memory, and emulator appearance. Later clean-chamfer and icon-family commits
supersede its current-art claims. Physical-watch rendering of the exact current
tree, live available/stale weather on that tree, and final wearer judgment
remain open.

## Raster 90 icon stroke-weight correction — 2026-08-18

Corrected and freshly validated the single-grid icon rasterization on both Wear
OS 5 targets:

- The defect was in the source pipeline, not WFF scaling: fractional
  nearest-neighbour expansion mapped the compact battery's top edge to three
  source rows and its bottom edge to two. The unavailable-weather outline and
  other sprites were vulnerable to the same unequal replication.
- Calendar, steps, and battery are now explicit project-owned 16×16 matrices.
  The battery uses equal two-cell top/bottom and left/right structural strokes;
  its terminal is an intentional two-cell extension.
- Weather candidates now use integer-only cell replication and optical padding.
  No source row or column can acquire a different target weight through
  normalization.
- Asset/study checks and 15 unit tests passed, including regression assertions
  for battery/calendar opposing edges and the unavailable-weather border. The
  exact generated surface remains 90 PNGs.
- Debug/release builds, lint, XML checks, WFF validator 1.7.0, and the official
  memory limits passed. The conservative evaluator report measured 696,240
  maximum active bytes and 155,520 maximum ambient bytes. Its optional
  `--estimate-optimization` report measured 464,220 and 101,002 bytes
  respectively; both are retained as distinct measurements.
- `wear5-opw3` was identity-proven as API 34, circular 466×466 at 320 dpi. Its
  unobscured WFF capture shows equal battery and unavailable-weather opposing
  edges, with the calendar outline following the same rule.
- `wear5` was independently identity-proven as API 34, circular 454×454 at 320
  dpi. The same strokes remained visually balanced and unclipped after WFF
  scaling.
- Runtime logs contained no WFF parse, resource, expression, or fatal failure.
  Both emulators lacked usable weather and reported provider error code 5,
  correctly selecting `WX --`. Both AVD names were re-proven before shutdown;
  no physical device was connected or modified.

Local review artifacts are retained under the Git-ignored
`outputs/raster90/captures/icon-weight/` directory:

- `raster90-icon-weight-wear5-opw3-interactive-466.png`
- `raster90-icon-weight-wear5-interactive-454.png`
- matching `raster90-icon-weight-*-logcat.txt` files

This checkpoint supersedes the single-grid runtime record below for icon
rasterization, test count, memory, and current interactive appearance. Icon
silhouettes and optical scale remain open design work; this correction only
makes their structural cell weight deterministic and symmetric.

## Raster 90 single-grid runtime candidate — 2026-08-18

Freshly validated the packaged 150×150 single-grid candidate on both Wear OS 5
targets:

- `tools/generate_raster90_assets.py --check` verified the exact deterministic
  surface of 90 PNGs. The asset set uses one 3-unit pitch / 2×2 lit-square grid,
  18×21 compact glyph advances, uniform 48×48 icon and weather tiles, 78×96
  time digits, and a 30×96 colon.
- The asset, icon-study, and single-grid-study checks passed together with 13
  unit tests. The tests assert exact resource dimensions and palette bounds,
  reject stale/corrupt resources, and parse the generated WFF geometry and its
  single ambient variant.
- `xmllint` passed and WFF validator 1.7.0 accepted `watchface.xml` as format
  version 2.
- `assembleDebug`, `assembleRelease`, and `lintDebug` passed under Android
  Studio JBR 25. Lint reported zero errors and 16 existing non-fatal warnings.
- The official memory-footprint evaluator passed the 10 MB ambient / 100 MB
  active limits. Its optimization-estimate report measured 428,176 maximum
  active bytes and 101,002 maximum ambient bytes.
- The primary runtime was identity-proven as `wear5-opw3`, Android 14 / API 34,
  model `sdk_gwear_x86_64`, circular 466×466 at 320 dpi, with the watch and WFF
  runtime features. After simulated AC power was disabled and the charging
  overlay dismissed, the debug surface selected Raster 90 and the unobscured
  WFF window rendered the complete single-grid composition.
- The native interactive capture showed the truthful `WX --` fallback, live
  weekday/date and time, `STP 00000`, and `BAT 100%`. All five row bands were
  centered and unclipped, the colon remained separated from the minute digits,
  and the uniform weather/calendar/walker/battery tile geometry was visible.
- Confirmed Dozing state reduced the 466×466 face to monochrome time only.
  Device-synchronized 12-hour rendering showed `06:xx`; forcing the emulator to
  24-hour mode showed `18:xx` without shifting or clipping, after which the
  original automatic setting was restored.
- The secondary runtime was independently identity-proven as `wear5`, Android
  14 / API 34, model `sdk_gwear_x86_64`, circular 454×454 at 320 dpi, with the
  same watch and WFF runtime features. Interactive and ambient captures remained
  centered and unclipped after WFF scaling.
- Runtime logs contained no WFF parse, resource, expression, or fatal failure.
  The 466 and 454 emulators reported weather-provider error codes 5 and 4
  respectively because neither had usable weather data; both correctly selected
  `WX --`.
- Both emulators were stopped only after re-proving their AVD names. No physical
  device was connected or modified.

Local review artifacts are retained under the Git-ignored
`outputs/raster90/captures/single-grid-runtime/` directory:

- `raster90-single-grid-runtime-wear5-opw3-interactive-466.png`
- `raster90-single-grid-runtime-wear5-opw3-ambient-466.png`
- `raster90-single-grid-runtime-wear5-opw3-24h-466.png`
- `raster90-single-grid-runtime-wear5-interactive-454.png`
- `raster90-single-grid-runtime-wear5-ambient-454.png`
- matching `*-window.xml` and `*-logcat.txt` evidence

The official validator and memory evaluator used for this check are retained
with their licenses under the ignored `outputs/tooling/google-watchface/`
namespace. This checkpoint supersedes the typography and V1 records below for
current packaged geometry, resource count, memory, and emulator appearance. The
expanded time numerals and icon artwork remain provisional; live
available/stale weather and the physical OnePlus Watch 3 remain separate gates.

## Raster 90 typography refinement — 2026-08-18

Freshly validated the consistent-separator and coarse-colon refinement on both
Wear OS 5 targets:

- Ordinary fine glyphs retain 30-unit advances while the literal space is now
  one shared 10-unit separator. Runtime and generated preview use it for
  `WX --`, `MON 17 AUG`, `STP 00000`, `STP 123456`, and `BAT 100%`; their exact
  row widths are 130, 260, 250, 280, and 220 units respectively.
- The 30-unit colon keeps the complete time at 350 units but now renders each
  dot as a 2×2 coarse-cell block. The preceding digit's trailing blank supplies
  leading separation and the colon's trailing blank supplies following
  separation, so its weight matches the digits without touching the minutes.
- Deterministic regeneration changed only the preview, colon, and space images;
  `--check` verified the complete 87-PNG surface. `xmllint` passed, and WFF
  validator 1.7.0 accepted the face as format version 2.
- A full rerun of `assembleDebug`, `assembleRelease`, and `lintDebug` passed
  under JBR 25. Lint retained zero errors and the same 16 non-fatal warnings:
  three documented version notices and 13 intentional duplicate bitmap aliases.
- The official memory-footprint evaluator passed and reported 677,600 maximum
  active bytes and 149,400 maximum ambient bytes.
- `wear5-opw3` was identity-proven as Android 14 / API 34, circular 466×466 at
  320 dpi. Its interactive render kept all compact rows centered and unclipped;
  the colon had digit-consistent weight and balanced separation. Confirmed
  Dozing state reduced the face to corrected coarse time only.
- `wear5` was independently identity-proven as Android 14 / API 34, circular
  454×454 at 320 dpi. Interactive and ambient renders preserved the same
  hierarchy, spacing, colon separation, centering, and edge clearance after WFF
  scaling.
- Runtime logs contained no WFF parse, resource, expression, or fatal failure.
  Both emulators reported weather-provider error code 4 because no usable
  weather source was available; the face truthfully selected `WX --`.
- Both emulators were stopped only after re-proving their AVD names. No physical
  device was connected or modified.

Local review artifacts are retained under the Git-ignored
`outputs/raster90/captures/typography/` directory:

- `raster90-typography-wear5-opw3-interactive-466.png`
- `raster90-typography-wear5-opw3-ambient-466.png`
- `raster90-typography-wear5-interactive-454.png`
- `raster90-typography-wear5-ambient-454.png`
- matching `raster90-typography-*-logcat.txt` files

This checkpoint supersedes the V1 record below for current spacing, colon
weight, memory, and emulator appearance. Live available/stale weather and the
physical OnePlus Watch 3 remain separate open gates.

## Raster 90 V1 — 2026-08-17

Freshly validated the functional resource-only V1 on both Wear OS 5 targets:

- `tools/generate_raster90_assets.py --check` verified the exact deterministic
  surface of 87 PNGs. The generated picker preview shows partly-cloudy daylight,
  `21°C`, `SAT 15 AUG`, `10:08`, `STP 03642`, and `BAT 82%` from the same source
  matrices as the runtime bitmap fonts and weather sprites.
- `xmllint` passed and WFF validator 1.7.0 accepted `watchface.xml` as format
  version 2.
- A clean `assembleDebug`, `assembleRelease`, and `lintDebug` passed under JBR
  25. Lint reported zero errors and 16 non-fatal warnings: three documented
  tool/SDK version-availability notices and 13 intentional duplicate glyph or
  weather aliases in the generated asset set.
- The official memory-footprint evaluator passed the 10 MB ambient / 100 MB
  active gates. Its report measured 512,972 maximum active bytes and 120,608
  maximum ambient bytes.
- The primary runtime was identity-proven as `wear5-opw3`, Android 14 / API 34,
  circular 466×466 at 320 dpi with the watch and WFF runtime features. The APK
  installed and the Wear debug surface selected it successfully.
- The 466×466 interactive capture showed live date/time, `STP 00000`,
  `BAT 100%`, and the truthful `WX --` fallback with crisp square cells and no
  clipping. A post-review spacing pass centered the time vertically, normalized
  every adjacent row-box gap to 20 active-frame units, and widened the colon to
  a centered three-cell separator so it does not fuse with minute digits. The
  ambient capture showed only the corrected coarse time on black.
- The secondary runtime was independently identity-proven as `wear5`, Android
  14 / API 34, circular 454×454 at 320 dpi with the same features. Its
  interactive and ambient captures remained crisp, centered, and unclipped
  after WFF scaling; the colon and row rhythm remained visibly distinct.
- Runtime logs contained no WFF parse, resource, expression, or fatal runtime
  failure. Both emulators reported weather-provider error code 6 because they
  had no usable weather source; that correctly selected `WX --`.
- Both emulators were stopped only after re-proving their AVD names. No physical
  device was connected or modified.

Local review artifacts are retained under the Git-ignored
`outputs/raster90/captures/v1/` directory:

- `raster90-v1-wear5-opw3-interactive-466.png`
- `raster90-v1-wear5-opw3-ambient-466.png`
- `raster90-v1-wear5-interactive-454.png`
- `raster90-v1-wear5-ambient-454.png`
- matching `raster90-v1-*-logcat.txt` files

This proves V1's live time/date/step/battery bindings, unavailable-weather
branch, time-only ambient mode, and both emulator geometries. The generated
preview plus validator prove the available-state resource composition, but live
available/stale weather, Celsius/Fahrenheit switching, and all condition sprites
still require a target with real location/weather data. The physical OnePlus
Watch 3 remains authoritative for the final display and power judgment.

## Raster 90 calibration scaffold — 2026-08-17

Freshly validated `:watchfaces:raster90` on the primary `wear5-opw3` target:

- Live target identity: AVD `wear5-opw3`, Android 14 / API 34,
  `sdk_gwear_x86_64`, circular display, 466×466 at 320 dpi, with
  `com.google.clockwork.watchface.runtime` present.
- Application ID `io.github.byebyebryan.raster90.watchface`; resource-only WFF
  v2 APK with `minSdk=34`, `targetSdk=35`, and `compileSdk=35`.
- `assembleDebug`, `assembleRelease`, and `lintDebug` passed. Lint reported zero
  errors and three intentional version-availability warnings for the documented
  Gradle, AGP, and compile-SDK compatibility pins.
- Watch Face Format validator 1.7.0 accepted `watchface.xml` as valid WFF v2.
- The official memory-footprint evaluator reported 72,984 maximum active bytes
  and 19,020 maximum ambient bytes.
- The APK installed and the Wear debug surface selected it successfully. A
  native 466×466 capture showed crisp fine/coarse cell edges, live Pixel
  Operator time, four font specimens, and the indexed palette. Doze mode hid
  all diagnostics and retained only the monochrome time.
- The system charging indicator occupied bottom-center bounds
  `[215,422][251,464]`; final layouts must reserve or deliberately tolerate
  that overlay region.
- Runtime inspection found no WFF parsing, resource, or expression failures.
  Package-replacement and emulator graphics warnings occurred during repeated
  debug reinstalls but did not prevent rendering.

This section records the historical calibration gate that preceded V1. The
functional V1 record above supersedes it for current emulator rendering; only
physical OnePlus Watch 3 validation remains open.

## Official sample baseline — 2026-08-15

Validated 2026-08-15 using the official Android `wear-os-samples` `Flavors`
watch face, which exercises WFF v2 and requires API 34:

- Temporary validation copy pinned to the project's planned `compileSdk=35`
  and `targetSdk=35`.
- Gradle 9.2.1, Android Gradle Plugin 9.0.0, and Android Studio JBR 25.
- `assembleDebug` and `lintDebug` passed (38 tasks).
- The resource-only APK declared `minSdk=34`, installed successfully on the
  historical validation target `emulator-5554`, and activated through the Wear
  debug surface. Resolve the current Wear AVD serial before any new deployment.
- The face rendered correctly at 454×454. Unset heart-rate and complication
  fields were expected because the emulator has no physical data sources.
- Runtime logs contained no WFF parsing, resource, or expression errors.
