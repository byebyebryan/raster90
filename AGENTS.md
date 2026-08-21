# Raster 90 — Project Context

Dedicated Raster 90 product repository. Raster 90 is a declarative Watch Face
Format (WFF) watch face for the OnePlus Watch 3, not a general-purpose Wear OS
app.

## Product and format decisions

- Start with **Watch Face Format v2** for Wear OS 5 / API 34 compatibility.
- Keep the watch-face bundle resource-only: `android:hasCode="false"` and
  `com.google.wear.watchface.format.version=2` in the manifest.
- Use the lowest WFF version that supports the design. WFF v3 requires Wear OS
  5.1 / API 35; WFF v4 requires Wear OS 6 / API 36.
- Do not use the legacy `androidx.wear.watchface` renderer unless a requirement
  cannot be expressed in WFF and the user explicitly changes direction.
- A WFF watch face and any future Wear/phone application logic must be separate
  app bundles. Do not add Kotlin/Java code to the watch-face bundle.
- Initial build targets: `compileSdk=35`, `targetSdk=35`, `minSdk=34`.
- The public watch-face name is **Raster 90**. `RASTER/90` is an optional visual
  treatment, not a different product name. The model number references the
  provisional 90×90 fine raster but remains a product designation if physical
  calibration changes the exact geometry.
- The permanent watch-face application ID is
  `io.github.byebyebryan.raster90.watchface`.
- Typography starts from the CC0 Pixel Operator family, but the runtime packages
  only deterministic bitmap-font glyphs generated from project-owned matrices. The
  four approved source TTFs and their license remain under `third_party/` as
  design provenance, never under the module's `res/font`.
- The packaged single-grid runtime treats the centered 450×450 active frame as
  one fictional 150×150 framebuffer. Every source cell is a solid 3×3 square
  with no gutter, and all elements use that one physical pixel scale. Historical
  checkpoints plus the 2026-08-21 simulated-weather capture validate this
  implementation at native 466×466 and scaled 454×454; the current exact tree
  is emulator-proven, while physical wearer validation remains open. The
  earlier 3-unit-pitch / 2×2-lit runtime remains historical comparison evidence,
  not the current visual design.
- Compact text remains based on the project-owned 5×7 glyphs. In the selected
  interactive composition, each 16-cell information band contains one
  vertically centered text line rather than two stacked 8-cell lines. The
  degree mark is a closed ring or box, never an open upper semicircle. Preview
  fixtures and the editable default use Celsius; users may explicitly choose
  Fahrenheit in the watch-face editor. The selected output converts the WFF
  provider value when its preferred unit differs, rather than merely relabeling
  it.
- Pixelarticons is visual research only for the current design pass. Do not add
  it as a dependency, vendor its SVGs, or mechanically trace/downsample them.
  Raster 90 icons remain independently authored, project-owned matrices unless
  a later explicit decision pins and licenses selected upstream assets.
- The packaged icon family is authored directly at true 16×16 resolution and
  rendered with solid 3×3 cells into 48×48 WFF tiles. The persistent resting
  icons are weather, steps, and battery. The calendar icon is intentionally
  removed; `SAT 15 AUG` is centered as text because it is already unambiguous.
  The selected step icon is the direct-authored `four-toe-vertical` pair of
  closed footprints with separated toe pads, one vertical 1×2 big-toe mark,
  three 1×1 toes per footprint, and vertically offset tapered soles; do not
  restore the walking-person silhouette or historical solid control.
  The weather tile remains the only persistent indexed-color plane. Do not
  integer-expand 8×8 art or use fractional nearest-neighbour resampling in the
  selected family; structural lines must be authored cell-by-cell with balanced
  optical weight.
