# Wear OS

Android monorepo for watch faces, Wear OS applications, and directly related
Android components. The first product is the **Raster 90** watch face for the
OnePlus Watch 3.

Raster 90 is a standalone, resource-only Watch Face Format v2 watch face for
Wear OS 5. V1 is a functional two-tier bitmap face with live time, date,
weather, steps, and battery; ambient mode reduces it to time only. Its exact
glyph and sprite resources are generated deterministically from reviewable
cell matrices rather than rendered from a runtime TTF.

The post-V1 design study is evaluating a single fictional 150×150 framebuffer:
one 3-unit source-pixel pitch with 2×2 lit squares, uniform 16×16 icon tiles,
8-pixel compact-text lines, and a 32-pixel high-resolution time line. This is
not packaged runtime geometry until native, scaled, and physical-watch
calibration approves it.

The resting face is intentionally monochrome except for the small weather
sprite. When emulator weather is unavailable it reports `WX --` without moving
the time. The generated preview records the available-state composition with
representative values; physical-device weather and wrist-distance validation
remain separate gates.

## Current targets

- OnePlus Watch 3: Wear OS 5 / Android 14 / API 34
- `wear5-opw3` emulator: primary 466×466 Wear OS 5 / Android 14 / API 34
- `wear5` emulator: secondary official 454×454 scaling reference
- OnePlus 13 and `phone16`: optional future companion targets, not required for
  watch-face development

## Repository boundaries

This is one Git repository with separate Android application modules. Each
application module must produce its own APK/AAB and use its own application ID.
The existing `:watchfaces:raster90` module uses
`io.github.byebyebryan.raster90.watchface`; it must remain resource-only and
cannot contain or depend on Kotlin/Java application logic.

Only modules with a concrete requirement will be created. See
[Repository Layout](docs/repository-layout.md) for the repository structure and
[Device Setup](docs/device-setup.md) for verified local targets. The
  visual and fictional-hardware contract is captured in
[Watch Face Design Direction](docs/watchface-design.md).
Generated mood and hierarchy studies are catalogued separately under
[Concept Artwork](design/concepts/README.md); they are not production WFF
resources or geometry references.

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
and the current validation record. Local screenshots, reports, and other
reviewable generated artifacts belong in the Git-ignored root `outputs/`
directory. Keep them namespaced: Raster 90 generators use
`outputs/raster90/studies/<study>/`, device evidence uses
`outputs/raster90/captures/<checkpoint>/`, and external visual references use
`outputs/references/`.

Regenerate or verify the bitmap resources with:

```sh
rtk python3 -B tools/generate_raster90_assets.py
rtk python3 -B tools/generate_raster90_assets.py --check
```
