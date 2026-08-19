# Device Setup and Verification

Live verification record for the physical OnePlus 13, physical OnePlus Watch 3,
and local phone and Wear OS emulators. Physical devices were last checked
2026-08-15; Raster 90 typography rendering was checked 2026-08-18.

## Physical OnePlus 13

| Property | Verified value |
|---|---|
| Manufacturer | OnePlus |
| Product, model, and device | `CPH2655` / `CPH2655` / `OP5D55L1` |
| Android release | 16 |
| SDK/API level | 36 |
| Display | 1440×3168, 640 dpi |
| Userspace ABI | `arm64-v8a` |
| Build ID | `BP2A.250605.015` |
| Build fingerprint | `OnePlus/CPH2655/OP5D55L1:16/BP2A.250605.015/V.R4T3.52da06f-2e397f6-2e81775:user/release-keys` |
| Security patch | 2026-07-01 |
| Companion-device feature | `android.software.companion_device_setup` |
| ADB transport | Pairing verified; Wireless debugging currently off |

The development workstation was paired successfully on 2026-08-15. Pairing
codes are one-time credentials and are intentionally not retained. IP addresses
and TLS ports can change whenever Wireless debugging or the network changes.

Wireless debugging turned itself off after validation. The phone is optional
for the current watch-face project, so it is intentionally left disconnected.
Re-enable it only when a phone-specific task requires the physical target.

### Reconnect

Enable Wireless debugging on the phone and keep both devices on the same LAN.
The trusted phone normally appears automatically:

```sh
rtk adb mdns services
rtk adb devices -l
```

If the `_adb-tls-connect._tcp` service is visible but no device is attached:

```sh
rtk adb connect <ip>:<debug-port>
```

Re-pair only if the phone or workstation has forgotten the trust relationship:

```sh
rtk adb pair <ip>:<pairing-port>
```

Enter the transient code shown by **Wireless debugging → Pair new device**. Do
not save it in project files or shell history. Never record the current IP,
pairing endpoint, or mDNS serial.

### Verify identity

Resolve the current serial from `adb devices -l`, then target the physical phone
explicitly—especially when `phone16` or `wear5` is also running:

```sh
rtk adb -s <phone-serial> shell getprop ro.product.model
rtk adb -s <phone-serial> shell getprop ro.product.device
rtk adb -s <phone-serial> shell getprop ro.build.version.release
rtk adb -s <phone-serial> shell getprop ro.build.version.sdk
rtk adb -s <phone-serial> shell getprop ro.build.id
rtk adb -s <phone-serial> shell getprop ro.build.version.security_patch
rtk adb -s <phone-serial> shell wm size
rtk adb -s <phone-serial> shell wm density
rtk adb -s <phone-serial> shell pm list features
```

Expected core values are `CPH2655`, `OP5D55L1`, Android `16`, API `36`,
1440×3168 at 640 dpi, and the companion-device feature recorded above.

## Physical OnePlus Watch 3

| Property | Verified value |
|---|---|
| Manufacturer | OnePlus |
| Product, model, and device | `OPWWE251` |
| Android release | 14 |
| SDK/API level | 34 |
| Display | 466×466, 320 dpi, circular, 60 Hz |
| Userspace ABI | `armeabi-v7a,armeabi` |
| Build ID | `AW2A.240903.001.A3.OPWWE251_11_A.162.260526` |
| Build fingerprint | `OnePlus/OPWWE251/OPWWE251:14/AW2A.240903.001.A3.OPWWE251_11_A.162.260526/01:user/release-keys` |
| Security patch | 2026-05-01 |
| Watch feature | `android.hardware.type.watch` |
| WFF runtime feature | `com.google.clockwork.watchface.runtime` |
| ADB transport | Wireless debugging over trusted mDNS |

The development workstation was paired successfully on 2026-08-15. Pairing
codes are one-time credentials and are intentionally not retained. IP addresses
and TLS ports can change whenever Wireless debugging or the network changes.

### Reconnect

Enable Wireless debugging on the watch and keep both devices on the same LAN.
The trusted watch normally appears automatically:

```sh
rtk adb mdns services
rtk adb devices -l
```

If the `_adb-tls-connect._tcp` service is visible but no device is attached:

```sh
rtk adb connect <ip>:<debug-port>
```

Re-pair only if the watch or workstation has forgotten the trust relationship:

```sh
rtk adb pair <ip>:<pairing-port>
```

Enter the transient six-digit code shown by **Wireless debugging → Pair new
device**. Do not save it in project files or shell history.

### Verify identity

Resolve the current serial from `adb devices -l`, then target the physical watch
explicitly—especially when the emulator is also running:

