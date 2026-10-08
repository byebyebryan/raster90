# Raster 90 refreshed-icon physical checkpoint — 2026-08-26

Freshly deployed packaged runtime `4a90116` to the identity-proven physical
OnePlus Watch 3 after promoting the refreshed static weather family:

- The exact generated surface contained 87 PNGs. Asset, font-presentation, and
  icon-presentation checks passed with 51 Python tests, `xmllint`, JBR 25 debug
  assembly and lint, WFF validator 1.7.0 for format v2, and the official memory
  gate. The evaluator reported 684,000 active bytes and 155,520 ambient bytes.
- Before installation, the explicit ADB target reported model `OPWWE251`,
  Android 14 / API 34, 466×466 at 320 dpi, `armeabi-v7a,armeabi`, and the watch
  and WFF runtime features. The target was physical rather than an emulator.
- The freshly built APK and its installed `base.apk` both had SHA-256
  `d435df22dbe9bcc7ebc4a0cec768212115fac65853aee50bad2222a0a93d6aef`.
  Installation succeeded, and the WFF debug surface selected
  `io.github.byebyebryan.raster90.watchface` with runtime version 2.
- In an `Awake` state, `mObscuringWindow` identified
  `com.google.wear.watchface.runtime.DeclarativeWatchFaceRuntime0`. The settled
  native capture rendered the refreshed outlined clear-night crescent with live
  provider weather at `18°C`, centered `WED 26 AUG`, clean-chamfer time, final
  `four-toe-vertical` footprints with `03591` steps, and the healthy white
  battery branch at `86%`, with complete rows and no clipping.
- This checkpoint proves the exact packaged tree's physical interactive
  renderer, current static icon integration, and a fresh available night-
  weather state. It does not prove sustained physical AOD, the yellow/orange/red
  battery branches, a stale-weather state, battery impact, perceived AMOLED
  quality, bezel appearance, or wrist-distance legibility.

The settled unretouched capture is retained at
`outputs/raster90/captures/physical-latest-weather-icons-20260826/interactive-power-wake.png`.
Transient pairing credentials and endpoints are not retained.
