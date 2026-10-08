# Emulator target setup — 2026-08-15

Historical identity/setup evidence. Use [Device Setup](../device-setup.md)
for current runbooks and recheck live identities before device operations.

## Phone16

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

## Wear5-opw3

Validated 2026-08-15 without replacing or modifying `wear5`, `phone16`, or the
retired backup AVD:

- `avdmanager` created `wear5-opw3` without `--force`; the pre-create AVD list
  did not contain that name.
- The cold boot used the launch command recorded in [Device Setup](../device-setup.md). Emulator startup selected
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