- The interactive composition omits seconds and uses a static colon. Its
  fixed information set is time, date, current weather, step count, and battery.
  The available-weather resting rows are `[weather] 21°C`, centered `SAT 15 AUG`,
  `[steps] 03642`, and `[battery] 82%`; do not restore the redundant `WX`,
  `STP`, or `BAT` headers. Weather uses at most four flat visible palette
  entries; all other information remains white. Ambient mode reduces this to
  monochrome time only.
- The packaged face uses active-frame bands 45–93, 111–159, 177–273, 291–339,
  and 357–405. The solid
  3×3 time remains vertically centered in one 342×96 `TimeText`, using the
  selected reviewed clean-chamfer primary/display cut. The square construction
  and legacy fine-chamfer controls remain source-only in the canonical font
  component. Keep preview and runtime coordinates identical when implementing.
  Weather/date spacing may receive a later optical pass; do not change it
  implicitly.
- Available/stale/unavailable weather must remain truthful. The packaged
  unavailable branch uses the neutral weather icon with `--` on the same
  single-line baseline as available weather; do not restore a `WX` header or
  imply a condition or temperature. Available weather was physically proven on
  the earlier deployed tree and is emulator-proven on the current tree through
  a simulated location; stale data still requires live physical-device
  validation.
- Power Saver Mode support is not required for the custom face. On the physical
  watch, entering Power Saver with an unsupported third-party face displays a
  warning and substitutes a basic OnePlus face; that fallback is acceptable.

## Devices and API targets

| Device | Intended target | API | Status |
|---|---|---:|---|
| OnePlus Watch 3 (`OPWWE251`) | Wear OS 5 / Android 14 | 34 | Paired over Wi-Fi ADB; live-verified 2026-08-15 |
| OnePlus 13 (`CPH2655`) | Android 16 | 36 | Pairing verified 2026-08-15; Wireless debugging currently off; optional target |

Wear OS 5 maps to API 34, not API 35. The physical watch confirms Android 14 /
API 34. The physical OnePlus 13 confirms Android 16 / API 36. See
`docs/device-setup.md` for both devices' build identities, pairing state, and
reconnection procedures.

## Environment (EndeavourOS / Arch)

Live-checked 2026-08-15:

- Android Studio: `/opt/android-studio` (2026.1.3 build, bundled JBR 25).
  Android Studio is useful for WFF-aware XML validation and its watch-face run
  configuration, but ordinary builds should also work from the CLI.
- Shell Java is OpenJDK 26. Prefer Android Studio's JBR 25 for Gradle builds
  until the generated Gradle/AGP combination is proven compatible with Java 26.
- SDK root: `~/Android/Sdk` (`ANDROID_HOME`, added to `PATH` by `~/.zshenv`).
  - cmdline-tools 19.0
  - platform-tools 37.0.1
  - build-tools 35.0.0 and 36.0.0
  - emulator 37.1.11
  - platforms android-35 and android-36
  - Wear image `system-images;android-34;android-wear;x86_64` (Wear OS 5)
  - Phone image `system-images;android-36;google_apis_playstore;x86_64`
  - Retired generic image `system-images;android-35;google_apis;x86_64`
- There is no global Gradle installation. Commit and use the project's Gradle
  wrapper.
- `/dev/kvm` is available for accelerated emulation.

`~/.zshenv` is chezmoi-managed. Edit
`~/.local/share/chezmoi/dot_zshenv`, then run `rtk chezmoi apply`; never append
directly to `~/.zshenv`.

## Emulator

The primary pixel-fidelity AVD is `wear5-opw3`:

- Wear OS 5 / Android 14 / API 34
- `system-images;android-34;android-wear;x86_64`
- Official `wearos_large_round` hardware profile
- 466×466, 320 dpi, circular runtime display

It was created as a separate AVD without replacing any existing target. Its
generated profile defaults are preserved; only `hw.lcd.width` and
`hw.lcd.height` in `~/.android/avd/wear5-opw3.avd/config.ini` are set to `466`.
Use a centered 450×450 active WFF grid on a 466×466 canvas when needed, subject
to renderer calibration. Always perform final edge-placement and complication
checks on the physical watch.

