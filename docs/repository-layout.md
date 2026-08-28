# Repository Layout

## Decision

Use the dedicated Raster 90 product repository rooted at
`/home/bryan/code/raster90`. Separate APK/AAB packaging requirements remain
module boundaries within this repository.

This repository may later contain Raster 90-specific Wear or phone companion
modules, but it is not an umbrella for unrelated Android products.

The product and display name are Raster 90. Its resource-only module is
`:watchfaces:raster90`, using application ID
`io.github.byebyebryan.raster90.watchface`. The active design contract remains
in `docs/watchface-design.md`.

## Current and reserved structure

```text
raster90/
├── AGENTS.md
├── README.md
├── docs/
│   └── media/          # Small tracked public subset of verified runtime captures
├── gradle/
├── settings.gradle.kts
├── build.gradle.kts
├── watchfaces/
│   └── raster90/       # Current module: standalone resource-only WFF bundle
├── wear-apps/          # Future; Raster 90-specific Wear application logic
├── mobile-apps/        # Future; Raster 90-specific phone companion
├── tools/              # Deterministic asset generation; future validation helpers
├── fonts/
│   └── raster90/       # Project-owned family source and tracked presentation
├── icons/
│   └── raster90/       # Project-owned icon source and tracked presentation
├── design/
│   ├── raster90/       # Historical icon/layout controls and design studies
│   └── concepts/       # Exploratory artwork; not production resources
└── third_party/        # Retained source material, licenses, and provenance
```

Only `watchfaces/raster90` is currently an Android module. The other
directories are reserved Raster 90 product architecture, not empty modules to
create preemptively.

## Module boundaries

### `watchfaces/raster90`

- Android application module producing its own APK/AAB.
- Application ID `io.github.byebyebryan.raster90.watchface`.
- Watch Face Format v2, `minSdk=34`, `compileSdk=35`, `targetSdk=35`.
- Resource-only with `android:hasCode="false"` and Kotlin disabled.
- Must not contain application services or depend on future code modules.
- Generated bitmap-font glyphs, weather sprites, and the picker preview live in
  `res/drawable-nodpi`; their source matrices do not live inside the module.

### `wear-apps/<name>` (future Raster 90 module)

- Separate application ID and APK/AAB.
- Owns Raster 90-specific Wear OS application logic or complication data
  providers that WFF cannot provide declaratively.
- Must not be packaged into the watch-face bundle.

### `mobile-apps/<name>` (future Raster 90 module)

- Separate application ID and APK/AAB targeting the phone platform.
- Exists only if a concrete Raster 90 companion-phone workflow is required.
- The watch-face bootstrap and deployment flow must not depend on it.

## Shared build policy

Use one Gradle root and version catalog so module-specific SDK targets can
differ without duplicating wrappers or repository configuration. Each Android
application module remains independently buildable and publishable.

The first scaffold pins Gradle 9.2.1 and Android Gradle Plugin 9.0.0, uses
Android Studio JBR 25, and includes only the `:watchfaces:raster90` Android
module.

## Current asset boundary

- `fonts/raster90/family.py` is the authoritative source for the complete
  project-owned secondary vocabulary and named primary square, reviewed
  clean-chamfer, and legacy fine-chamfer display variants. `PRIMARY_DIGITS`
  remains the stable alias for the selected clean-chamfer runtime cut.
  `design/raster90/matrices.py` keeps compatibility aliases for design studies
  alongside palette and legacy comparison sprites.
- `icons/raster90/family.py` is the authoritative source for the selected
  weather, steps, and battery art: stable 16×16 storage matrices with a 15×15
  drawable field centered on cell `(7,7)` and a mandatory trailing empty
  row/column; the ordered battery tint bands; complete day/night WFF condition
  maps; the exact palette; neutral
  unavailable icon, and stale marker. `design/raster90/icon_resolution_studies.py`
  retains calendar,
  resolution, and other historical controls while rebinding selected aliases
  for comparison renderers.
- `tools/generate_raster90_assets.py` is the sole deterministic producer and
  checker for the 87 packaged/preview PNGs; it consumes only the secondary
  runtime subset and the complete primary 0-9/colon surface.
- `tools/render_raster90_font_family.py` produces and checks the tracked,
  self-contained family overview and specimen sheets under
  `fonts/raster90/preview/`.
- `tools/render_raster90_icon_family.py` produces and checks the tracked,
  self-contained selected icon/weather/state/matrix and native/magnified face
  sheets under `icons/raster90/preview/`.
- `tools/render_raster90_icon_resolution_studies.py` produces ignored,
  deterministic comparison sheets and full-face mocks; it does not change the
  watch-face module.
- `third_party/pixel-operator/` retains the four approved CC0 source fonts and
  license as design provenance; no TTF is packaged.
- `docs/media/` contains only reviewed public presentation copies selected from
  completed device-evidence checkpoints. Its files must retain provenance in
  `docs/media/README.md`; the ignored evidence tree remains canonical.
- `outputs/` is Git-ignored and namespaced by product and purpose:
  `outputs/raster90/studies/<study>/` holds generated design studies,
  `outputs/raster90/captures/<checkpoint>/` holds emulator or physical-device
  evidence, `outputs/references/` holds external visual references, and
  `outputs/tooling/<tool>/` holds locally downloaded validators and their
  licenses. Do not place new artifacts directly in the root.

Physical-watch adjustment and post-V1 motion/color decisions remain tracked in
`docs/watchface-design.md`; they do not change the Raster 90 repository
boundary.