```sh
rtk adb -s <watch-serial> shell getprop ro.product.model
rtk adb -s <watch-serial> shell getprop ro.build.version.release
rtk adb -s <watch-serial> shell getprop ro.build.version.sdk
rtk adb -s <watch-serial> shell getprop ro.build.id
rtk adb -s <watch-serial> shell getprop ro.build.version.security_patch
rtk adb -s <watch-serial> shell pm list features
```

Expected core values are `OPWWE251`, Android `14`, API `34`, and the two watch
and WFF runtime features recorded above.

## Power modes and custom faces

Observed on the physical watch with a third-party face installed from Google
Play:

- The custom face works in normal Smart Mode.
- Entering Power Saver Mode warns that the custom face is unsupported there.
- The watch substitutes a basic OnePlus face for Power Saver Mode.
- Power Saver Mode itself remains available; only the custom face is lost while
  that mode is active.

This is an acceptable product tradeoff. The planned WFF face targets Smart Mode
and its ambient/AOD presentation; it does not need an RTOS/Power Saver variant.
Do not assume that a third-party face is rendered by the BES2800 or receives the
same Smart Mode optimizations as an official OnePlus face—measure battery life on
the physical device.

After the first local WFF build is installed, verify:

1. The custom face remains selected through ordinary screen-off/AOD cycles.
2. Power Saver Mode selects a safe fallback without errors or rebooting.
3. Leaving Power Saver Mode restores or allows reselecting the custom face.
4. Smart Mode battery behavior is acceptable over a representative day.

## Android 16 phone emulator

The durable `phone16` AVD uses the official `pixel_9_pro_xl` profile and the
Google Play x86_64 image `system-images;android-36;google_apis_playstore;x86_64`.
Only the generated display dimensions and density were customized so the
runtime matches the physical OnePlus 13: `hw.lcd.width=1440`,
`hw.lcd.height=3168`, and `hw.lcd.density=640` in
`~/.android/avd/phone16.avd/config.ini`. Other profile defaults remain intact.

### Comparison with the physical target

| Property | `phone16` emulator | OnePlus 13 |
|---|---|---|
| Android / API | 16 / 36 | 16 / 36 |
| Identity | `sdk_gphone64_x86_64` / `emu64xa` | `CPH2655` / `OP5D55L1` |
| Display | 1440×3168 | 1440×3168 |
| Density | 640 dpi | 640 dpi |
| Form factor | Normal phone; no `android.hardware.type.watch` | Normal phone |
| Userspace ABI | `x86_64` | `arm64-v8a` |
| Image/profile | Google Play x86_64 / `pixel_9_pro_xl` | OnePlus production build |
| Google packages | Google Play services and Play Store present | Device-provided |

The emulator is a display/API and Google-services development analogue, not a
hardware replica. The physical phone remains authoritative for OnePlus OEM
behavior, sensors, performance, radios, and battery behavior.

### Launch and stop

Use an explicit, cold-booted headless launch:

```sh
rtk emulator -avd phone16 -no-window -no-audio -no-boot-anim \
  -gpu swiftshader_indirect -no-metrics -no-snapshot
```

Resolve the runtime serial and prove that it is `phone16` before stopping it;
serial assignment is dynamic when `wear5` or another AVD is attached:

```sh
rtk adb devices -l
rtk adb -s <phone-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <phone-emulator-serial> shell getprop ro.build.version.sdk
rtk adb -s <phone-emulator-serial> shell wm size
rtk adb -s <phone-emulator-serial> shell wm density
```

After confirming `phone16`, stop only that verified target:

```sh
rtk adb -s <phone-emulator-serial> emu kill
```

When the phone, watch, or another emulator is attached, never rely on the
default ADB target; use `rtk adb -s <serial> ...` for every command.

### Fresh validation record

Validated 2026-08-15 after installing the API 36 Google Play image (sdkmanager
package version `7`) and creating `phone16` without replacing any existing AVD:

- The emulator reported `Boot completed in 20903 ms` with SwiftShader and no
  fatal emulator startup error.
- `ro.boot.qemu.avd_name` was `phone16`; Android release/API were `16` / `36`;
  build ID was `BE2A.250530.026.D1`.
- `wm size` and `wm density` reported `1440×3168` and `640`.
- `pm list features` showed normal phone capabilities and no
  `android.hardware.type.watch` feature.
- `com.google.android.gms` and `com.android.vending` were installed; the
  launcher exposed a working Play Store entry.
- A UI Automator dump showed the Nexus Launcher hierarchy, and a 1440×3168
  screenshot showed a usable Android launcher with Phone, Messages, Play Store,
  Chrome, and Camera controls.
- The emulator emitted routine first-boot Google-service/no-account warnings in
  logcat, but no fatal boot failure. No package was installed on either physical
  device during this validation.
- The physical phone's wireless ADB transport dropped during the session and
  Wireless debugging was later found switched off. The phone was not modified;
  re-enable debugging before any future physical-phone validation.