Cold-boot it headlessly with SwiftShader:

```sh
rtk emulator -avd wear5-opw3 -no-window -no-audio -no-boot-anim \
  -gpu swiftshader_indirect -no-metrics -no-snapshot
```

Resolve the dynamic runtime serial and continue only after proving that it is
`wear5-opw3`; serial assignment can change whenever another AVD is attached:

```sh
rtk adb devices -l
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.qemu.avd_name
```

Sanity-check the same explicitly targeted device before relying on it:

```sh
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-opw3-serial> shell getprop ro.build.version.release
rtk adb -s <wear-opw3-serial> shell getprop ro.build.version.sdk
rtk adb -s <wear-opw3-serial> shell getprop ro.product.model
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.emulator.circular
rtk adb -s <wear-opw3-serial> shell wm size
rtk adb -s <wear-opw3-serial> shell wm density
rtk adb -s <wear-opw3-serial> shell pm list features
```

Expected evidence is model `sdk_gwear_x86_64`, Android `14`, SDK `34`, circular
value `1`, physical size `466x466`, density `320`, and features
`android.hardware.type.watch` and `com.google.clockwork.watchface.runtime`.
The corresponding runtime package is `com.google.wear.watchface.runtime`.
Before stopping, prove the identity again and stop only that verified target:

```sh
rtk adb -s <wear-opw3-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-opw3-serial> emu kill
```

The official `wear5` AVD remains unchanged as the secondary portability and
scaling reference:

- Wear OS 5 / Android 14 / API 34
- `system-images;android-34;android-wear;x86_64`
- `wearos_large_round` hardware profile
- 454×454, 320 dpi, circular runtime display

Use `wear5` for the official 454×454 WFF scaling reference; use
`wear5-opw3` for pixel-fidelity checks against the physical 466×466 watch.
Resolve and prove its dynamic serial before any targeted command:

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

The expected secondary evidence is model `sdk_gwear_x86_64`, SDK `34`, circular
value `1`, physical size `454x454`, density `320`, and the same watch/WFF
runtime features. Do not change the official `wear5` dimensions.

The validated phone AVD is `phone16`:

- Android 16 / API 36, Google Play x86_64 system image
- Official `pixel_9_pro_xl` hardware profile
- Runtime display aligned to 1440×3168 at 640 dpi to match the physical phone

Launch it headlessly from a cold boot:

```sh
rtk emulator -avd phone16 -no-window -no-audio -no-boot-anim \
  -gpu swiftshader_indirect -no-metrics -no-snapshot
```

Resolve the runtime serial and prove that it is `phone16` before stopping or
sanity-checking it:

```sh
rtk adb devices -l
rtk adb -s <phone-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <phone-emulator-serial> shell getprop ro.build.version.sdk
rtk adb -s <phone-emulator-serial> shell wm size
rtk adb -s <phone-emulator-serial> shell wm density
rtk adb -s <phone-emulator-serial> shell pm list features
rtk adb -s <phone-emulator-serial> emu kill
```

Expected phone evidence is AVD `phone16`, SDK `36`, 1440×3168 at 640 dpi,
`android.hardware.type.watch` absent, and Google Play services plus Play Store
packages present. With either emulator and either physical device attached,
always target every ADB command explicitly with `rtk adb -s <serial> ...`.

`wear5-generic-android15-backup-20260814` is a retired backup of the original
misconfigured AVD. It uses a generic Android 15 Google APIs image, is not a Wear
OS target, and must not be used for watch-face deployment or validation.

## Watch-face structure and workflow

The `:watchfaces:raster90` scaffold follows the official WFF sample structure:

- `AndroidManifest.xml` declares a resource-only WFF v2 application.
- `res/raw/watchface.xml` contains the face definition.
- `res/xml/watch_face_info.xml` declares preview/editability metadata.
- Generated bitmap fonts, weather sprites, strings, and the picker preview live
  in their normal `res/` directories. Non-font/non-runtime source matrices live
  in `design/raster90/`; authoritative project-owned font and selected icon
  components live under `fonts/raster90/` and `icons/raster90/`. All remain
  outside the application module. The complete secondary vocabulary and
  historical icon controls are presentation/source-only while the generators
  package only current WFF expression glyphs and selected icon surfaces.
- The packaged runtime uses a 466×466 WFF canvas with a centered 450×450 active
  grid. The official 454×454 target scales that coordinate space cleanly; the
  physical watch remains authoritative.

Build with the wrapper and JBR 25:

```sh
JAVA_HOME=/opt/android-studio/jbr rtk proxy ./gradlew \
  :watchfaces:raster90:assembleDebug \
  :watchfaces:raster90:lintDebug
```

Before building after any matrix or generator change, regenerate and verify the
exact asset surface:

```sh
rtk python3 -B tools/generate_raster90_assets.py
rtk python3 -B tools/generate_raster90_assets.py --check
rtk python3 -B tools/render_raster90_font_family.py
rtk python3 -B tools/render_raster90_font_family.py --check
rtk python3 -B tools/render_raster90_icon_family.py
rtk python3 -B tools/render_raster90_icon_family.py --check
```

For a Wear emulator deployment, resolve the runtime serial and prove the exact
chosen AVD name (`wear5-opw3` for pixel fidelity or the secondary `wear5`)
before installing. Installation alone does not guarantee that the face becomes
active; Android Studio's WFF run configuration deploys and selects it.
For the emulator-only simulated-location weather procedure, follow
`docs/device-setup.md`; never run its root, appops, or test-provider commands on
a physical device.
For local debug builds, the official codelab's debug surface also works:

```sh
rtk adb devices -l
rtk adb -s <wear-emulator-serial> shell getprop ro.boot.qemu.avd_name
rtk adb -s <wear-emulator-serial> install -r \
  watchfaces/raster90/build/outputs/apk/debug/raster90-debug.apk
rtk adb -s <wear-emulator-serial> shell am broadcast \
  -a com.google.android.wearable.app.DEBUG_SURFACE \
  --es operation set-watchface \
  --es watchFaceId io.github.byebyebryan.raster90.watchface
```

Confirm the selected face visually after every deploy.

The debug broadcast's favorite ID is not proof that the screenshot is
unobscured. A cold-booted AVD may leave its charging activity or app launcher
above the WFF window. On an identity-proven emulator only, use `emu power ac
off` and `emu power status discharging`, dismiss the overlay, and verify that
`mObscuringWindow` is
`com.google.wear.watchface.runtime.DeclarativeWatchFaceRuntime0` before
retaining a capture. Never send emulator-console power commands to a physical
device.

Use both textual and visual checks:

```sh
rtk mkdir -p outputs/raster90/captures/<checkpoint>
rtk adb -s <wear-emulator-serial> shell uiautomator dump /sdcard/window.xml
rtk adb -s <wear-emulator-serial> exec-out cat /sdcard/window.xml
rtk adb -s <wear-emulator-serial> exec-out screencap -p \
  > outputs/raster90/captures/<checkpoint>/watchface.png
```

Keep disposable but reviewable local artifacts under the Git-ignored root
`outputs/` directory rather than `/tmp`. Namespace artifacts by product, then
purpose: generated studies belong under `outputs/raster90/studies/<study>/`,
emulator or physical-device evidence under
`outputs/raster90/captures/<checkpoint>/`, and external visual references under
`outputs/references/`. Do not restore a flat output dump. Use descriptive
target-and-mode names when retaining multiple captures.

Public README media is the narrow exception: `docs/media/` may contain a small
tracked subset copied byte-for-byte from a completed capture checkpoint. Record
its provenance in `docs/media/README.md`, keep the full evidence under
`outputs/`, and never retouch a runtime capture or promote it beyond what the
identity, window, power, and provider evidence proves.

