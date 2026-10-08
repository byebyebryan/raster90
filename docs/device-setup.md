# Device Setup and Deployment

Runbooks for the original Amazfit Balance, OnePlus Watch 3, and optional
OnePlus 13/phone emulator. Recorded OS/build values are dated baselines, not
a live inventory. Recheck the target before every device operation. Build and
asset commands belong in [Development](development.md); completed evidence
and remaining validation belong in [Validation](validation.md).

## Physical Amazfit Balance

| Property | Checkpoint value |
|---|---|
| Product | Amazfit Balance (original) |
| Zepp API level | 307 |
| Firmware | `3.28.8.1` |
| Display target | Native 480×480 round canvas |
| Raster 90 app ID | `1125469` |
| Deployment | Zepp App developer-mode QR preview |
| Evidence | Owner-reported device identity and owner-provided 480×480 screenshot, 2026-08-29 |

The first physical checkpoint proves the static Zepp package's interactive
resting layout: native weather with `15°C`, complete date and time, fixed-width
`00000` steps, and `61%` battery. It does not prove AOD, long-term refresh,
power impact, 12/24-hour behavior, or the subsequent metadata-only
debug-disabled build. Package architecture, exact screenshot hash, build
commands, and remaining acceptance gates are recorded in the
[Zepp package README](../watchfaces/raster90-zepp/README.md).

## Physical OnePlus 13

| Property | Checkpoint value (2026-08-15) |
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
| ADB transport | Pairing verified; Wireless debugging off at the checkpoint |

The development workstation was paired successfully on 2026-08-15. Pairing
codes are one-time credentials and are intentionally not retained. IP addresses
and TLS ports can change whenever Wireless debugging or the network changes.

Wireless debugging turned itself off after that validation. The phone is
optional for watch-face work; reconnect only for a phone-specific task and
verify its current state rather than assuming this baseline is still live.

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

| Property | Checkpoint value (2026-08-15) |
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

This is an acceptable product tradeoff. Raster 90 targets Smart Mode
and its ambient/AOD presentation; it does not need an RTOS/Power Saver variant.
Do not assume that a third-party face is rendered by the BES2800 or receives the
same Smart Mode optimizations as an official OnePlus face—measure battery life on
the physical device.

During a future physical power-mode validation, verify:

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

See the [dated target setup](checkpoints/2026-08-15-target-setup.md) for the
original phone-emulator validation record.

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

See the [dated target setup](checkpoints/2026-08-15-target-setup.md) for the
original primary-emulator validation record.

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

### Simulated-location weather on a Wear emulator

The available-weather emulator capture used Google's documented WFF weather-test
route. This is an emulator-only procedure for a Wear target whose identity has
already been proven as `wear5-opw3` or `wear5`; do not run root, appops, or test-
provider commands on a physical watch or phone. Resolve the serial again after
the ADB restart caused by `root`:

```sh
# <wear-emulator-serial> must already be proven as the intended Wear AVD.
rtk adb -s <wear-emulator-serial> unroot
rtk adb -s <wear-emulator-serial> shell cmd location set-location-enabled true
rtk adb -s <wear-emulator-serial> root
rtk adb -s <wear-emulator-serial> wait-for-device
rtk adb devices -l
rtk adb -s <wear-emulator-serial-after-root> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-emulator-serial-after-root> shell appops set 0 \
  android:mock_location allow
rtk adb -s <wear-emulator-serial-after-root> shell cmd location providers \
  add-test-provider gps
rtk adb -s <wear-emulator-serial-after-root> shell cmd location providers \
  set-test-provider-enabled gps true
rtk adb -s <wear-emulator-serial-after-root> shell cmd location providers \
  set-test-provider-location gps --location 37.773972,-122.431297
```

Re-prove the AVD name after `root` before continuing with deployment or capture.
The resulting weather is provider data for the simulated coordinates, not live
local or physical weather; network access and the Wear weather provider still
must be available. Label every resulting screenshot and evidence file as
simulated. This procedure changes emulator state only and does not hard-code
weather or location data into the watch-face bundle. This record documents the
tested sequence; it does not claim idempotence or provide untested cleanup
commands.

## Deploy, select, and capture Wear OS

First prove the physical model/API or chosen AVD identity using the sections
above. For an emulator, the expected AVD is `wear5-opw3` for pixel fidelity or
the secondary `wear5`. Then install and select the debug face:

```sh
rtk adb devices -l
rtk adb -s <verified-wear-serial> install -r \
  watchfaces/raster90/build/outputs/apk/debug/raster90-debug.apk
rtk adb -s <verified-wear-serial> shell am broadcast \
  -a com.google.android.wearable.app.DEBUG_SURFACE \
  --es operation set-watchface \
  --es watchFaceId io.github.byebyebryan.raster90.watchface
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

Retain a capture only when `mObscuringWindow` identifies a
`com.google.wear.watchface.runtime.DeclarativeWatchFaceRuntime*` window and the
image shows the selected face unobscured. The runtime index can change. Console
power commands are emulator-only; never send them to a physical device.

```sh
rtk mkdir -p outputs/raster90/captures/<checkpoint>
rtk adb -s <verified-wear-serial> shell dumpsys window displays
rtk adb -s <verified-wear-serial> shell dumpsys power
rtk adb -s <verified-wear-serial> exec-out screencap -p \
  > outputs/raster90/captures/<checkpoint>/watchface.png
```

Record identity, source/APK hashes, window, power, provider kind, and limits.
For runtime diagnostics, resolve its PID first, then target that PID:

```sh
rtk adb -s <verified-wear-serial> shell pidof -s com.google.wear.watchface.runtime
rtk adb -s <verified-wear-serial> logcat --pid <runtime-pid>
```

When both targets are attached, identify them before installing:

```sh
rtk adb devices -l
```

The emulator reports model `sdk_gwear_x86_64`; the physical watch reports
`OPWWE251`.
