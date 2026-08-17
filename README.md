# Wear OS

Android monorepo for the OnePlus Watch 3 watch-face project and any directly
related Wear OS or phone components.

The first deliverable is a standalone, resource-only Watch Face Format v2
watch face for Wear OS 5. The repository does not currently contain an Android
project; environment and device validation were completed before scaffolding.

## Current targets

- OnePlus Watch 3: Wear OS 5 / Android 14 / API 34
- `wear5-opw3` emulator: primary 466×466 Wear OS 5 / Android 14 / API 34
- `wear5` emulator: secondary official 454×454 scaling reference
- OnePlus 13 and `phone16`: optional future companion targets, not required for
  watch-face development

## Repository boundaries

This is one Git repository with separate Android application modules. Each
application module must produce its own APK/AAB and use its own application ID.
The planned `watchface` module must remain resource-only and cannot contain or
depend on Kotlin/Java application logic.

Only modules with a concrete requirement will be created. See
[Repository Layout](docs/repository-layout.md) for the planned structure and
[Device Setup](docs/device-setup.md) for verified local targets. The
pre-implementation visual and fictional-hardware contract is captured in
[Watch Face Design Direction](docs/watchface-design.md).
Generated mood and hierarchy studies are catalogued separately under
[Concept Artwork](design/concepts/README.md); they are not production WFF
resources or geometry references.

Operational instructions for coding agents are in [AGENTS.md](AGENTS.md).