For renderer failures, first obtain the runtime PID with
`rtk adb -s <serial> shell pidof -s com.google.wear.watchface.runtime`, then
inspect that PID with `rtk adb -s <serial> logcat --pid <PID>`.

Before publishing, run the WFF XML validator and memory-footprint checks in
addition to the normal Gradle build and lint gates. Test interactive, ambient,
12/24-hour, complication, and round-edge behavior on the emulator, then repeat
on the physical watch.

## Physical watch

The OnePlus Watch 3 was paired successfully on 2026-08-15. Live identity:

- Product/model/device: `OPWWE251`
- Android 14 / API 34
- Display: 466×466, 320 dpi, circular, 60 Hz
- Userspace ABI: `armeabi-v7a,armeabi`
- Build: `AW2A.240903.001.A3.OPWWE251_11_A.162.260526`
- Security patch: 2026-05-01
- Features: `android.hardware.type.watch` and
  `com.google.clockwork.watchface.runtime`

Wireless ADB ports are ephemeral. With Wireless debugging enabled and both
machines on the same LAN, the paired watch normally reconnects through mDNS.
Discover it with:

```sh
rtk adb mdns services
rtk adb devices -l
```

If automatic reconnection fails, use the current `_adb-tls-connect._tcp`
endpoint from mDNS with `rtk adb connect <ip>:<debug-port>`. Pair again only if
the stored trust has been removed. Never record a pairing code.

When any emulator and either physical device are attached, always target commands
explicitly with `rtk adb -s <serial> ...`.

### Pairing a new or reset watch

On the watch: enable Developer Options by tapping Build Number seven times,
then enable ADB debugging and Wireless debugging. Pair and connect with:

```sh
rtk adb pair <ip>:<pairing-port>
rtk adb connect <ip>:<debug-port>
```

After connecting, verify the serial and API level before installing anything:

```sh
rtk adb devices -l
rtk adb -s <serial> shell getprop ro.build.version.release
rtk adb -s <serial> shell getprop ro.build.version.sdk
```

## Physical OnePlus 13

The OnePlus 13 was paired and verified successfully on 2026-08-15. It is an
optional future companion target and is not required for watch-face work. Live
identity from that verification:

- Product/model/device: `CPH2655` / `CPH2655` / `OP5D55L1`
- Android 16 / API 36
- Display: 1440×3168, 640 dpi
- Userspace ABI: `arm64-v8a`
- Build ID: `BP2A.250605.015`
- Security patch: 2026-07-01
- Companion feature: `android.software.companion_device_setup`

Wireless debugging turned itself off after the initial validation and is
currently intentionally left off. Its absence is not a project blocker.
Wireless ADB ports are ephemeral; when phone work is required, re-enable
Wireless debugging and discover the phone through mDNS:

```sh
rtk adb mdns services
rtk adb devices -l
```

If automatic reconnection fails, use the current `_adb-tls-connect._tcp`
endpoint from mDNS with `rtk adb connect <ip>:<debug-port>`. Pair again only if
the stored trust was removed; never record a pairing code or transient endpoint.
Before any install or other state-changing command, verify the current phone
serial and target it explicitly:

```sh
rtk adb devices -l
rtk adb -s <phone-serial> shell getprop ro.product.model
rtk adb -s <phone-serial> shell getprop ro.build.version.sdk
rtk adb -s <phone-serial> shell wm size
rtk adb -s <phone-serial> shell wm density
```

## Next steps

- [x] Initialize the dedicated Raster 90 repository and record module/package
  boundaries.
- [x] Choose Raster 90 as the public watch-face name.
- [x] Choose `io.github.byebyebryan.raster90.watchface` as the permanent
  application ID.
- [x] Scaffold and validate the standalone resource-only WFF v2 project.
- [x] Draft the initial visual direction and fictional-hardware constraints.
- [x] Select Pixel Operator as the starting typography family.
- [x] Define the baseline information set without seconds.
- [x] Record the provisional two-tier raster and conservative circular fit
  budget.
