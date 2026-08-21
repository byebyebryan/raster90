# Raster 90

Dedicated Android product repository for the **Raster 90** watch face for the
OnePlus Watch 3.

Raster 90 is a standalone, resource-only Watch Face Format v2 watch face for
Wear OS 5. Its packaged runtime uses one fictional 150×150 framebuffer with
solid 3×3 source pixels, true 16×16 icons, and one icon-led value per
information row. Weather, steps, and battery keep icons;
`SAT 15 AUG` is centered without a calendar icon, and the redundant `WX`,
`STP`, and `BAT` headers are removed. Ambient mode remains time-only.

The solid-grid runtime is live-validated at native 466×466 on the physical
OnePlus Watch 3 and at native 466×466 / scaled 454×454 on Wear OS emulators.
Exact glyph and sprite resources are generated deterministically from
reviewable cell matrices rather than rendered from a runtime TTF. Its primary
time uses the reviewed project-owned clean-chamfer cut; the square construction
and legacy fine-chamfer remain named source controls, while the complete
secondary family remains source-only outside the current runtime subset.
The selected cut is freshly renderer-validated in interactive and confirmed
Dozing states on the native 466×466 `wear5-opw3` target. No physical deployment
of this selected cut is recorded yet; wearer-distance and AMOLED optical
judgment remain open.

The resting face is intentionally monochrome except for the small weather
sprite. Weather is Celsius by default with an explicit Fahrenheit override in
the watch-face editor; mismatched WFF provider units are converted before the
selected unit is shown. When weather is unavailable, the runtime keeps the row
and time fixed while showing a neutral weather icon plus `--` on one line. The
physical watch has also proven a live available night-weather row. Sustained
AOD, stale weather, wrist-distance, and battery validation remain separate
gates.

## Current targets

- OnePlus Watch 3: Wear OS 5 / Android 14 / API 34
- `wear5-opw3` emulator: primary 466×466 Wear OS 5 / Android 14 / API 34
- `wear5` emulator: secondary official 454×454 scaling reference
- OnePlus 13 and `phone16`: optional future companion targets, not required for
  watch-face development

## Repository boundaries

This repository contains the Raster 90 product and its Android components. The
current `:watchfaces:raster90` application module must produce its own APK/AAB
and use its own application ID. It uses
`io.github.byebyebryan.raster90.watchface`; it must remain resource-only and
cannot contain or depend on Kotlin/Java application logic.

Future application modules must likewise be independently packaged and may
provide Raster 90-specific Wear or phone companion functionality only. This
repository is not an umbrella for unrelated Android products.

Only modules with a concrete Raster 90 requirement will be created. See
[Repository Layout](docs/repository-layout.md) for the repository structure and
[Device Setup](docs/device-setup.md) for verified local targets. The
visual and fictional-hardware contract is captured in
[Watch Face Design Direction](docs/watchface-design.md).
Generated mood and hierarchy studies are catalogued separately under
[Concept Artwork](design/concepts/README.md); they are not production WFF
resources or geometry references.

The project-owned bitmap families are first-class repository components under
[`fonts/raster90/`](fonts/raster90/README.md) and
[`icons/raster90/`](icons/raster90/README.md). Their tracked
[font preview](fonts/raster90/preview/index.html) contains the complete font
matrix sheets and an interactive local specimen; the [icon
preview](icons/raster90/preview/index.html) contains selected utility/weather
matrices, truthful weather-state treatment, and native/magnified face views.
The runtime icon generator imports selected surfaces directly from
`icons/raster90/family.py`.

Operational instructions for coding agents are in [AGENTS.md](AGENTS.md).

## Build

Use Android Studio's bundled JBR with the committed Gradle wrapper:

```sh
JAVA_HOME=/opt/android-studio/jbr rtk proxy ./gradlew \
  :watchfaces:raster90:assembleDebug \
  :watchfaces:raster90:lintDebug
```

The debug APK is written to
`watchfaces/raster90/build/outputs/apk/debug/raster90-debug.apk`. See
[Device Setup](docs/device-setup.md) for explicit-target emulator deployment
and the current validation record. Disposable screenshots, reports, and design
studies belong in the Git-ignored root `outputs/` directory. Keep them
namespaced: Raster 90 generators use
`outputs/raster90/studies/<study>/`, device evidence uses
`outputs/raster90/captures/<checkpoint>/`, and external visual references use
`outputs/references/`. Locally downloaded validation binaries and their licenses
use `outputs/tooling/<tool>/`.

Regenerate or verify the bitmap resources with:

```sh
rtk python3 -B tools/generate_raster90_assets.py
rtk python3 -B tools/generate_raster90_assets.py --check

# Generate/check the complete tracked font-family presentation.
rtk python3 -B tools/render_raster90_font_family.py
rtk python3 -B tools/render_raster90_font_family.py --check

# Generate/check the complete tracked icon-family presentation.
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
```
The presentations write complete font/icon sheets, native-scale specimens, and
self-contained local `preview/index.html` files.
