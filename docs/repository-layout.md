# Repository Layout

## Decision

Use a product-focused Android monorepo rooted at `/home/bryan/code/wear-os`.
Separate APK/AAB packaging requirements are module boundaries, not Git
repository boundaries.

The initial repository contains documentation only. Bootstrap the first module
only after the design direction is reviewed and the application ID and display
name are settled. The active pre-implementation contract is in
`docs/watchface-design.md`.

## Planned structure

```text
wear-os/
├── AGENTS.md
├── README.md
├── docs/
├── gradle/
├── settings.gradle.kts
├── build.gradle.kts
├── watchface/          # First module: standalone resource-only WFF bundle
├── wear-app/           # Future; create only for required Wear application logic
├── mobile-app/         # Future; create only for a required phone companion
├── tools/              # Future; repository-owned validation/deployment helpers
└── design/             # Exploratory artwork; later, deterministic source assets
```

Only `watchface` belongs in the initial Android scaffold. The other directories
are reserved architecture, not empty modules to create preemptively.

## Module boundaries

### `watchface`

- Android application module producing its own APK/AAB.
- Watch Face Format v2, `minSdk=34`, `compileSdk=35`, `targetSdk=35`.
- Resource-only with `android:hasCode="false"` and Kotlin disabled.
- Must not contain application services or depend on future code modules.

### `wear-app` (future)

- Separate application ID and APK/AAB.
- Owns any Wear OS application logic or complication data providers that WFF
  cannot provide declaratively.
- Must not be packaged into the watch-face bundle.

### `mobile-app` (future)

- Separate application ID and APK/AAB targeting the phone platform.
- Exists only if a concrete companion-phone workflow is required.
- The watch-face bootstrap and deployment flow must not depend on it.

## Shared build policy

Use one Gradle root and version catalog so module-specific SDK targets can
differ without duplicating wrappers or repository configuration. Each Android
application module remains independently buildable and publishable.

The first scaffold is expected to pin Gradle 9.2.1 and Android Gradle Plugin
9.0.0, use Android Studio JBR 25, and create only the `:watchface` module.

## Decisions required before scaffolding

1. Permanent watch-face `applicationId`.
2. Project and user-visible watch-face name.
3. Approval of the indexed-color interactive, localized-event, and ambient
   mockup direction.
