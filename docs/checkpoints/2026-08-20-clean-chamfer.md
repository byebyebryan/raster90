# Raster 90 clean-chamfer emulator checkpoint — 2026-08-20

Promoted the reviewed primary numeral cut into the packaged runtime and
freshly validated it on the native-size Wear OS 5 target:

This checkpoint was captured after `b7ffa65` and before `33e2912`. The later
commit promoted the canonical icon family, changed the packaged steps PNG, and
updated tracked previews. Consequently, this is not a capture of the current
exact tree: it remains authoritative for the clean-chamfer time and the
pre-promotion runtime behavior only.

- Commit `b7ffa65` keeps square and clean-chamfer digits as first-class
  canonical matrices, retains the earlier global fine-chamfer as a named
  source-only control, and selects clean chamfer through the stable runtime
  aliases. Preview and packaged time resources are generated from that same
  selected source.
- The selected tree passed 43 Python tests, all deterministic asset and font
  presentation checks, XML parsing, debug and release assembly, lint, WFF
  validator 1.7.0 against format version 2, and the official memory limits.
  The conservative evaluator reported 684,000 maximum active bytes and
  155,520 maximum ambient bytes; `--estimate-optimization` reported 492,220
  and 104,004 bytes respectively.
- The capture pass rebuilt the debug APK with Android Studio JBR 25 after fresh
  asset and font-presentation checks. The installed APK SHA-256 was
  `09597296e4a94f8096ce2ebe012508a9562216c94336e58ca902a0a0bd7fdacc`.
- `wear5-opw3` was cold-booted and identity-proven before installation as
  Android 14 / API 34, model `sdk_gwear_x86_64`, circular runtime `1`, physical
  size 466×466, density 320, with the watch and WFF runtime features.
- The APK installed and the debug surface selected
  `io.github.byebyebryan.raster90.watchface`. Window/display evidence identified
  `DeclarativeWatchFaceRuntime0` as the obscuring watch-face surface.
- The native interactive capture shows the clean-chamfer time, centered date,
  truthful neutral weather icon plus `--`, the pre-promotion step tile with
  `00000`, and battery at `100%`, with complete rows and no circular-edge
  clipping. Emulator weather remained unavailable; the runtime log records
  provider error code 4 rather than implying a condition or temperature.
- Confirmed `mWakefulness=Dozing` reduced the face to dimmed monochrome time
  only. The emulator was woken, its AVD name was re-proven, and only that target
  was stopped; the final ADB device list was empty.

Ignored screenshots, hierarchy dumps, power/display state, APK identity, and
runtime logs are retained under
`outputs/raster90/captures/clean-chamfer-runtime/`. This checkpoint supersedes
earlier emulator records for the selected primary numeral art and native
466×466 appearance only. The later [2026-08-21 checkpoint](2026-08-21-simulated-weather.md) supersedes it
for the final steps tile and simulated available-weather presentation. The
earlier 454×454 scaling evidence remains valid; physical clean-chamfer
appearance, sustained AOD, and battery impact remain separate gates.
