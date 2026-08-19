# Repository Layout

## Decision

Use a product-focused Android monorepo rooted at `/home/bryan/code/wear-os`.
Separate APK/AAB packaging requirements are module boundaries, not Git
repository boundaries.

The first product and display name are Raster 90. Its resource-only V1 module is
`:watchfaces:raster90`, using application ID
`io.github.byebyebryan.raster90.watchface`. The active design contract remains
in `docs/watchface-design.md`.

## Current and reserved structure

```text
wear-os/
├── AGENTS.md
├── README.md
├── docs/
├── gradle/
├── settings.gradle.kts
├── build.gradle.kts
├── watchfaces/
│   └── raster90/       # First module: standalone resource-only WFF bundle
├── wear-apps/          # Future; create only for required Wear application logic
├── mobile-apps/        # Future; create only for a required phone companion
├── tools/              # Deterministic asset generation; future validation helpers
├── design/
│   ├── raster90/       # Reviewable glyph, icon, and palette matrices
│   └── concepts/       # Exploratory artwork; not production resources
└── third_party/        # Retained source material, licenses, and provenance
```

Only `watchfaces/raster90` belongs in the initial Android scaffold. The other
directories are reserved architecture, not empty modules to create
preemptively.

## Module boundaries

### `watchfaces/raster90`

- Android application module producing its own APK/AAB.
- Application ID `io.github.byebyebryan.raster90.watchface`.
- Watch Face Format v2, `minSdk=34`, `compileSdk=35`, `targetSdk=35`.
- Resource-only with `android:hasCode="false"` and Kotlin disabled.
- Must not contain application services or depend on future code modules.
- Generated bitmap-font glyphs, weather sprites, and the picker preview live in
  `res/drawable-nodpi`; their source matrices do not live inside the module.

### `wear-apps/<name>` (future)

- Separate application ID and APK/AAB.
- Owns any Wear OS application logic or complication data providers that WFF
  cannot provide declaratively.
- Must not be packaged into the watch-face bundle.

### `mobile-apps/<name>` (future)

- Separate application ID and APK/AAB targeting the phone platform.
- Exists only if a concrete companion-phone workflow is required.
- The watch-face bootstrap and deployment flow must not depend on it.

## Shared build policy

Use one Gradle root and version catalog so module-specific SDK targets can
differ without duplicating wrappers or repository configuration. Each Android
application module remains independently buildable and publishable.

The first scaffold pins Gradle 9.2.1 and Android Gradle Plugin 9.0.0, uses
Android Studio JBR 25, and includes only the `:watchfaces:raster90` Android
module.

## Current V1 asset boundary

- `design/raster90/matrices.py` is the human-reviewable source of truth.
- `tools/generate_raster90_assets.py` is the sole deterministic producer and
  checker for the 87 packaged/preview PNGs.
- `third_party/pixel-operator/` retains the four approved CC0 source fonts and
  license as design provenance; no TTF is packaged in V1.
- `outputs/` is Git-ignored and namespaced by product and purpose:
  `outputs/raster90/studies/<study>/` holds generated design studies,
  `outputs/raster90/captures/<checkpoint>/` holds emulator or physical-device
  evidence, and `outputs/references/` holds external visual references. Do not
  place new artifacts directly in the root.

Physical-watch adjustment and post-V1 motion/color decisions remain tracked in
`docs/watchface-design.md`; they do not change the monorepo boundary.