During this historical validation, the runtime serial was `emulator-5554` and
the identity check showed `phone16`; only that verified target was stopped. The
watch was reconnected. The phone is intentionally offline; when it is needed,
re-enable Wireless debugging and verify whether the stored pairing remains.

## Emulator reference

### Primary pixel-fidelity target: `wear5-opw3`

The `wear5-opw3` AVD is the primary local target for matching the physical
OnePlus Watch 3 pixel grid. It is a separate Wear OS 5 / Android 14 / API 34
AVD created from the installed
`system-images;android-34;android-wear;x86_64` image and official
`wearos_large_round` hardware profile. The generated profile defaults are
preserved; only these persistent display values differ from the generated
454×454 profile:

```ini
hw.lcd.width=466
hw.lcd.height=466
hw.lcd.density=320
```

The config is `~/.android/avd/wear5-opw3.avd/config.ini`. WFF work may use a
466×466 canvas with a centered 450×450 active grid, subject to renderer
calibration; this is a coordinate-space note, not a visual design specification.

| Property | `wear5-opw3` emulator | OnePlus Watch 3 |
|---|---|---|
| Android / API | 14 / 34 | 14 / 34 |
| Identity | `sdk_gwear_x86_64` / `emu64xa` | `OPWWE251` / `OPWWE251` |
| Display | 466×466 | 466×466 |
| Density | 320 dpi | 320 dpi |
| Shape / refresh | Circular / 60 Hz | Circular / 60 Hz |
| Userspace ABI | `x86_64,arm64-v8a` | `armeabi-v7a,armeabi` |
| Image/profile | Wear OS 5 x86_64 / `wearos_large_round` | OnePlus production build |
| WFF runtime | Feature and package present | Feature present |

Cold-boot the primary target headlessly with SwiftShader:

```sh
rtk emulator -avd wear5-opw3 -no-window -no-audio -no-boot-anim \
  -gpu swiftshader_indirect -no-metrics -no-snapshot
```

Resolve the dynamic serial and prove the AVD identity before any targeted
operation. Never assume `emulator-5554` or another serial:

```sh
rtk adb devices -l
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.qemu.avd_name
```

Continue only when that command returns `wear5-opw3`, then run the sanity
checks against the same explicit serial:

```sh
rtk adb -s <wear-opw3-serial> shell getprop ro.build.version.release
rtk adb -s <wear-opw3-serial> shell getprop ro.build.version.sdk
rtk adb -s <wear-opw3-serial> shell getprop ro.product.model
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.emulator.circular
rtk adb -s <wear-opw3-serial> shell wm size
rtk adb -s <wear-opw3-serial> shell wm density
rtk adb -s <wear-opw3-serial> shell pm list features
rtk adb -s <wear-opw3-serial> shell pm list packages
```

Expected values are Android `14`, API `34`, model `sdk_gwear_x86_64`, circular
runtime `1`, physical size `466x466`, density `320`, feature
`android.hardware.type.watch`, feature `com.google.clockwork.watchface.runtime`,
and package `com.google.wear.watchface.runtime`.

Before stopping, repeat the identity proof and stop only the verified target:

```sh
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-opw3-serial> emu kill
```

#### Fresh primary-target validation record

Validated 2026-08-15 without replacing or modifying `wear5`, `phone16`, or the
retired backup AVD:

- `avdmanager` created `wear5-opw3` without `--force`; the pre-create AVD list
  did not contain that name.
- The cold boot used the launch command above. Emulator startup selected
  SwiftShader, reported `wear5-opw3`, `sdk_gwear_x86_64`, circular runtime, and
  boot completed successfully. The runtime serial was resolved dynamically.
- Android reported release/API `14` / `34`, model `sdk_gwear_x86_64`, physical
  size `466x466`, density `320`, `android.hardware.type.watch`, and
  `com.google.clockwork.watchface.runtime`.
- Package `com.google.wear.watchface.runtime` was present at version
  `332917000`; the Wear services and declarative watch-face packages were
  present.
- UI Automator returned a root hierarchy bounded `[0,0][466,466]`, and a
  screencap was a 466×466 RGBA PNG showing the default circular watch UI.
- The image emitted a repeated prebuilt sensor-HAL abort
  (`/vendor/bin/hw/android.hardware.sensors-service.multihal`, unexpected
  sensor type `26`). Wear System UI remained foreground and the target stayed
  usable for the identity, hierarchy, and screenshot checks; treat sensor
  features as unreliable on this emulator until separately investigated.

The emulator was stopped only after re-proving `ro.boot.qemu.avd_name`, and the
temporary UI dump/screenshot artifacts were removed. The final AVD list still
contained `wear5-opw3`, `wear5`, `phone16`, and
`wear5-generic-android15-backup-20260814`.