- [x] Validate both raster tiers, Pixel Operator specimens, the circular safe
  area, and ambient reduction on the primary 466×466 emulator.
- [x] Generate exact bitmap-font/weather assets from reviewable matrices and
  implement the functional V1 time, date, weather, steps, battery, and
  time-only ambient composition.
- [x] Validate V1 interactive and ambient rendering on both the native 466×466
  and scaled 454×454 Wear OS 5 emulators.
- [ ] Complete physical-watch validation of the exact current solid-grid tree.
  Current-tree interactive rendering and simulated available weather are proven
  on `wear5-opw3`; the latest physical captures predate both the final
  `four-toe-vertical` steps tile and clean-chamfer time cut. Wearer judgment of
  AMOLED appearance, bezel, wrist distance, sustained AOD, and battery remains
  open. The earlier 3/2 runtime remains comparison evidence only.
- [x] Live-test available weather with real physical-watch data, including a
  night-family condition icon and the WFF provider's Fahrenheit unit (historical
  pre-final-art deployment; current emulator weather uses a documented simulated
  GPS test provider).
- [ ] Live-test stale weather with real data; emulator testing proves the
  truthful icon-plus-`--` unavailable fallback and the current simulated
  available-weather route, but not stale data.
- [x] Produce actual-size icon studies exposing the optical-weight and
  recognizability problems in the earlier 8×8/12×12 split.
- [x] Package and validate the 150×150 single-grid system at native 466×466 and
  scaled 454×454, including interactive, time-only ambient, and 12/24-hour sync
  (historical plus current-tree emulator evidence; the current capture uses a
  simulated GPS weather provider).
- [x] Normalize and package all mapped WFF weather conditions plus steps and
  battery on uniform 16×16 icon tiles; the calendar icon was deliberately
  removed from the selected composition.
- [x] Recalculate and implement the single-grid row bands and circular fit.
- [x] Select the next visual direction from deterministic mocks: solid 3×3 base
  cells, true 16×16 weather/steps/battery icons, one icon-led value per row,
  centered date text, and no calendar or redundant field headers.
- [x] Implement the selected solid-grid design in generated assets, preview, and
  WFF without weakening truthful weather fallbacks.
- [x] Validate the selected redesign at native 466×466 and scaled 454×454 before
  treating the mocks as runtime evidence.
- [x] Implement the header-free unavailable-weather presentation as a neutral
  icon plus `--` on one centered row.
- [x] Live-test a fresh available state with real physical-watch weather data
  (historical pre-final-art deployment).
- [x] Add an editable Celsius-default temperature-unit setting with an explicit
  Fahrenheit override and declarative conversion of the WFF provider value;
  verify both editor choices on the primary Wear OS 5 emulator and live
  converted Celsius output on the physical watch.
- [ ] Live-test a stale state with real location/weather data.
- [x] Formalize the selected reviewed clean-chamfer primary/display numerals,
  retain square and legacy fine-chamfer controls, and complete the project-owned
  secondary/text family; physical wearer optical review remains open.
- [x] Deploy the selected clean-chamfer runtime to the identity-proven
  `wear5-opw3` target and capture native 466×466 interactive and confirmed
  Dozing time-only evidence without clipping.
- [x] Capture the current exact runtime tree on `wear5-opw3` with the documented
  GPS test provider: available simulated weather, final footprints, clean-
  chamfer time, and confirmed Dozing time-only behavior; physical and stale
  weather gates remain open.
- [ ] Design post-V1 animation and rare color events separately from the stable
  resting face.
- [x] Pair the physical OnePlus Watch 3 over Wi-Fi and record its live OS/API.
- [x] Pair the physical OnePlus 13 over Wi-Fi and validate the `phone16` API 36
  Google Play emulator target.