### Secondary portability/scaling reference: `wear5`

The official `wear5` AVD remains unchanged as the secondary Wear OS 5 / Android
14 / API 34 target using `system-images;android-34;android-wear;x86_64` and the
`wearos_large_round` profile. It is the official 454×454 portability/scaling
reference; use `wear5-opw3` for pixel-fidelity checks against the physical
466×466 display. Its expected runtime is circular, 320 dpi, with the watch and
WFF runtime features.

Launch it only when the 454×454 reference is needed, and resolve its dynamic
serial before targeted commands:

```sh
rtk emulator -avd wear5 -no-window -no-audio -no-boot-anim \
  -gpu swiftshader_indirect -no-metrics -no-snapshot
rtk adb devices -l
rtk adb -s <wear-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-emulator-serial> shell wm size
rtk adb -s <wear-emulator-serial> shell wm density
rtk adb -s <wear-emulator-serial> shell getprop ro.boot.emulator.circular
rtk adb -s <wear-emulator-serial> shell pm list features
rtk adb -s <wear-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-emulator-serial> emu kill
```

The AVD named `wear5-generic-android15-backup-20260814` is a retired backup of
the original misconfigured target. It uses
`system-images;android-35;google_apis;x86_64`, is generic Android rather than
Wear OS, and must never be used for watch-face deployment or validation. It is
retained only as an explicit backup until removal is separately authorized.

### Comparison with the physical target

| Property | `wear5` emulator | OnePlus Watch 3 |
|---|---|---|
| Android / API | 14 / 34 | 14 / 34 |
| Display | 454×454 | 466×466 |
| Density | 320 dpi | 320 dpi |
| Shape / refresh | Circular / 60 Hz | Circular / 60 Hz |
| Userspace ABI | `x86_64,arm64-v8a` | `armeabi-v7a,armeabi` |
| WFF runtime version | `332917000` | `332919060` |
| Sensor data | Emulated subset; no heart-rate or step-counter feature | Real heart-rate, step-counter, step-detector, and OEM sensors |

The official large-round `wear5` AVD is the correct secondary portability
target and remains at 454×454. The primary `wear5-opw3` target covers exact
466×466 pixel placement. WFF uses a 450×450 active grid; a centered grid on a
466×466 canvas is subject to renderer calibration. The physical watch remains
authoritative for edge placement, sensor-backed complications, OEM behavior,
and battery testing.

The emulator cannot represent OnePlus's BES2800/RTOS, Dual-Engine behavior,
Power Saver fallback, or OEM watch-face picker. Those require the physical
watch.

### End-to-end WFF v2 validation

#### Raster 90 solid-grid runtime — 2026-08-18

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

This checkpoint supersedes the icon-weight and 3/2 single-grid runtime records
below for current packaged geometry, resource count, memory, and emulator
appearance. Physical-watch rendering, live available/stale weather, and final
time-numeral authorship remain open.

#### Raster 90 icon stroke-weight correction — 2026-08-18

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

#### Raster 90 single-grid runtime candidate — 2026-08-18

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

#### Raster 90 typography refinement — 2026-08-18

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

#### Raster 90 V1 — 2026-08-17

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

#### Raster 90 calibration scaffold — 2026-08-17

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

#### Official sample baseline — 2026-08-15

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

Use this explicit-target flow for new deployments; first prove that the chosen
serial belongs to the intended AVD (`wear5-opw3` for pixel fidelity or the
secondary `wear5`):

```sh
rtk adb devices -l
rtk adb -s <wear-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-emulator-serial> install -r <debug-apk>
rtk adb -s <wear-emulator-serial> shell am broadcast \
  -a com.google.android.wearable.app.DEBUG_SURFACE \
  --es operation set-watchface --es watchFaceId <application-id>
```

The debug broadcast's favorite ID proves selection was requested, not that a
screenshot is unobscured. A cold-booted AVD can show its full-screen charging
activity or app launcher above the WFF window. On an identity-proven emulator,
disable simulated AC power and dismiss the overlay before retaining evidence:

```sh
rtk adb -s <wear-emulator-serial> emu power ac off
rtk adb -s <wear-emulator-serial> emu power status discharging
rtk adb -s <wear-emulator-serial> shell input keyevent KEYCODE_BACK
rtk adb -s <wear-emulator-serial> shell dumpsys window
```

Only retain the capture after `mObscuringWindow` identifies
`com.google.wear.watchface.runtime.DeclarativeWatchFaceRuntime0`. This is an
emulator presentation check; do not send emulator-console power commands to a
physical device.

When both targets are attached, identify them before installing:

```sh
rtk adb devices -l
```

The emulator reports model `sdk_gwear_x86_64`; the physical watch reports
`OPWWE251`.
